# coding=utf-8
"""Koskya Utilities Module
contains the Kosakya Utilitiy Classes
"""

import os
import pprint

from ka_utg.dod import DoD as KaDoD
from ka_utg.file import File as KaFile

from ka_uta.ka_xml import Xml2Dic
from ka_uta.ka_json import Json


class Path:

    @classmethod
    def sh_file_paths(cls, path):
        paths = []
        for entry in cls.scantree(path):
            paths.append(entry.path)
        return paths

    @classmethod
    def scantree(cls, path):
        """Recursively yield DirEntry objects for given directory."""
        for entry in os.scandir(path):
            if entry.is_dir(follow_symlinks=False):
                yield from cls.scantree(entry.path)
            else:
                yield entry

    @classmethod
    def sh_file_paths_by_ext(cls, path, ext):
        paths = []
        for entry in cls.scantree(path):
            if entry.name.endswith(ext):
                paths.append(entry.path)
        return paths

    @staticmethod
    def mkdir(path):
        try:
            if path is None:
                return
            dir = os.path.dirname(path)
            if not os.path.isdir(dir):
                os.makedirs(dir)
                # msg = f"Directory {dir} Created"
        except Exception as e:
            raise e

    @staticmethod
    def get(path, prefix=None):
        try:
            if not path:
                if not prefix:
                    return prefix
                return os.path.expanduser(prefix)
            path = os.path.expanduser(path)
            if not os.path.isabs(path):
                if prefix:
                    return os.path.join(prefix, path)
            return path
        except Exception as e:
            raise e

    @classmethod
    def read(cls, path, prefix=None):
        return KaFile.read(cls.get(path, prefix))

    @classmethod
    def read_2str(cls, path, mode='rb'):
        """ binary read file path into string
        """
        with open(path, mode) as fd:
            str_binary = fd.read()
        return str_binary

    def read_xml2dic(path, **kwargs):
        mode = kwargs.get('mode', 'rb')
        with open(path, mode) as fd:
            data = fd.read()
            dic = Xml2Dic.mig(data, **kwargs)
            return dic

    @classmethod
    def read_2dic(cls, path, fmt, **kwargs):
        if fmt == "xml":
            return cls.read_xml2dic(path, **kwargs)
        elif fmt == "json":
            return Json.read(path, json='ojson', **kwargs)
        return None

    @classmethod
    def write_dic(cls, dic, path, fmt, indent=2):
        if fmt == "txt":
            data = pprint.pformat(dic, indent=indent)
        elif fmt == "json":
            data = Json.dumps(dic, json='ujson', indent=indent)
        with open(path, 'w') as fd:
            fd.write(data)


class Paths:

    @staticmethod
    def get(paths=None, keys=None, prefix=None):
        """get path from nested dictionary of paths
        get the path from the nested path dictionary by looping through
        the keys list and recursively locating the dictionary value
        for every key

        Args:
            paths (dict): dictionary of paths
            keys (list): array of keys
            path_prefix (str): path prefix
        Returns:
            path (str): path
        """
        return Path.get(KaDoD.get_item_(paths, keys), prefix)

    @classmethod
    def read(cls, paths=None, keys=None, prefix=None, sw_warning=False):
        """get path from nested dictionary of paths and read path

        Args:
            paths (dict): dictionary of paths
            keys (list): array of keys
            path_prefix (str): path prefix
        Returns:
            (list): File content
        """
        return KaFile.read(cls.get(paths, keys, prefix), sw_warning)
