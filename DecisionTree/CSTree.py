
class CSNode(object):
    def __init__(self, data = -1, firstchild=None, nextsibling=None):
        self.data = data
        self.firstchild = firstchild
        self.nextsibling = nextsibling

class CSTree(object):
    def __init__(self):
        self.root = CSNode()

    def __clear_tree(self, node_t):
        if(node_t is not None):
            clear_tree(node_t.firstchild)
            clear_tree(node_t.nextsibling)
            node_t = None

    def __tree_depth(self, node_t):
        node_p = CSNode()
        depth = 0
        max_depth = 0
        if node_t is None:
            return 0

        node_p=node_t.firstchild
        while node_p != None:
            depth = tree_depth(node_p)
            if depth>max_depth:
                max_depth = depth
            node_p=node_p.nextsibling
        return max_depth+1

    def __preorder_traverse(self, node_t, visit_func):
        if node_t is None:
            visit_func(node_t)
            preorder_traverse(node_t.firstchild, visit_func)
            preorder_traverse(node_t.nextsibling, visit_func)

    def __postorder_traverse(self, node_t, visit_func):
        if node_t is None:
            postorder_traverse(node_t.firstchild, visit_func)
            visit_func(node_t)
            postorder_traverse(node_t.nextsibling, visit_func)

    def clear_tree(self):
        clear_tree(self.root)
    
    def create_tree_from_file(filename):
        file_in = open(filename)

    def tree_empty(self):
        if self.root is None:
            return True
        else:
            return False
    def tree_depth(self):
        node_p = self.root
        depth = 0
        max_depth=tree_depth(node_p)
        if node_p is not None:
            node_p = node_p.nextsibling
        while node_p is not None:
            depth = tree_depth(node_p)
            if depth > max_depth:
                max_depth = depth
            node_p = node_p.nextsibling

        return max_depth

    def insert_child(self, node_p, position_i, node_new):
        node_temp = node_new
        node_new.root = None
        if self.root is not None:
            if position_i == 1:
                node_temp.nextsibling = node_p.firstchild
                node_p.firstchild = node_temp
            else:
                node_q = node_p.firstchild
                j = 2
                while q is not None and j < position_i:
                    node_q = node_q.nextsibling
                    j += 1
                    if j==position_i:
                        node_temp.nextsibling = node_q.nextsibling
                        node_q.nextsibling = node_temp
                    else:
                        return False
            return True
        else:
            return False
            
