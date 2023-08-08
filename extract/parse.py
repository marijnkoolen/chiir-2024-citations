from xml.etree.ElementTree import Element

import parse_tei
from parse_bibl_data import get_ref_info
from parse_text import parse_paragraphs


def get_references(root: Element):
    refs = {}
    list_bibl = parse_tei.get_element_by_tag(root, 'listBibl')
    for bibl_struct in parse_tei.get_elements_by_tag(list_bibl, 'biblStruct'):
        ref = get_ref_info(bibl_struct)
        refs[ref['analytic']['id']] = ref
    return refs


def get_citations(root: Element):
    paragraphs = parse_paragraphs(root)
    citations = []
    return citations
