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

    def best_attribute(self, datas, attributes, count):
        class_count = len(count)           #类别数
        num_count = count.values()         #类别对应样例个数的list
        sum_count = sum(count.values())    #样例总数
        ent_d = 0
        for i in range(class_count):
            ent_d_v = -( num_count[i]/sum_count * np.log(num_count[i]/sum_count, 2) )
            ent_d += ent_d_v
            
        ent_attribute = []
        best_attri = attributes[0]
        ent_max = 0
        for attribute in attributes :
            data_attri = [data[attribute] for data in datas]
            data_class = [data[-1] for data in datas]
            data_v = zip(data_attri, data_class)
            count_attri = Counter(data_attri)
            ent_sample = 0
            for samp in count_attri.keys():
                attri_temp = [ attri for attri in data_attri if attri==samp] #取出所有样本的值
                class_temp = [ y for (x,y) in data_v if x==samp ]
                count_temp = Counter(class_temp)
                a = len(count_temp)
                b = count.values()
                c = sum(count.values())
                ent_d_temp = 0
                for i in range(a):
                    ent_d_v_temp = -( b[i]/c * np.log(b[i]/c, 2) )
                    ent_d_temp += ent_d_v_temp
                ent_sample += c/sum_count * ent_d_temp
            ent_attribute.append(ent_sample)
            if ent_sample > ent_max:
                best_attri = attribute
                best_attri_count = count_attri

        return best_attri

    def sub_attribute(attributes, attribute):

            


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
        
        best_attri, best_attri_count = best_attribute(attributes, count)

        for samp in best_attri_count.keys():
            d_v = [data[best_attri] for data in datas if data[best_attri]==samp]
            node_v = CSNode()
            if !d_v :
                node_v.firstchild =None
                node_v.nextsibling = None
                node_v.data = class_result
            else:
                node_v = tree_generate(d_v, attributes.remove(best_attri))

            if node.firstchild is None:
                node.firstchild = node_v
            else:
                node.firstchild.nextsibling = node_v

        return node



if __name__ == '__main__':
    clf = DecisionTreeClassifier()
    clf.tree_generate()
