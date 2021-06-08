import hashlib
import os
import shutil
import subprocess
from os import PathLike, path
from pathlib import Path
from typing import List, NamedTuple, Optional, Tuple

from jinja2 import Environment, PackageLoader
from splashgen.site_config import DEFAULT_BRANDING, SEO, Branding, Link

jinja = Environment(loader=PackageLoader(
    "splashgen", "jinja_templates"), autoescape=False)


class Import(NamedTuple):
    """See: https://github.com/microsoft/TypeScript/blob/663b19fe4a7c4d4ddaa61aedadd28da06acd27b6/src/compiler/types.ts"""

    clause: Optional[str]
    """This is a string version of an ImportClause node"""

    mod: str

    def __str__(self) -> str:
        if self.clause is not None:
            return f'import {self.clause} from "{self.mod}"'
        return f'import "{self.mod}"'


class SourceFile(object):
    _imports: List[Import]

    def __init__(self, output_path: str, context: 'BuildContext') -> None:
        self.output_path = output_path
        self.context = context
        self._imports = []
        self._code = ""

    def add_imports(self, *imports: Import) -> None:
        self._imports.extend(imports)

    def add_import(self, import_: Import) -> None:
        self.add_imports(import_)


# NOTE: In the future, this could be a frontend/ dir that's in the codebase's
# repo
_FRONTEND_DIR = (Path(path.dirname(__file__)) / '..' / 'frontend').resolve()


class BuildContext(object):
    def __init__(self, source_dir: Path, build_dir: Path) -> None:
        self.source_dir = source_dir
        self.build_dir = build_dir
        self.cache_dir = self.build_dir / "sg-buildcache"
        self.tmp_dir = self.build_dir / "sg-temp"

        for dirname in (self.cache_dir, self.tmp_dir):
            os.makedirs(dirname, exist_ok=True)

    def copy_from_frontend(self, *sources: PathLike) -> None:
        for source in sources:
            source_path = _FRONTEND_DIR / source
            if not source_path.exists():
                raise IOError(f"Could not find source {source}")
            dest_path = self.build_dir / source
            shutil.copyfile(source_path, dest_path)

    def mkdirs(self, *dirs: PathLike) -> None:
        for dir in dirs:
            os.makedirs(self.build_dir / dir, exist_ok=True)

    def run_installs_if_necessary(self) -> None:
        if self._pkg_files_changed():
            self._run_npm_install()
            self._cache_pkg_md5()

    def write_to_public(self, input: PathLike) -> Tuple[bool, str]:
        written = False
        outfile = self.build_dir / "public" / path.basename(input)
        in_hash = self._get_md5(input)
        if not outfile.exists() or self._get_md5(outfile) != in_hash:
            shutil.copyfile(input, outfile)
            written = True

        return (written, outfile)

    def gen_favicon(self, logo_pathlike: PathLike) -> None:
        print("Generating favicons")
        logo_path = Path(logo_pathlike)
        if not logo_path.exists():
            raise IOError("Could not find logo for favicon")
        gen_favicons_script = Path(self.tmp_dir / "gen-favicons.js")
        shutil.copyfile(_FRONTEND_DIR / "_scripts" / "gen-favicons.js",
                        gen_favicons_script)
        subprocess.run(f"node {Path(*gen_favicons_script.parts[1:])} {Path(*logo_path.parts[1:])} public/",
                       shell=True, cwd=self.build_dir, check=True)

    def _pkg_files_changed(self) -> bool:
        cached_pkg = self._read_cached("package.json-md5")
        pkg_md5 = self._get_md5(self.build_dir / "package.json")

        if cached_pkg is None or pkg_md5 != cached_pkg:
            return True
        return False

    def _read_cached(self, filename: PathLike) -> Optional[str]:
        cached = None
        cached_file = self.cache_dir / filename
        if cached_file.exists():
            with open(cached_file, 'r') as f:
                cached = f.read()

        return cached

    def _run_npm_install(self):
        print("Installing dependencies")
        subprocess.run("npm install", shell=True,
                       cwd=self.build_dir, check=True)

    def _cache_pkg_md5(self):
        md5 = self._get_md5(self.build_dir / "package.json")
        if md5 is not None:
            self._write_cached("package.json-md5", md5)

    def _write_cached(self, filename: PathLike, content: str) -> None:
        with open(self.cache_dir / filename, 'w') as f:
            f.write(content)

    def _get_md5(self, filepath: PathLike) -> Optional[str]:
        if not Path(filepath).exists():
            return None
        with open(filepath, 'r') as f:
            return hashlib.md5(f.read().encode("utf-8")).hexdigest()

    def create_synthetic_component(self, cmp: 'Component') -> SourceFile:
        pass


