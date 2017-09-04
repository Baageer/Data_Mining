from CSTree import CSNode, CSTree
from collections import Counter
import numpy as np
import queue
class DecisionTreeClassifier(object):
    def __init__(self, datas, attributes):
        self.datas = datas
        self.attributes = attributes
        self.root=None

    def is_same_class(self, datas, attributes):
        #print(datas)
        temp = datas[0][-1]
        for data in datas:
            if data[-1] != temp:
                return False
        return temp

    def is_same_attribute(self, datas, attributes):
        #print(attributes)
        temp_p = []
        for date in datas:
            temp_p.append(date[0])
        
        for attribute in attributes:
            temp_q = []
            for data in datas:
                temp_q.append(data[attribute])
            if temp_p != temp_q:
                return False
            temp_p = temp_q

        return True

    def find_count_max(self, datas, attributes):
        classes = [data[-1] for data in datas]
        count = Counter(classes)
        #max_count = count.most_common(1)[0][0]
        m = max(count.values())
        max_count = sorted([x for (x, y) in count.items() if y==m])[0]
        return max_count, count

    def best_attribute(self, datas, attributes, count):
        class_count = len(count)           #类别数
        num_count = [i for i in count.values()]         #类别对应样例个数的list
        sum_count = sum(count.values())    #样例总数
        ent_d = 0
        for i in range(class_count):
            ent_d_v = -( num_count[i]/sum_count * np.log2(num_count[i]/sum_count) )
            ent_d += ent_d_v
        #print('ent_d:', ent_d)
            
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
                b = [i for i in count.values()]
                c = sum(count.values())
                ent_d_temp = 0
                for i in range(a):
                    ent_d_v_temp = -( b[i]/c * np.log2(b[i]/c) )
                    ent_d_temp += ent_d_v_temp
                ent_sample += c/sum_count * ent_d_temp
            ent_attribute.append(ent_sample)
            if ent_sample > ent_max:
                best_attri = attribute
                best_attri_count = count_attri

        return best_attri, best_attri_count
            


    def tree_generate(self, datas, attributes):
        node = CSNode()
        #print('2', node)
        #print(root, root.data, root.firstchild, root.nextsibling)
        class_result = self.is_same_class(datas, attributes)
        if class_result != False:
            node.firstchild = None
            node.data = class_result
            #print('3', node)
            return node
        
        is_same = self.is_same_attribute(datas, attributes)
        class_result, count = self.find_count_max(datas, attributes)
        if len(attributes)==0 or is_same:            
            node.firstchild = None
            node.data = class_result
            #print('4', node)
            return node
        
        best_attri, best_attri_count = self.best_attribute(datas, attributes, count)

        for samp in best_attri_count.keys():
            d_v = [data for data in datas if data[best_attri]==samp]
            #print(d_v)
            node_v = CSNode()
            if len(d_v)==0 :
                node_v.firstchild =None
                node_v.nextsibling = None
                node_v.data = class_result
            else:
                #print(attributes,best_attri)
                temp_list = attributes.copy()
                temp_list.remove(best_attri)
                node_v = self.tree_generate(d_v, temp_list)
                #node_v = self.tree_generate(d_v, attributes.remove(best_attri))
                #改用copy()方法，避免在for循环与递归调用中使用同一个list

            if node.firstchild is None:
                node.firstchild = node_v
            else:
                node.firstchild.nextsibling = node_v
                
        #print(node)
        return node

def visit_func(node_t):
    print(node_t.data)

def preorder_traverse(node_t, visit_func):
    if node_t is not None:
        visit_func(node_t)
        preorder_traverse(node_t.firstchild, visit_func)
        preorder_traverse(node_t.nextsibling, visit_func)

def printTreeB(node_t):
    if (node_t is None):
        print ("Empty")
        return 0
    top = []
    bottom = []
    bottom.append(node_t)
    n = 1

    while len(top)!=0 or len(bottom)!=0 :
        #print(n)
        if len(bottom)!=0:
            b = bottom.pop()
            print("+"+"-"*n, b.data)
            n += 3
            if b.firstchild is not None:
                bottom.append(b.firstchild)
                
                
            top.append(b)
            #print('j: ',len(top))

        else:
            t = top.pop()
            n -= 3
            if t.nextsibling is not None:
                #print('i: ', len(top), ' ' ,t.data ,' ', t.nextsibling.data)
                bottom.append(t.nextsibling)
    


if __name__ == '__main__':
    clf = DecisionTreeClassifier([[0,1,0,1],[1,0,0,-1],[0,0,1,1],[0,0,0,-1]],
                                 [0,1,2])
    node = clf.tree_generate([[0,1,0,1],[1,0,0,-1],[0,0,1,1],[0,0,0,-1]],
                                 [0,1,2])
    #preorder_traverse(node, visit_func)
    
    printTreeB(node)
