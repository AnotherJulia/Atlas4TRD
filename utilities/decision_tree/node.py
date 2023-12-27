class TreeNode:

    def __init__(self, slug, depth):
        self.slug = slug
        self.children = []

        self.model_depth = depth

    def attach_child(self, node):
        self.children.append(node)

    def return_children(self):
        return self.children


