"""phml.utilities.builder

This module serves as a utility to make building elements and ast's easier.
"""

from __future__ import annotations

from typing import Optional

from phml.core.nodes import NODE, Comment, DocType, Element, Root, Text

__all__ = ["p"]


def __process_children(node, children: list[str | list | int | NODE]):
    for child in children:
        if isinstance(child, str):
            node.children.append(Text(child, node))
        elif isinstance(child, (float, int)):
            node.children.append(Text(str(child), node))
        elif isinstance(child, NODE):
            child.parent = node
            node.children.append(child)
        elif isinstance(child, list):
            for nested_child in child:
                if isinstance(nested_child, str):
                    node.children.append(Text(nested_child, node))
                elif isinstance(nested_child, (float, int)):
                    node.children.append(Text(str(nested_child), node))
                elif isinstance(nested_child, NODE):
                    nested_child.parent = node
                    node.children.append(nested_child)
                else:
                    raise TypeError(
                        f"Unkown type <{type(nested_child).__name__}> in {child}:\
 {nested_child}"
                    )


def p(  # pylint: disable=[invalid-name,keyword-arg-before-vararg]
    selector: Optional[str] = None,
    *args: str | list | dict | int | NODE,
):
    """Generic factory for creating phml nodes."""

    # Get all children | non dict objects
    children = [child for child in args if isinstance(child, (str, list, int, NODE))]

    # Get all properties | dict objects
    props = [prop for prop in args if isinstance(prop, dict)]

    if selector is not None:
        # Is a comment
        if isinstance(selector, str) and selector.startswith("<!--"):
            return Comment(selector.replace("<!--", "").replace("-->", ""))

        # Is a text node
        if (
            isinstance(selector, str)
            and (len(selector.split(" ")) > 1 or len(selector.split("\n")) > 1)
            and len(args) == 0
        ):
            return Text(selector)

        if not isinstance(selector, str):
            args = [selector, *args]
            selector = None

            children = [child for child in args if isinstance(child, (str, list, int, NODE))]
            return parse_root(children)
        return parse_node(selector, props, children)

    return parse_root(children)


def parse_root(children: list):
    """From the given information return a built root node."""

    node = Root()
    __process_children(node, children)
    return node


def parse_node(selector: str, props: dict, children: list):
    """From the provided selector, props, and children build an element node."""
    from phml.utilities import parse_specifiers  # pylint: disable=import-outside-toplevel

    node = parse_specifiers(selector)
    if not isinstance(node[0], dict) or len(node[0]["attributes"]) > 0:
        raise TypeError("Selector must be of the format `tag?[#id]?[.classes...]?`")

    node = node[0]

    node["tag"] = "div" if node["tag"] == "*" else node["tag"]

    if node["tag"].lower() == "doctype":
        str_children = [child for child in children if isinstance(child, str)]
        if len(str_children) > 0:
            return DocType(str_children[0])
        return DocType()

    if node["tag"].lower().strip() == "text":
        return Text(
            " ".join([str(child) for child in children if isinstance(child, (str, int, float))])
        )

    if node["tag"].lower().strip() == "comment":
        return Comment(
            " ".join([str(child) for child in children if isinstance(child, (str, int, float))])
        )

    properties = {}
    for prop in props:
        properties.update(prop)

    if len(node["classList"]) > 0:
        properties["class"] = "" if "class" not in properties else properties["class"]
        properties["class"] += " ".join(node["classList"])
    if node["id"] is not None:
        properties["id"] = node["id"]

    element = Element(
        node["tag"],
        properties=properties,
        startend=len(children) == 0,
    )

    __process_children(element, children)
    return element
