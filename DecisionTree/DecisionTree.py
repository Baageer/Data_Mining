from CSTree import CSNode, CSTree
from collections import Counter
import numpy as np
class DecisionTreeClassifier(object):
    def __init__(self, datas, attributes):
        self.datas = datas
        self.attributes = attributes

    def is_same_class(self, datas, attributes):
        temp = datas[0][-1]
        for data in datas:
            if data[-1] != temp:
                return False
        return temp

    def is_same_attribute(self, datas, attributes):
        temp_p = []
        for i in attributes:
            temp_p += datas[0][i]

        for data in datas:
            for attribute in attributes:
                temp_q += datas
            if temp_p != temp_q:
                return False
            temp_p = temp_q
        
        classes = [data[-1] for data in datas]
        count = Counter(classes)
        #max_count = count.most_common(1)[0][0]
        m = max(count.values())
        max_count = sorted([x for (x, y) in count.items() if y==m])[0]
        return max_count, count

    def best_attributel(self, attributes, count):
        class_count = len(count)           #类别数
        num_count = count.values()         #类别对应样例个数的list
        sum_count = sum(count.values())    #样例总数
        ent_d = 0
        for i in range(class_count):
            ent_d_v = -( num_count[i]/sum_count * np.log(num_count[i]/sum_count, 2) )
            ent_d += ent_d_v

    def tree_generate(self, datas, attributes):
        node = CSNode()
        #print(root, root.data, root.firstchild, root.nextsibling)
        class_result = is_same_class(datas, attributes)
        if class_result != False:
            node.firstchild = None
            node.data = class_result
            return 0
        
        class_result, count = is_same_attribute(datas, attributes)
        if !attributes or class_result != False:
            node.firstchild = None
            node.data = class_result
            return 0
        
        best_attri = best_attribute(attributes, count)


if __name__ == '__main__':
    clf = DecisionTreeClassifier()
    clf.tree_generate()
