# coding=utf-8

import pprint

from ka_uta.ka_json import Json


class Arr:
    """ io for Array
    """
    @staticmethod
    def write(arr: list, path: str) -> None:
        with open(path, 'wt') as fd:
            string = '\n'.join(arr)
            fd.write(string)


class XmlStr:
    """ io for Xml String
    """
    @staticmethod
    def write(xmlstr: str, path: str) -> None:
        with open(path, 'w') as fd:
            fd.write(xmlstr)


class Dic:
    """ io for Dictionary
    """
    class Txt:
        @staticmethod
        def write(dic: dict, path_: str, indent: int = 2) -> None:
            data = pprint.pformat(dic, indent=indent)
            with open(path_, 'w') as fd:
                fd.write(data)

    class Json:
        @staticmethod
        def write(dic: dict, path_: str, indent: int = 2) -> None:
            Json.write(dic, path_, indent=indent)
