from typing import Union
from xml.etree.ElementTree import Element

import parse_tei


def get_authors(tei_ele: Element):
    author_tag = parse_tei.make_tei_tag('author')
    authors = []
    for author in tei_ele.iter(author_tag):
        author_info = {}
        for child in author:
            tag = parse_tei.clean_tag(child.tag)
            if tag == 'persName':
                author_info['author_name'] = get_author_name(child)
            else:
                tag_info = {
                    'text': ' '.join([text for text in child.itertext()]),
                    'attrs': child.attrib
                }
                author_info[tag] = tag_info
        authors.append(author_info)
    return authors


def get_author_name(name_ele):
    return {parse_tei.clean_tag(child.tag): ' '.join([t for t in child.itertext()]) for child in name_ele}
def get_ref_id(bibl_struct: Element) -> str:
    id_tag = parse_tei.make_tei_tag('id')
    return bibl_struct.attrib[id_tag]


def get_ref_info(bibl_struct):
    analytic = get_analytic(bibl_struct)
    monogr = get_monogr(bibl_struct)
    return {'analytic': analytic, 'monogr': monogr}


def get_analytic(bibl_struct: Element):
    analytic = parse_tei.get_elements_by_tag(bibl_struct, 'analytic')[0]
    analytic_title = parse_tei.get_elements_by_tag(analytic, 'title')[0]
    analytic_info = {
        'id': get_ref_id(bibl_struct),
        'title': ' ---- '.join([text_string for text_string in analytic_title.itertext()]),
        'authors': get_authors(analytic),
        'doi': get_ref_idno(analytic)
    }
    return analytic_info


def get_monogr(bibl_struct: Element):
    monogr = parse_tei.get_elements_by_tag(bibl_struct, 'monogr')[0]
    monogr_info = {}
    for child in monogr:
        if parse_tei.has_tag(child, 'imprint'):
            monogr_info['imprint'] = get_imprint(child)
        else:
            tag = parse_tei.clean_tag(child.tag)
            tag_info = {
                'text': ' '.join([text for text in child.itertext()]),
                'attrs': child.attrib
            }
            monogr_info[tag] = tag_info
    return monogr_info


def get_imprint(bibl_struct: Element):
    imprint = parse_tei.get_elements_by_tag(bibl_struct, 'imprint')[0]
    imprint_info = {}
    for child in imprint:
        tag = parse_tei.clean_tag(child.tag)
        tag_info = {
            'text': ' '.join([text for text in child.itertext()]),
            'attrs': child.attrib
        }
        imprint_info[tag] = tag_info
    return imprint_info


def get_ref_idno(analytic: Element) -> Union[str, None]:
    idno = parse_tei.get_elements_by_tag(analytic, 'idno')
    if len(idno) == 0:
        return None
    else:
        return idno[0].text


