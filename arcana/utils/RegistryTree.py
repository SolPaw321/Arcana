from anytree import Node, RenderTree

class RegistryTree:
    def __init__(self, root: str):
        super().__init__()
        self._root = Node(root)
        self._nodes = {root: self._root}

    @property
    def root(self):
        return self._root

    def add_key(self, key: str, parent: str = None, **kwargs):
        if not parent:
            parent = self._root
        else:
            parent = self._nodes[parent]

        if key not in self._nodes:
            if kwargs:
                self._nodes[key] = Node(key, parent=parent, **kwargs)
            else:
                self._nodes[key] = Node(key, parent=parent)

    def render_tree(self):
        for pre, fill, node in RenderTree(self._root):
            print("%s%s" % (pre, node.name))

    def all_registered(self):
        return self._nodes.keys()

    def get_data(self, node_name: str, data_name: str):
        return getattr(self._nodes[node_name], data_name)
