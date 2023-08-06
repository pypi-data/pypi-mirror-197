# VirtualPython
# get_vp_result
# process_vp_blocks

from phml.core.virtual_python.import_objects import ImportFrom, Import
from phml.core.virtual_python import VirtualPython, get_python_result, process_python_blocks


def test_import_objects():
    imp = Import(["pprint, phml"])
    assert repr(imp) == "Import(modules=[pprint, phml])"
    assert str(imp) == "import pprint, phml"

    imp = ImportFrom("phml", ["inspect", "classnames"])
    assert repr(imp) == "ImportFrom(module='phml', names=[inspect, classnames])"
    assert str(imp) == "from phml import inspect, classnames"


def test_virtual_python():
    vp = VirtualPython("import phml\nmessage='dog'")
    assert repr(vp) == "VP(imports: 1, locals: 2)"


def test_get_vp_result():
    result = get_python_result("message='2'\nresult=message")
    assert result == "2"
    result = get_python_result(
        """\
message = ['2', 3]
(void, invalid) = (None, "RED ALERT")
results=message\
"""
    )
    assert result == ['2', 3]

    assert get_python_result("cow") is None
    assert get_python_result("cow\nresult=dog") is None

    get_python_result("invalid('call')", cat=None)


def test_process_vp_blocks():
    vp = VirtualPython()
    result = process_python_blocks("The {thing} has a {desc}.", vp, thing="cat", desc="big heart")
    assert result == "The cat has a big heart."
    result = process_python_blocks("The {thing} has a {desc}.", vp, thing="cat", desc="big heart")
    assert result == "The cat has a big heart."


if __name__ == "__main__":
    test_process_vp_blocks()
