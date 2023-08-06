from deprecated import deprecated

from drb.core.path import ParsedPath
from drb.core.node import DrbNode
from drb.core.factory import DrbFactory
from drb.nodes.abstract_node import AbstractNode
from drb.exceptions.core import DrbException, DrbNotImplementationException
from drb.exceptions.file import DrbFileNodeFactoryException
from urllib.parse import urlparse
from typing import Any, List, Optional

import io
import os
import platform
import pathlib
import re
import stat
import drb.topics.resolver as resolver


def is_hidden(path: str) -> bool:
    """
    Check if the associated file of the given path is hidden.
    :param path: file path to check
    :return: True if the file of the corresponding path is hidden
    :rtype: bool
    """
    # os_type = 'Linux' | 'Windows' | 'Java'
    os_type = platform.uname()[0]
    if os_type == 'Windows':
        return bool(os.stat(path).st_file_attributes &
                    stat.FILE_ATTRIBUTE_HIDDEN)
    return os.path.basename(path).startswith('.')


def impl_stream(path: str) -> io.FileIO:
    return io.FileIO(path, 'r+')


def impl_buffered_stream(path: str) -> io.BufferedReader:
    return io.BufferedReader(impl_stream(path))


class DrbFileNode(AbstractNode):
    """
    Parameters:
        path (Union[str, ParsedPath]): The path of the file
                                       to read with this node.
        parent (DrbNode): The parent of this node (default: None)
    """
    __attributes = [
        'directory', 'size', 'modified', 'readable', 'writable', 'hidden']

    def __init__(self, path, parent: DrbNode = None):
        super().__init__()
        if isinstance(path, ParsedPath):
            self._path = path
        else:
            if platform.uname()[0] == 'Windows':
                path = pathlib.Path(path).as_posix()
            self._path = ParsedPath(os.path.abspath(path))
        self.parent: DrbNode = parent
        self.__init_attr()
        self._available_impl.append(io.RawIOBase)
        self.name = self._path.filename
        self._children: List[DrbNode] = None

    @property
    def path(self) -> ParsedPath:
        return self._path

    def __init_attr(self):
        file_stat = os.stat(self.path.path)

        self @= (self.__attributes[0], os.path.isdir(self.path.path))

        self @= (self.__attributes[1], file_stat.st_size)

        self @= (self.__attributes[2], file_stat.st_mtime)

        self @= (self.__attributes[3], os.access(self.path.path, os.R_OK))

        self @= (self.__attributes[4], os.access(self.path.path, os.W_OK))

        self @= (self.__attributes[5], is_hidden(self.path.path))

    @property
    @resolver.resolve_children
    @deprecated(version='2.1.0', reason='Only bracket browse should be use')
    def children(self) -> List[DrbNode]:
        if self._children is None:
            self._children = []
            if os.path.isdir(self.path.path):
                sorted_child_names = sorted(os.listdir(self.path.path))
                for filename in sorted_child_names:
                    child = DrbFileNode(self.path / filename, parent=self)
                    self._children.append(child)
        return self._children

    def get_impl(self, impl: type, **kwargs) -> Any:
        if issubclass(impl, io.RawIOBase):
            return impl_stream(self.path.path)
        if issubclass(impl, io.BufferedIOBase):
            return impl_buffered_stream(self.path.path)
        raise DrbNotImplementationException(
            f'no {impl} implementation found')

    def close(self) -> None:
        """
        Not use in this implementation.

        Returns:
            None
        """
        pass


class DrbFileFactory(DrbFactory):

    @staticmethod
    def _create_from_uri_of_node(node: DrbNode):
        uri = node.path.name
        parsed_uri = urlparse(uri)
        if (platform.uname()[0] == "Windows"
                and re.match(r"^/[a-zA-Z]:", parsed_uri.path)):
            path = parsed_uri.path[:1].replace('%20', ' ')
        else:
            path = parsed_uri.path
        if os.path.exists(path):
            return DrbFileNode(path, node)
        raise DrbFileNodeFactoryException(f'File not found: {path}')

    def _create(self, node: DrbNode) -> DrbNode:
        return self._create_from_uri_of_node(node)
