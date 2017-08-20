from CSTree import CSNode, CSTree

class DecisionTreeClassifier(object):
    def __init__(self, datas, ):
        self.datas = datas

    def tree_generate(self):
        root = CSNode(self.datas)
        #print(root, root.data, root.firstchild, root.nextsibling)

if __name__ == '__main__':
    clf = DecisionTreeClassifier(5)
    clf.tree_generate()
