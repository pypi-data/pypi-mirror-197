from phml.core.nodes import *
from pytest import raises


def test_point():
    point = Point(1, 3)
    assert point.line == 1 and point.column == 3 and point.offset is None

    with raises(IndexError, match="Point.line must be >= 0 but was .+"):
        Point(-1, 0)

    with raises(IndexError, match="Point.column must be >= 0 but was .+"):
        Point(0, -1)

    with raises(IndexError, match="Point.offset must be >= 0 or None but was .+"):
        Point(0, 0, -1)

    assert Point(1, 3) == Point(1, 3)
    assert repr(Point(1,3)) == "point(line: 1, column: 3, offset: None)"

def test_position():
    position = Position(Point(1, 2), Point(3, 4))
    assert (
        (position.start.line == 1 and position.start.column == 2)
        and (position.end.line == 3 and position.end.column == 4)
        and position.indent is None
    )

    with raises(IndexError, match="Position.indent value must be >= 0 or None but was .+"):
        Position(Point(1, 2), Point(3, 4), -1)
        
    assert Position(Point(1, 2), Point(3, 4)) == Position(Point(1, 2), Point(3, 4))
    assert Position(Point(1, 2), Point(3, 4)) == Position((1, 2), (3, 4))

def test_ast():
    with raises(
        TypeError, match="The given tree/root node for AST must be of type `Root` or `Element`"
    ):
        AST(None)
    with raises(
        TypeError, match="The given tree/root node for AST must be of type `Root` or `Element`"
    ):
        AST("Something")
    with raises(
        TypeError, match="The given tree/root node for AST must be of type `Root` or `Element`"
    ):
        AST(Text("test"))

    ast = AST(Root(children=[Element("div", startend=True)]))
    for anode, cnode in zip(
        ast, [Root(children=[Element("div", startend=True)]), Element("div", startend=True)]
    ):
        assert anode == cnode

    assert not ast == Element("div")

    assert ast.size == 2

    assert ast.children == ast.tree.children


def test_root():
    root = Root()
    assert root.parent is None and root.position is None and len(root.children) == 0
    assert repr(root) == "root [0]"


def test_element():
    element = Element()
    assert (
        element.tag == "element"
        and element.properties == {}
        and element.parent is None
        and element.position is None
        and element.startend is False
        and len(element.children) == 0
    )

    element = Element("div", {"id": "test"})
    assert element.start_tag() == '<div id="test">' and element.end_tag() == "</div>"
    
    world = Text("world")
    element.append(world)
    assert element.children == [world]
    element.insert(0, Text("hello"))
    assert element.children == [Text("hello"), world]
    element.remove(world)
    assert element.children == [Text("hello")]

    element = Element("input", {"type": "checkbox"}, startend=True)
    assert element.start_tag() == '<input type="checkbox" />' and element.end_tag() is None

    element["type"] = "number"
    assert element.properties["type"] == "number"

    assert element["type"] == "number"

    del element["type"]
    assert "type" not in element.properties

    with raises(TypeError, match="Index must be a str and value must be either str or bool."):
        element[3] = "The"
    with raises(TypeError, match="Index must be a str and value must be either str or bool."):
        element["type"] = 4


def test_doctype():
    doctype = DocType()
    assert doctype.parent is None and doctype.position is None and doctype.lang == "html"

    assert doctype.stringify() == "<!DOCTYPE html>"

    assert doctype is not None

    assert repr(doctype) == "node.doctype(html)"
    
    assert not doctype == Text("test")


def test_text():
    text = Text()
    assert text.value == "" and text.position is None and text.parent is None

    text = Text("Sample")
    assert text.stringify() == "Sample" and text.stringify(2) == "  Sample"
    assert repr(text) == "literal.text('Sample')"

    raw = """\
multiline
text\
"""
    rendered = """\
  multiline
  text\
"""
    text = Text(raw)
    assert text.stringify() == raw and text.stringify(2) == rendered


def test_comment():
    comment = Comment()
    assert comment.value == "" and comment.position is None and comment.parent is None

    comment = Comment("Sample")
    assert comment.stringify() == "<!--Sample-->" and comment.stringify(2) == "  <!--Sample-->"
    assert repr(comment) == "literal.comment(value: Sample)"
    raw = """\
<!--multiline
text-->\
"""
    rendered = """\
  <!--multiline
  text-->\
"""
    comment = Comment(
        """\
multiline
text\
"""
    )
    assert comment.stringify() == raw and comment.stringify(2) == rendered

    comment = Comment(
        """\
 multiline
with more than
two lines \
"""
    )

    assert (
        comment.stringify()
        == """\
<!-- multiline
with more than
two lines -->\
"""
    )
