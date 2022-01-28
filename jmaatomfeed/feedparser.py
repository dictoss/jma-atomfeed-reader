#!/usr/bin/python3
#
# Atom Feed XML reader for JMA library.
#
import logging
import xml.etree.ElementTree as ET

# dependency libraries.
import requests

g_logger = logging.getLogger(__name__)


class JmaAtomFeedParser(object):
    XML_NS_KEY = 'jmaatomfeed'
    XML_NS_NAME = 'http://www.w3.org/2005/Atom'
    XML_NS_DICT = {XML_NS_KEY: XML_NS_NAME}

    def __init__(self, timeout=(10.0, 60.0)):
        self.download_timeout = timeout
        self.data_raw = None

        # python object's XML extracted.
        self.xml_title = None
        self.xml_subtitle = None
        self.xml_updated = None
        self.xml_id = None
        self.xml_links = None
        self.xml_rights = None
        self.xml_entry_list = None

    def download(self, url_or_path):
        _xmldata = None
        _response = None

        if not url_or_path:
            raise ValueError('url_or_path is empty.')

        try:
            if url_or_path.startswith('http'):
                _response = requests.get(
                    url_or_path,
                    timeout=self.download_timeout)
                if 200 <= _response.status_code <= 299:
                    # convert str.
                    _xmldata = _response.content.decode('utf-8')
            else:
                with open(url_or_path, 'r', encoding='utf-8') as f:
                    _xmldata = f.read()
        except Exception as e:
            g_logger.error('EXCEPT: %s', e)
            _xmldata = None

        return _xmldata

    def loads(self, data):
        def ET_find_helper(node, key):
            return node.find(
                '{}:{}'.format(self.XML_NS_KEY, key),
                namespaces=self.XML_NS_DICT)

        def ET_findall_helper(node, key):
            return node.findall(
                '{}:{}'.format(self.XML_NS_KEY, key),
                namespaces=self.XML_NS_DICT)

        self.data_raw = data
        _root = ET.fromstring(data)

        # pickup line header data.
        self.xml_title = ET_find_helper(_root, 'title').text
        self.xml_subtitle = ET_find_helper(_root, 'subtitle').text
        self.xml_updated = ET_find_helper(_root, 'updated').text
        self.xml_id = ET_find_helper(_root, 'id').text

        # pickup <link> tags.
        # self.xml_links = []

        # pickup <entry> tag.
        # self.xml_rights = ''

        # pickup <entry> tags.
        _entries = []
        for e in ET_findall_helper(_root, 'entry'):
            _author = ET_find_helper(e, 'author')

            _obj = {
                'title': ET_find_helper(e, 'title').text,
                'id': ET_find_helper(e, 'id').text,
                'updated': ET_find_helper(e, 'updated').text,
                'auther': ET_find_helper(_author, 'name').text,
                'link_mime': ET_find_helper(e, 'link').text,
                'link_url': ET_find_helper(e, 'link').text,
                'content': ET_find_helper(e, 'content').text,
            }
            _entries.append(_obj)

        self.xml_entry_list = _entries

    def get_title(self):
        return self.xml_title

    def get_subtitle(self):
        return self.xml_subtitle

    def get_updated(self):
        return self.xml_updated

    def get_id(self):
        return self.xml_id

    def get_rights(self):
        return self.xml_rights

    def get_entry_list(self):
        return self.xml_entry_list


if __name__ == '__main__':
    pass
