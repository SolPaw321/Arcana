from anytree import Node, RenderTree, find, find_by_attr
from typing import Any


class RegistryTree:
    def __init__(self, root: str):
        super().__init__()
        self._root = Node(root)

    @property
    def root(self) -> Node:
        """Return the root."""
        return self._root

    def find_by_name(self, name: str) -> Node | None:
        """
        Find node by name.

        :param name: node name to be found
        :return: The founded node or None, if not fund
        """
        res = find(self._root, filter_=lambda node: node.name == name)
        return res

    def add_key(self, key: str, parent: str = None, **kwargs):
        """
        Add a key into the tree.
        If parent is not specified, then the key will be added to root.

        :param key: name to be added
        :param parent: parent name. default is None
        :param kwargs: specify data to be hold into the node
        """
        if not parent:
            parent = self._root
        else:
            parent = self.find_by_name(parent)

        if not self.find_by_name(key):
            if kwargs:
                Node(key, parent=parent, **kwargs)
            else:
                Node(key, parent=parent)

    def render_tree(self):
        """Render the tree."""
        for pre, fill, node in RenderTree(self._root):
            print("%s%s" % (pre, node.name))

    def all_registered(self) -> tuple[str]:
        """Return all leaves in the tree."""
        names = [leaf.name for leaf in self._root.leaves]
        return tuple(names)

    def get_data(self, node_name: str, data_name: str) -> Any | None:
        """
        Return the data holding into specific node.

        :param node_name: the node name
        :param data_name: the holding data name
        :return: founded data or None
        """
        return getattr(self.find_by_name(node_name), data_name)