class Component(object):
    def render(self) -> Optional['Component']:
        return None

    def gen_sources(self, ctx: BuildContext) -> List[str]:
        py_component = self.render()
        if py_component is not None:
            with ctx.create_synthetic_component(self) as subctx:
                # Write the component definition file, and put
                py_component.generate(subctx)
                # ...in the body of the component.
                return subctx.sources

        # Do the thing where you we find the right stuff from the frontend dir,
        # and then import it.
        return []

    def gen_instance(self) -> str:
        # Stuff with the attributes and other stuff from the component class.
        return ""

    def generate(self, ctx: BuildContext):
        ctx.ensure_imported_into_current(self.gen_sources(ctx))
        ctx.write_into_current(self.gen_instance())


class _Raw(Component):
    def __init__(self, react_code: str) -> None:
        super().__init__()
        self.react_code = react_code

    def gen_sources(self, ctx: BuildContext) -> List[str]:
        return []

    def gen_instance(self) -> str:
        return self.react_code


class WebPage(Component):
    content: Optional[Component]

    def __init__(self, title: str = "", is_homepage: bool = False) -> None:
        super().__init__()
        self.title = title
        self.is_homepage = is_homepage
        self.content = None

    def generate(self, ctx: BuildContext):
        if self.content is None:
            self.content = _Raw("<div></div>")
        # Make sure the actual component doesn't get written into its own
        # source file.
        self.content._embedded = True

        basename = "index" if self.is_homepage else slugify(self.title)
        extra_template_args = {
            # page stuff like the name, etc.
        }
        # TODO: Subpages / subdirectories
        with ctx.source_file(f"pages/{basename}.tsx", custom_template="page.tsx.jinja", custom_template_extras=extra_template_args):
            ctx.ensure_imported_into_current(
                self.content.gen_sources(ctx, embed=True))
            ctx.write_into_current(self.content.gen_instance())


class WebApp(object):
    _pages: List[WebPage]
    layout: Optional[Component]
    seo: SEO
    branding: Branding
    nav_links: List[Link]
    nav_actions: List[Link]

    def __init__(self, branding: Optional[Branding] = None, seo: Optional[SEO] = None) -> None:
        self._pages = []
        self.layout = None
        if not seo:
            self.seo = SEO(title="Web App")
        self.seo = seo
        if not branding:
            self.branding = DEFAULT_BRANDING
        else:
            self.branding = branding
        self.nav_links = []
        self.nav_actions = []

    def add_page(self, page: WebPage) -> None:
        self._pages.append(page)

    def generate(self) -> None:
        build_context = self._mkbuild()
        self._init_base_frontend(build_context)
        self._gen_app_skeleton(build_context)
        self._gen_pages(build_context)
        build_context.run_formatter()

    def _mkbuild(self) -> BuildContext:
        cwd = Path(".")
        output_dir = cwd / ".splashgen"
        os.makedirs(output_dir, exist_ok=True)
        return BuildContext(cwd, output_dir)

    def _init_base_frontend(self, ctx: BuildContext):
        # Copies tsconfig, package.json, package-lock.json, generates the
        # nextjs directory structure, e.g. pages/ and components/. Only if
        # necessary (e.g. the shasum changes). ctx.write_to_build(file, force=False)
        ctx.copy_from_frontend(
            'tsconfig.json',
            'package.json',
            'package-lock.json',
            'next-env.d.ts')
        ctx.mkdirs('pages', 'components', 'public')

        # Runs npm install if package.json shasum has changed
        ctx.run_installs_if_necessary()

        # If branding logo shasum has changed, places the logo in public/ and
        # converts it into a favicon (using whatever we need to use in order to
        # do that).
        logo = self.branding.logo or DEFAULT_BRANDING.logo
        written, logo_path = ctx.write_to_public(logo)
        if written:
            ctx.gen_favicon(logo_path)
        # NOTE: In the future if there is a frontend/ folder in an app
        # directory it should use things from there instead, vs. our own
        # front-end directory, although that might be problematic in terms of
        # library version compatibility so idk.

    def _gen_app_skeleton(self, ctx: BuildContext):
        """Based off the properties in the app, generates pages/_app.tsx."""
        ctx.copy_from_frontend("components/atoms/branding.tsx")
        with ctx.source_file('pages/_app.tsx', custom_template="app.tsx.jinja") as app_tsx:
            bs_mod = "bootstrap-dark-5/dist/css/bootstrap-night.min.css" \
                if self.branding.theme == "dark" \
                else "bootstrap/dist/css/bootstrap.min.css"
            app_tsx.add_imports(
                Import(None, bs_mod),
                Import("{ DefaultSeo }", "next-seo"),
                Import("type { AppProps }", "next/app"),
                Import("Head", "next/head"),
                Import("{ BrandingProvider }", "components/atoms/branding"),
            )

            self.layout.children = [
                _Raw("<Component {...pageProps} />")
            ]
            self.layout.generate(ctx)

    def _gen_pages(self, ctx: BuildContext):
        for page in self._pages:
            page.generate(ctx)
