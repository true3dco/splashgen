import sys
import os
import importlib
import splashgen


# See: https://github.com/pallets/flask/blob/9039534eee6a87da98a1dee9e4338d1b73e861f8/src/flask/cli.py#L223
def prepare_import(path):
    path = os.path.realpath(path)
    fname, ext = os.path.splitext(path)
    if ext == ".py":
        path = fname

    if os.path.basename(path) == "__init__":
        path = os.path.dirname(path)

    module_name = []

    # move up until outside package structure (no __init__.py)
    while True:
        path, name = os.path.split(path)
        module_name.append(name)

        if not os.path.exists(os.path.join(path, "__init__.py")):
            break

    if sys.path[0] != path:
        sys.path.insert(0, path)

    return ".".join(module_name[::-1])


def main():
    if len(sys.argv) < 2:
        raise ValueError("Missing file arg")

    mod = prepare_import(sys.argv[-1])
    importlib.import_module(mod)
    if splashgen._assigned_component is None:
        raise RuntimeError("launch() was never called. Make sure to call "
                           "launch() with your splash site!")

    index = splashgen._assigned_component.render()
    with open(os.path.join(splashgen._assigned_component.build_dir, 'index.html'), 'w') as indexf:
        indexf.write(index)


if __name__ == "__main__":
    main()
