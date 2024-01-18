from utilities.decision_tree import Tree, TreeNode, TreeEngine, Leaf

# TREE CREATION
tree = Tree("patient allocation", "intake")
tree.build(decision_map_path="../../config/decision_map.json")


# CHECK THE MODEL
<<<<<<< HEAD
tree.model()

# LETS CREATE THE AGENTS
engine = TreeEngine(tree, leaf_template=Leaf, leaf_count=10000, decision_map_path="../../config/decision_map.json")
engine.plot_distributions(10, verbose=True)
=======
# tree.model()

# LETS CREATE THE AGENTS
engine = TreeEngine(tree, leaf_template=Leaf, leaf_count=1000, decision_map_path="../../config/decision_map.json")
engine.plot_distributions(4, verbose=True)
>>>>>>> origin/packaging/framework

