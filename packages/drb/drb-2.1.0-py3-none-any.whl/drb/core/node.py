from __future__ import annotations

import abc
import io
from typing import List, Optional, Any, Dict, Tuple

from deprecated import deprecated

from .item import DrbItem
from .path import ParsedPath, parse_path
from ..exceptions.core import DrbException
from ..utils.utils import get_name_namespace_index, get_name_namespace_value


class DrbNode(DrbItem, abc.ABC):
    """
    Generic node interface. This interface represents a single node of a tree
    of data. Any node can have no, one or several children. This interface
    provides the primarily operations to browse an entire data structure. All
    implementations of the "Data Request Broker" shall be able to produce such
    nodes.
    """
    __event_type_node = {
        'child-added',
        'child-removed',
        'child-changed',
        'attribute-added',
        'attribute-removed',
        'attribute-changed',
    }

    def __init__(self):
        super(DrbNode, self).__init__()
        self.__namespace_aware = None
        self._attrs = {}
        self._parent = None
        self._available_impl = [io.BufferedIOBase]
        for event_name in self.__event_type_node:
            self._event_manager.append_event_type(event_name)

    def __matmul__(self, other):
        """
        Returns a specific attribute requested in argument,
        this argument can be a str the name of the attribute,
        or a tuple representing the name and namespace of the
        attribute.

        the usage:
            node @ name -> retrieve the attribute
            node @ (name, namespace) -> retrieve the attribute

        Returns:
            Any: The value of the attribute
        """
        try:
            key = get_name_namespace_index(other)
            return self._attrs[(key[0], key[1])]
        except (IndexError, TypeError, KeyError) as error:
            raise DrbException(f'No attribute {other} found') from error

    def __imatmul__(self, other):
        """
        Allow to add, update or delete an attributes.

        the usage:
            node @= (name, value) -> add/update the attribute
            node @= (name, namespace, value) -> add/update the attribute
            node @ (name, None) -> delete the attribute
            node @ (name, namespace, None) -> delete the attribute

        Returns:
            DrbNode: The node requested
        """
        name, namespace, value = get_name_namespace_value(other)
        if value is None:
            del self._attrs[(name, namespace)]
        else:
            self._attrs[(name, namespace)] = value
        return self

    def attribute_names(self):
        """
        Retrieve a set of str representing the name of all
        the attributes of a DrbNode.

        Returns:
            Set(str): A set of attributes names
        """
        return set([x for x in self._attrs.keys()])

    @property
    @abc.abstractmethod
    @deprecated(version='2.1.0',
                reason='Usage of the @ operator is recommended')
    def attributes(self) -> Dict[Tuple[str, str], Any]:
        """
        Returns attributes of the current node. This operation all attributes
        owned by the current node.
        Attributes are represented by a dict with as key the tuple
        (name, namespace_uri) of the attribute and as value the value of this
        attribute.

        Returns:
            dict: A dict of attributes of the current node
        """
        raise NotImplementedError

    @deprecated(version='2.1.0',
                reason='Usage of the @ operator is recommended')
    def get_attribute(self, name: str, namespace_uri: str = None) -> Any:
        """
        Returns the value of the corresponding attribute, following its name,
        and its namespace URI for the matching.

        Parameters:
            name (str): attribute name to match
            namespace_uri (str, optional): attribute namespace URI to match
        Returns:
            Any: the associated value of the matched attribute
        :Raises:
            DrbException: if the given name and namespace URI not math any
            attribute of the current node
        """
        key = (name, namespace_uri)
        if key in self._attrs.keys():
            return self @ key
        raise DrbException(f'Attribute not found name: {name}, '
                           f'namespace: {namespace_uri}')

    @property
    @abc.abstractmethod
    @deprecated(version='2.1.0', reason='Only bracket browse should be use')
    def children(self) -> List[DrbNode]:
        """
        The list of children of the current node. Returns a list of
        references to the children of the current node. The current node may
        have no child and the operation returns therefore a null reference.

        Returns:
            list: The list of children
        """
        raise NotImplementedError

    @property
    def parent(self) -> Optional[DrbNode]:
        """
        The parent of this node. Returns a reference to the parent node
        of the current node according to the current implementation.
        Most of the nodes have a parent except root nodes or
        if they have just been removed, etc.
        If the node has no parent the operation returns None.

        Returns:
            The parent of this node or None
        """
        return self._parent

    @parent.setter
    def parent(self, parent: DrbNode) -> None:
        self._parent = parent

    @property
    def path(self) -> ParsedPath:
        """
        The full path of this node. The path is the complete location
        of this node. The supported format is URI and apache common VFS.

        Returns:
            A ParsedPath representing the node location
        """
        if self.parent is None:
            return parse_path(self.name)
        return self.parent.path / self.name

    @abc.abstractmethod
    def __len__(self):
        """
        Returns the children number of the current node.

        Returns:
            int: children number
        """
        raise NotImplementedError

    @abc.abstractmethod
    def __getitem__(self, item):
        """
        Implements the item in bracket operator to access this node children.
        The brace operator is used to access the children node, according to
        the following supported items:

        * ``int``: the item-th children node will be returned

        * ``slice``: children node of the requested slice will be returned

        * ``str``: the first child node with the item as name is retrieved
          from its children

        * ``tuple``: the following tuple must be supported per each node
          implementation:

            * (name: ``str``, namespace: ``str``): retrieves first child by is
              name and namespace_uri.

            * (name: ``str``, item: ``int`` | ``slice``): retrieves a child or
              a children interval having a specific name.

            * (name: ``str``, namespace: ``str``, item: ``int`` | ``slice``):
              retrieves a child or a children interval having a specific name
              and namespace_uri

        * ``Predicate``: children nodes matching this predicate are
          returned, may return an empty list

        Returns:
            DrbNode or List[DrbNode]: expected child node(s) according to the
            case
        Raises:
            DrbException: if no child is found, except for ``Predicate`` case
                          where an empty may return.
        Examples:

        .. code-block:: python

            # get first child
            child = node[0]
            # get last child
            child = node[-1]
            # get children interval (last 3 children)
            children = node[-3:-1]

            # first child by its name
            child = node['child_name'] # == node['child_name', 0]
            # third child named name_child
            child = node['child_name', 2]
            # children interval of child named child_name (first 2 children)
            children = node['child_name', :2]

            # first child named child_name and having as namespace ns
            child = node['child_name', 'ns']
            # last child named child_name and having as namespace ns
            child = node['child_name', 'ns', -1]
            # all children named child_name and having as namespace ns
            child = node['child_name', 'ns', :]

            # get children using a Predicate
            children = node[MyPredicate()]
        """
        return NotImplemented

    def __setitem__(self, key, value):
        """
        Implements the item in bracket operator to add or update the children,
        of a node, by given in argument the key and the new value.
        The key can be:

        * ``int``: the item-th children node will be updated

        * ``str``: the first child node with the item as name is updated

        * ``tuple``: the following tuple must be supported per each node
          implementation:

            * (name: ``str``, namespace: ``str``): update first child by is
              name and namespace_uri.

        The value must be a new DrbNode, the node will be a new child of the
        first node.

        Raises:
            DrbException: if no child is found, except for ```` case
                          where an empty may return.
        Examples:

        .. code-block:: python

            # Add a new children
            node[None] = new_node

            # Update an existing children
            node['name'] = new_node
            node['name', 'namespace'] = new_node
        """
        return NotImplemented

    def __delitem__(self, key):
        """
        Implements the item in bracket operator to delete a children,
        of a node, by given in argument the key, it can be:

        * ``int``: the item-th children node will be deleted

        * ``str``: the first child node with the item as name is deleted
          from its children

        * ``tuple``: the following tuple must be supported per each node
          implementation:

            * (name: ``str``, namespace: ``str``): delete first child by is
              name and namespace_uri.

        Raises:
            DrbException: if no child is found, except for ```` case
                          where an empty may return.
        Examples:

        .. code-block:: python

            # Delete an existing children
            del node['name']
            del node['name', 'namespace']
        """
        return NotImplemented

    @abc.abstractmethod
    def has_child(self, name: str = None, namespace: str = None) -> bool:
        """
        Checks if current node has a child following name and namespace
        criteria. If `name` and `namespace` are not specified it will check if
        the current node has at least a child.

        Returns:
            bool: ``True`` if current node has a child following name and
            namespace criteria, otherwise ``False``
        """
        raise NotImplementedError

    def impl_capabilities(self) -> List[type]:
        """
        List all the possible interface the node can provide.

        Returns:
            List[type]: A list of all interface possible
        """
        return self._available_impl.copy()

    def has_impl(self, impl: type) -> bool:
        """
        Tests if a specific interface can be provided. These operation tests
        with a minimum of time and memory consumption if the current
        implementation can provide a specific interface. It is important to
        consider that ``has_impl`` provides information about the ability to
        provide such interface in general cases but not focused on the current
        instance. It may therefore be impossible to get a specific
        implementation from a node whereas ``has_impl`` operation returns true.

        Parameters:
            impl (type): the implementation type expected
        Returns:
            bool: True if an implementation of the interface can be provided
        and False otherwise.
        """
        for t in self._available_impl:
            if issubclass(impl, t):
                return True
        return False

    @abc.abstractmethod
    def get_impl(self, impl: type, **kwargs) -> Any:
        """
        This operation returns a reference to an object implementing a
        specific interface. This method authorizes a specific and/or direct
        API instead of using the DrbNode interface. The provided object is
        independent of this node and shall be released/closed by the caller
        when interface requires such finally operations.

        Parameters:
            impl (type): the implementation type expected
        Return:
            Any: the expected implementation.
        Raises:
            DrbNotImplementedException: if `impl` is not supported by the
                                        current node
        """
        raise NotImplementedError

    def close(self) -> None:
        """
        Releases all resources attached to the current node.
        """
        pass

    @property
    def namespace_aware(self) -> bool:
        """
        Property flag to decide about behaviour during browsing of its
        children. This flag is transitive from a parent to its child until the
        first definition using this property setter. Default value ``False``

        * ``True``: take into account children namespace during browsing
        * ``False``: does not take into account children namespace during
          browsing

        Returns:
            bool: ``True`` if node take care of namespace during browsing of
        its children, otherwise ``False``
        """
        if self.__namespace_aware is None:
            if self.parent is None:
                return False
            return self.parent.namespace_aware
        return self.__namespace_aware

    @namespace_aware.setter
    def namespace_aware(self, value: Optional[bool]) -> None:
        """
        Update browsing behaviour. see :func:`~node.DrbNode.namespace_aware`
        Parameters:
            value (bool): new value of ``namespace_aware`` or None to retrieve
                          parent behaviour
        Raises:
            ValueError: if the given value is not a boolean
        """
        if value is not None and not isinstance(value, bool):
            raise ValueError('Only a value boolean is expected here !')
        self.__namespace_aware = value

    def __hash__(self):
        return hash(self.path.name)

    def __contains__(self, item) -> bool:
        if isinstance(item, str):
            return self.has_child(item)
        if isinstance(item, tuple) and len(item) == 2:
            return self.has_child(*item)
        return False

    def __eq__(self, other):
        return self.path == other.path
