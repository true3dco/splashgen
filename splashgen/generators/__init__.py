import dataclasses
import hashlib
import inspect
import json
import os
import shutil
import subprocess
from contextlib import contextmanager
from os import PathLike, path
from pathlib import Path
from typing import (Any, ContextManager, Dict, List, NamedTuple, Optional, Set, TextIO,
                    Tuple)

import humps
from jinja2 import Environment, PackageLoader
from splashgen.site_config import DEFAULT_BRANDING, SEO, Branding, Link

_jinja = Environment(loader=PackageLoader(
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

    def __hash__(self) -> int:
        return hash(str(self))

    def __eq__(self, o: object) -> bool:
        return str(self) == str(o)


class SourceFile(object):
    imports: Set[Import]
    _code: str
    _template: str
    _jinja = _jinja

    def __init__(self,
                 output_path: str,
                 custom_template: Optional[str] = None,
                 custom_template_extras: Optional[str] = None) -> None:
        self.output_path = output_path
        self.imports = set()
        self._code = ""
        self._template = custom_template or "source_file.tsx.jinja"
        self._custom_template_extras = custom_template_extras or {}

    def close(self):
        with open(self.output_path, 'w') as out_file:
            self._render_into(out_file)

    def add_imports(self, *imports: Import) -> None:
        for import_ in imports:
            self.add_import(import_)

    def add_import(self, import_: Import) -> None:
        self.imports.add(import_)

    def add_code(self, code: str) -> None:
        self._code += code

    def _render_into(self, out_file: TextIO) -> None:
        tmpl = self._jinja.get_template(self._template)
        context = {
            "imports": self.imports,
            "code": self._code,
            **self._custom_template_extras
        }
        source = tmpl.render(context)
        out_file.write(source)


# NOTE: In the future, this could be a frontend/ dir that's in the codebase's
# repo
_FRONTEND_DIR = (Path(path.dirname(__file__)) / '..' / 'frontend').resolve()


class BuildContext(object):
    _source_stack: List[SourceFile]
    _component_paths: Dict[Any, str]

    def __init__(self, source_dir: Path, build_dir: Path) -> None:
        self.source_dir = source_dir
        self.build_dir = build_dir
        self.cache_dir = self.build_dir / "sg-buildcache"
        self.tmp_dir = self.build_dir / "sg-temp"
        self._source_stack = []
        self._component_paths = {}

        for dirname in (self.cache_dir, self.tmp_dir):
            os.makedirs(dirname, exist_ok=True)

    def copy_from_frontend(self, *sources: PathLike) -> None:
        for source in sources:
            source_path = _FRONTEND_DIR / source
            if not source_path.exists():
                raise IOError(f"Could not find source {source}")
            dest_path = self.build_dir / source
            os.makedirs(path.dirname(dest_path), exist_ok=True)
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

    @contextmanager
    def source_file(self, rel_path: PathLike, **kwargs) -> ContextManager[SourceFile]:
        source = SourceFile(self.build_dir / rel_path, **kwargs)
        self._source_stack.append(source)
        try:
            yield source
        finally:
            source.close()
            self._source_stack.pop()

    def ensure_imported_into_current(self, component: 'Component') -> None:
        if isinstance(component, _Raw):
            # We treat raw special and just pass through its output.
            return

        current = self._current_source()
        component_import = self._get_or_generate_import_for_current(component)
        if component_import not in current.imports:
            current.add_import(component_import)

    def write_into_current(self, code: str) -> str:
        self._current_source().add_code(code)

    def _get_or_generate_import_for_current(self, component: 'Component') -> Import:
        cmp_cls = type(component)
        if cmp_cls in self._component_paths:
            cmp_path = self._component_paths[cmp_cls]
        else:
            # gen_source needs to generate sources for any components that it
            # uses...we can do this by parsing the component itself
            cmp_path = self._gen_component_source(component)
            self._component_paths[cmp_cls] = cmp_path

        rel_mod_path = self._resolve_path_with_current(cmp_path)
        return Import(cmp_cls.__name__, rel_mod_path)

    def _resolve_path_with_current(self, cmp_path: str) -> str:
        """Figures out the right import path from the current file"""
        current = self._current_source()
        current_dir_relpath = path.relpath(
            path.dirname(current.output_path), self.build_dir)
        relpath = path.relpath(cmp_path, current_dir_relpath)
        if not relpath.startswith('.'):
            # It's in the same directory and we have to add the ./
            relpath = f"./{relpath}"
        return relpath

    def _gen_component_source(self, component: 'Component') -> str:
        """Returns the relative path in the build to the component"""
        if isinstance(component, WebPage):
            raise NotImplementedError("Can't do pages yet!")

        needs_transpile = component.render() is not None
        if needs_transpile:
            raise NotImplementedError("Transpilation coming soon")

        return self._gen_sources_from_frontend(component)

    def _gen_sources_from_frontend(self, component: 'Component') -> str:
        # Do the thing where you we find the right stuff from the frontend dir,
        # and then import it.
        class_file = inspect.getfile(type(component))
        component_name = type(component).__name__
        # Chop off all the parts until you come across a directory called components/
        component_dir_parts = Path(path.dirname(class_file)).parts
        rel_idx = -1
        # TODO: This won't work for pages, sooo, do something different
        for idx, part in enumerate(component_dir_parts):
            if part == 'components':
                rel_idx = idx
                break
        if rel_idx < 0:
            raise RuntimeError("Component defined outside components/ dir")
        rel_component_dir = path.join(
            *component_dir_parts[rel_idx:])
        frontend_component_dir = _FRONTEND_DIR / rel_component_dir
        files = list(frontend_component_dir.glob(f"{component_name}*"))
        if not files:
            raise RuntimeError(
                f"Could not find any sources to generate component {component_name}")
        cmp_path = None
        for file in files:
            rel_path = path.relpath(file, _FRONTEND_DIR)
            dest_path = self.build_dir / rel_path
            os.makedirs(path.dirname(dest_path), exist_ok=True)
            shutil.copyfile(file, dest_path)

            maybe_cmp_path, ext = path.splitext(rel_path)
            if ext in ['.js', '.jsx', '.tsx']:
                cmp_path = maybe_cmp_path

        if cmp_path is None:
            raise RuntimeError(
                f"Could not find js/jsx/tsx for {component_name}")
        return cmp_path

    def _current_source(self) -> SourceFile:
        if not self._source_stack:
            raise IndexError("There are no sources")
        return self._source_stack[-1]

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


def _try_stringify_prop_value(value: Any, ctx: BuildContext) -> str:
    # TODO: There's probably a much better way to do this
    valtype = type(value)
    if valtype is str:
        return json.dumps(value)
    if valtype in (int, float, bool, type(None)):
        return f"{{{json.dumps(value)}}}"
    if valtype in (tuple, list):
        sub_stringifications = [
            _try_stringify_prop_value(v, ctx) for v in value]
        valid_subs = [ss for ss in sub_stringifications if ss is not None]
        return f"{{[{', '.join(valid_subs)}]}}"
    if valtype is dict:
        copy = dict(value)
        for k in copy.keys():
            conv = _try_stringify_prop_value(copy[k], ctx)
            if conv is not None:
                del copy[k]
            else:
                copy[k] = conv
        # We have to quote properties as they may be any string
        obj_props = [f'"{k}": {v}' for (k, v) in copy.items()]
        return f"{{{{{', '.join(obj_props)}}}}}"
    if dataclasses.is_dataclass(value):
        datadict = humps.camelize(dataclasses.asdict(value))
        for k in datadict.keys():
            conv = _try_stringify_prop_value(datadict[k], ctx)
            if conv is not None:
                del datadict[k]
            else:
                datadict[k] = conv
        # We do *not* have to quote properties here
        obj_props = [f'{k}: {v}' for (k, v) in datadict.items()]
        return f"{{{{{', '.join(obj_props)}}}}}"
    if isinstance(value, Component):
        # Dunno if this works...
        return value.gen_instance(ctx)

    raise NotImplementedError(
        f"Value of type {valtype} cannot be converted to a prop")


class Component(object):
    def render(self) -> Optional['Component']:
        return None

    def gen_sources(self, ctx: BuildContext) -> List[str]:
        py_component = self.render()
        if py_component is not None:
            self._process_py_component(py_component)

    def gen_instance(self, ctx: BuildContext) -> str:
        component_name = type(self).__name__
        props_string = self._gen_props_string(ctx)
        s = f"<{component_name} {props_string}"
        if hasattr(self, 'children'):
            s += ">\n"
            for child in getattr(self, 'children'):
                s += child.gen_instance(ctx)
            s += f"</{component_name}>"
        else:
            s += "/>"
        return s

    def generate(self, ctx: BuildContext):
        ctx.ensure_imported_into_current(self)
        ctx.write_into_current(self.gen_instance(ctx))

    def _gen_props_string(self, ctx: BuildContext):
        ctor_arg_spec = inspect.getfullargspec(type(self).__init__)
        ctor_args_without_self = ctor_arg_spec.args[1:]
        prop_strings = []
        for arg_name in ctor_args_without_self:
            if arg_name == "children":
                # We treat children special. Pass.
                continue

            has_matching_attribute = hasattr(self, arg_name)
            if not has_matching_attribute:
                continue

            arg_attr_value = getattr(self, arg_name)
            stringified_value = _try_stringify_prop_value(arg_attr_value, ctx)
            if stringified_value:
                prop_name = humps.camelize(arg_name)
                prop_string = f"{prop_name}={stringified_value}"
                prop_strings.append(prop_string)

        return " ".join(prop_strings)


class _Raw(Component):
    def __init__(self, react_code: str) -> None:
        super().__init__()
        self.react_code = react_code

    def gen_sources(self, ctx: BuildContext) -> List[str]:
        return []

    def gen_instance(self, ctx: BuildContext) -> str:
        return self.react_code


class WebPage(Component):
    content: Optional[Component]

    def __init__(self, title: str = "", is_homepage: bool = False) -> None:
        super().__init__()
        self.title = title
        self.is_homepage = is_homepage
        self.content = None

    def generate(self, ctx: BuildContext):
        raise NotImplementedError
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
        # TODO: Figure out how to split up data, etc, for pages
        with ctx.source_file(f"pages/{basename}.tsx", custom_template="page.tsx.jinja", custom_template_extras=extra_template_args):
            pass


class WebApp(object):
    _pages: List[WebPage]
    layout: Optional[Component]
    seo: SEO
    branding: Branding
    nav_links: List[Link]
    nav_actions: List[Link]

    def __init__(self, branding: Optional[Branding] = None, seo: Optional[SEO] = None) -> None:
        self._pages = []
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
        # TODO: Dedupe from above
        _, logo_path = ctx.write_to_public(
            self.branding.logo or DEFAULT_BRANDING.logo)
        custom_template_extras = {
            "branding": self.branding,
            "seo": self.seo,
            "logo_path": f"/{path.basename(logo_path)}"
        }
        with ctx.source_file('pages/_app.tsx',
                             custom_template="app.tsx.jinja",
                             custom_template_extras=custom_template_extras):
            self.layout.children = [
                _Raw("<Component {...pageProps} />")
            ]
            self.layout.generate(ctx)

    def _gen_pages(self, ctx: BuildContext):
        for page in self._pages:
            page.generate(ctx)
