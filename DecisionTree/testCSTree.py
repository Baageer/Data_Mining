from CSTree import CSNode, CSTree
import queue
import time

def printTree(node_t):
    if (node_t is None):
        print ("Empty")
        return 0
    top = queue.Queue()
    bottom = queue.Queue()
    bottom.put(node_t)
    n = 1
    print(top.empty(),bottom.empty())
    while top.empty()==False or bottom.empty()==False :
        #print(n)
        if bottom.empty()==False:
            b = bottom.get()
            print("+"+"-"*n, b.data)
            if b.firstchild is not None:
                bottom.put(b.firstchild)
                
                n += 1
            top.put(b)
            print('j: ',top.qsize())

        else:
            t = top.get()
            if t.nextsibling is not None:
                print('i: ', top.qsize(), ' ' ,t.data ,' ', t.nextsibling.data)
                bottom.put(t.nextsibling)
                n -= 1


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
    nodeA = CSNode("A")
    nodeB = CSNode("B")
    nodeC = CSNode("C")
    nodeD = CSNode("D")
    nodeE = CSNode("E")
    nodeF = CSNode("F")
    nodeG = CSNode("G")
    nodeH = CSNode("H")
    nodeI = CSNode("I")
    nodeJ = CSNode("J")
    nodeK = CSNode("K")

    nodeA.firstchild = nodeB
    nodeB.firstchild = nodeD
    nodeB.nextsibling = nodeC
    nodeD.firstchild = nodeH
    nodeD.nextsibling = nodeE
    nodeE.nextsibling = nodeF
    nodeC.firstchild = nodeG
    nodeG.firstchild = nodeI
    nodeI.nextsibling = nodeJ
    nodeJ.nextsibling = nodeK

    printTreeB(nodeA)

    
