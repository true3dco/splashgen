import inspect
import json
import dataclasses
from typing import Any, List

import humps
from splashgen.core import BuildContext


def _try_stringify_prop_value(value: Any, ctx: BuildContext) -> str:
    # TODO: There's probably a much better way to do this
    valtype = type(value)
    if valtype is str:
        return json.dumps(value)
    if valtype in (int, float, bool, type(None)):
        return f"{{{json.dumps(value)}}}"
    if valtype in (tuple, list):
        sub_stringifications = [_try_stringify_prop_value(v) for v in value]
        valid_subs = [ss for ss in sub_stringifications if ss is not None]
        return f"{{[{', '.join(valid_subs)}]}}"
    if valtype is dict:
        copy = dict(value)
        for k in copy.keys():
            conv = _try_stringify_prop_value(copy[k])
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
            conv = _try_stringify_prop_value(datadict[k])
            if conv is not None:
                del datadict[k]
            else:
                datadict[k] = conv
        # We do *not* have to quote properties here
        obj_props = [f'{k}: {v}' for (k, v) in datadict.items()]
        return f"{{{{{', '.join(obj_props)}}}}}"
    if isinstance(value, Component):
        return value.generate(ctx)

    raise NotImplementedError(
        f"Value of type {valtype} cannot be converted to a prop")


class Component(object):
    """The core class for all splashgen components"""

    def render(self) -> 'Component':
        """Create an instance of a component by composing other components.

        Override this in a subclass in order to create components from those
        which already exist.
        """
        return None

    def find_sources(self) -> List[str]:
        """Gather source files associated with the component.

        If render isn't overridden, this will be used instead.
        """
        component_name = self.__class__.__name__
        extensions = [".js", ".jsx", ".ts", ".tsx", ".css", ".scss"]
        # CONTINUE HERE, OR JUST PASS __file__ into __init__()
        dir_path = somehow_find_file_of_calling_class
        glob_the_dir_path
        return_the_right_shit

    def gen_sources(self, ctx: BuildContext) -> List[str]:
        # TODO: Either render() or find_sources() or err if nothing there.
        # Somehow need to get imports from component file!
        pass

    def gen_instance(self, ctx: BuildContext) -> str:
        component_name = self.__class__.__name__
        props_string = self._gen_props_string(ctx)
        s = f"<{component_name} {props_string}"
        if self.children:
            with ctx.indented_region():
                s += ">\n"
                for child in self.children:
                    s += f"{ctx.indent}{child.gen_instance(ctx)}"
        else:
            s += "/>"

    def generate(self, ctx: BuildContext) -> str:
        sources = self.gen_sources(ctx)
        ctx.add_to_build(sources)
        return self.gen_instance(ctx)

    def _gen_props_string(self, ctx: BuildContext):
        ctor_arg_spec = inspect.getfullargspec(self.__class__.__init__)
        ctor_args_without_self = ctor_arg_spec.args[1:]
        prop_strings = []
        for arg_name in ctor_args_without_self:
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
