# encoding: utf-8

"""
General purpose functions that raise the abstraction level of interacting with
objectify elements.
"""

from __future__ import absolute_import

from lxml import objectify

from pptx.oxml.ns import NamespacePrefixedTag, qn


def child(element, child_tag_str):
    """
    Return direct child of *element* having tag matching *child_tag_str* or
    |None| if no such child element is present.
    """
    nsptag = NamespacePrefixedTag(child_tag_str)
    xpath = './%s' % child_tag_str
    matching_children = element.xpath(xpath, namespaces=nsptag.nsmap)
    return matching_children[0] if len(matching_children) else None


def get_or_add(start_elm, *path_tags):
    """
    Retrieve the element at the end of the branch starting at parent and
    traversing each of *path_tags* in order, creating any elements not found
    along the way. Not a good solution when sequence of added children is
    likely to be a concern.
    """
    parent = start_elm
    for tag in path_tags:
        child_ = child(parent, tag)
        if child_ is None:
            child_ = SubElement(parent, tag)
        parent = child_
    return child_


def SubElement(parent, tag):
    nsptag = NamespacePrefixedTag(tag)
    return objectify.SubElement(parent, nsptag.clark_name, nsmap=nsptag.nsmap)


def sub_elm(parent, tag, **extra):
    return objectify.SubElement(parent, qn(tag), **extra)
