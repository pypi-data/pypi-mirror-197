import pathlib
def find_ROOT_dir():
    ROOT_dir = pathlib.__file__
    ROOT_dir = ROOT_dir.replace("\\", "/")
    ROOT_dir = "/".join(ROOT_dir.split("/")[:-1]) + "/site-packages/latlong"
    print(ROOT_dir)
    return ROOT_dir