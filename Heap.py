class Node_Qnow:
    def __init__(self, val = None, min = None):
        self.right = None
        self.left = None
        self.val = val
        self.min = min
        self.parent = None
        self.bal = None
    
class Qnow:
    def __init__(self):
        self.root = Node_Qnow()

    def insert(self, x):
        aux = self.root
        if aux.val == None:
            aux.val = x
            aux.min = x
            aux.bal = 0
        else:
            self.insertQnowBal(aux, x)

    def insertQnow(self, node, x):
        if node.min > x:
            node.min = x
        if x > node.val:
            if node.right == None:
                new = Node_Qnow(x, x)
                new.parent = node
                node.right = new
            else:
                new = self.insertQnow(node.right, x)
        else:
            if node.left == None:
                new = Node_Qnow(x , x)
                new.parent = node
                node.left = new
            else:
                new = self.insertQnow(node.left, x)
        return new

    def insertQnowBal(self, node, x):
        q = self.insertQnow(node, x)
        q.bal = 0
        p = q.parent
        while p != None:
            if p.left == q:
                if p.bal == 1:
                    p.bal = 0
                    p = None
                elif p.bal == 0:
                    p.bal = -1
                    q = p
                    p = p.parent
                else:
                    if q.bal == -1:
                        self.RotDir(p)
                        p.bal = 0
                        q.bal = 0
                    else:
                        t = q.right
                        self.RotEsq(q)
                        self.RotDir(p)
                        if t.bal == 1:
                            q.bal = -1
                        else:
                            q.bal = 0
                        if t.bal == -1:
                            p.bal = 1
                        else:
                            p.bal = 0
                        t.bal = 0
                    p = None
            else:
                if p.bal == -1:
                    p.bal = 0
                    p = None
                elif p.bal == 0:
                    p.bal = 1
                    q = p
                    p = p.parent
                else:
                    if q.bal == 1:
                        self.RotEsq(p)
                        p.bal = 0
                        q.bal = 0
                    else:
                        t = q.left
                        self.RotDir(q)
                        self.RotEsq(p)
                        if t.bal == 1:
                            p.bal = -1
                        else:
                            p.bal = 0
                        if t.bal == -1:
                            q.bal = 1
                        else:
                            q.bal = 0
                    p = None
        root = self.root
        while root.parent != None:
            root = root.parent
        self.root = root
    
    def delete(self, x):
        aux = self.root
        self.DeleteQnowBal(aux, x)

    def DeleteQnow(self, node, x):
        if x > node.val:
            aux, esquerda = self.DeleteQnow(node.right, x)
        elif x < node.val:
            aux, esquerda = self.DeleteQnow(node.left, x)
        else:
            if node.right == None:
                aux = node.left
                if node.parent == None:
                    self.root = aux
                    return node.parent, False
                if node.parent.left == node:
                    esquerda = True
                    node.parent.left = aux
                else:
                    esquerda = False
                    node.parent.right = aux
                if aux != None:
                    aux.parent = node.parent
                return node.parent, esquerda
            node.val = node.right.min
            aux, esquerda = self.DelMin(node.right)
        if node.left == None:
            node.min = node.val
        else:
            node.min = node.left.min
        return aux, esquerda

    def DelMin(self, node):
        if node.left == None:
            if node.parent.left == node:
                esquerda = True
                node.parent.left = node.right
                if node.right != None:
                    node.right.parent = node.parent
            else:
                esquerda = False
                node.parent.right = node.right
                if node.right != None:
                    node.right.parent = node.parent
            return node.parent, esquerda           
        else:
            aux, esquerda = self.DelMin(node.left)
            if node.left == None:
                node.min = node.val
            else:
                node.min = node.left.min
            return aux, esquerda

    def DeleteQnowBal(self, node, x):
        p, esquerda = self.DeleteQnow(node, x)
        diminuiu = True
        while diminuiu and p != None:
            if esquerda:
                p, diminuiu = self.AjusteEsq(p)
            else:
                p, diminuiu = self.AjusteDir(p)
            if p.parent != None and p == p.parent.left:
                esquerda = True
            else:
                esquerda = False
            p = p.parent
        root = self.root
        if root == None:
            return
        while root.parent != None:
            root = root.parent
        self.root = root

    def AjusteEsq(self, p):
        if p.bal  == -1:
            p.bal = 0
            return p, True
        elif p.bal == 0:
            p.bal = 1
            return p, False
        else:
            q = p.right
            if q.bal >= 0:
                self.RotEsq(p)
                if q.bal == 0:
                    p.bal = 1
                    q.bal = -1
                    return q, False
                else:
                    p.bal = 0
                    q.bal = 0
                    return q, False
            else:
                t = q.left
                self.RotDir(q)
                self.RotEsq(p)
                if t.bal == 1:
                    p.bal = -1
                else:
                    p.bal = 0
                if t.bal == -1:
                    q.bal = 1
                else:
                    q.bal = 0
                t.bal = 0
                return t, True

    def AjusteDir(self, p):
        if p.bal == 1:
            p.bal = 0
            return p, True
        elif p.bal == 0:
            p.bal = -1
            return p, False
        else:
            q = p.right
            if q.bal <= 0:
                self.RotDir(p)
                if q.bal == 0:
                    p.bal = -1
                    q.bal = 1
                    return q, False
                else:
                    q.bal = 0
                    p.bal = 0
                    return q, True
            else:
                t = q.right
                self.RotEsq(q)
                self.RotDir(p)
                if t.bal == 1:
                    q.bal = -1
                else:
                    q.bal = 0
                if t.bal == -1:
                    p.bal = 1
                else:
                    p.bal = 0
                t.bal = 0
                return t, True

    def RotEsq(self, node):
        aux = node.right
        node.right = aux.left
        if aux.left != None:
            aux.left.parent = node
        aux.left = node
        aux.min = node.min
        aux.parent = node.parent
        node.parent = aux
        if aux.parent != None:
            p = aux.parent
            if p.left == node:
                p.left = aux
            else:
                p.right = aux
    
    def RotDir(self, node):
        aux  = node.left
        node.left = aux.right
        aux.right = node
        if node.left != None:
            node.left.parent = node
            node.min = node.left.min
        else:
            node.min = node.val
        aux.parent = node.parent
        node.parent = aux
        if aux.parent != None:
            p = aux.parent
            if p.left == node:
                p.left = aux
            else:
                p.right = aux
    
    def Print(self):
        self.PrintAux(self.root)
        print()
    
    def PrintAux(self, node):
        if node == None:
            return
        self.PrintAux(node.left)
        print(node.val, end = " ")
        self.PrintAux(node.right)
    
    def PrintArvore(self):
        self.PrintArvoreAux(self.root, 0)
        print()
        print()
    
    def PrintArvoreAux(self, node, d):
        if node == None:
            return
        self.PrintArvoreAux(node.right, d + 1)
        for i in range(0, d):
            print("    ", end = "")
        print(node.val)
        self.PrintArvoreAux(node.left, d + 1)
    def Min(self):
        if self.root == None:
            return None
        return self.root.min


class NodeH:
    def __init__(self, is_leaf, max_left_time, left, right, value, weight, smin, fvmax, fvmin, parent, bal):
        self.is_leaf = is_leaf
        self.max_left_time = max_left_time
        self.left = left
        self.right = right
        self.value = value
        self.weight = weight
        self.smin = smin
        self.fvmax = fvmax
        self.fvmin = fvmin
        self.parent = parent
        self.bal = bal
        if is_leaf:
            if weight == 1:
                self.fvmax = self
            if weight == 0:
                self.fvmin = self
    
class ABBB_OP:
    def __init__(self):
        self.ABBB = None
    
    def insert(self, time, value, op):
        if self.ABBB == None:
            new = NodeH(True, time, None, None, value, op, op, None, None, None, 0)
            self.ABBB = new
        else:
            self.insertBal(time, value, op)

    def insertBal(self, time, value, op):
        q = self.insertAux(self.ABBB, time, value, op)
        q.bal = 0
        p = q.parent
        while p != None:
            if p.left == q:
                if p.bal == 1:
                    p.bal = 0
                    p = None
                elif p.bal == 0:
                    p.bal = -1
                    q = p
                    p = p.parent
                else:
                    if q.bal == -1:
                        self.RotDir(p)
                        p.bal = 0
                        q.bal = 0
                    else:
                        t = q.right
                        self.RotEsq(q)
                        self.RotDir(p)
                        if t.bal == 1:
                            q.bal = -1
                        else:
                            q.bal = 0
                        if t.bal == -1:
                            p.bal = 1
                        else:
                            p.bal = 0
                        t.bal = 0
                    p = None
            else:
                if p.bal == -1:
                    p.bal = 0
                    p = None
                elif p.bal == 0:
                    p.bal = 1
                    q = p
                    p = p.parent
                else:
                    if q.bal == 1:
                        self.RotEsq(p)
                        p.bal = 0
                        q.bal = 0
                    else:
                        t = q.left
                        self.RotDir(q)
                        self.RotEsq(p)
                        if t.bal == 1:
                            p.bal = -1
                        else:
                            p.bal = 0
                        if t.bal == -1:
                            q.bal = 1
                        else:
                            q.bal = 0
                    p = None
        root = self.ABBB
        while root.parent != None:
            root = root.parent
        self.ABBB = root

    def insertAux(self, node, time, value, op):
        if node.is_leaf:
            return self.subArvore(node, time, value, op)
        else:
            if time > node.max_left_time:
                new = self.insertAux(node.right, time, value, op)
                self.Atualiza(node)
            else:
                new = self.insertAux(node.left, time, value, op)
                self.Atualiza(node)
            return new

    def delete(self, time):
        if self.ABBB.is_leaf:
            self.ABBB = None
        else:
            self.deleteBal(time)
    
    def deleteBal(self, time):
        p, esquerda = self.deleteAux(self.ABBB, time)
        diminuiu = True
        while diminuiu and p != None:
            if esquerda:
                p, diminuiu = self.AjusteEsq(p)
            else:
                p, diminuiu = self.AjusteDir(p)
            if p.parent != None and p == p.parent.left:
                esquerda = True
            else:
                esquerda = False
            p = p.parent
        root = self.ABBB
        while root.parent != None:
            root = root.parent
        self.ABBB = root

    def deleteAux(self, node, time):
        if node.is_leaf:
            parent = node.parent
            if parent.parent == None:
                if parent.max_left_time < time:
                    self.ABBB = parent.left
                    parent.left.parent = None
                    return parent.left, False
                else:
                    self.ABBB = parent.right
                    parent.right.parent = None
                    return parent.right, False
            else:
                if parent.parent.right == parent:
                    esquerda = False
                    if parent.right == node:
                        parent.parent.right = parent.left
                        parent.left.parent = parent.parent
                        self.Atualiza(parent.parent)
                    else:
                        parent.parent.right = parent.right
                        parent.left.parent = parent.parent
                        self.Atualiza(parent.parent)
                else:
                    esquerda = True
                    if parent.right == node:
                        parent.parent.left = parent.left
                        parent.left.parent = parent.parent
                        parent.parent.max_left_time = parent.parent.left.max_left_time
                        self.Atualiza(parent.parent)
                    else:
                        parent.parent.left = parent.right
                        parent.right.parent = parent.parent
                        parent.parent.max_left_time = parent.parent.left.max_left_time
                        self.Atualiza(parent.parent)
                return parent.parent, esquerda
        else:
            if node.max_left_time < time:
                new, esquerda = self.deleteAux(node.right, time)
                self.Atualiza(node)
                return new, esquerda
            else:
                new, esquerda = self.deleteAux(node.left, time)
                self.Atualiza(node)
                return new, esquerda

    def AjusteEsq(self, p):
        if p.bal  == -1:
            p.bal = 0
            return p, True
        elif p.bal == 0:
            p.bal = 1
            return p, False
        else:
            q = p.right
            if q.bal >= 0:
                self.RotEsq(p)
                if q.bal == 0:
                    p.bal = 1
                    q.bal = -1
                    return q, False
                else:
                    p.bal = 0
                    q.bal = 0
                    return q, False
            else:
                t = q.left
                self.RotDir(q)
                self.RotEsq(p)
                if t.bal == 1:
                    p.bal = -1
                else:
                    p.bal = 0
                if t.bal == -1:
                    q.bal = 1
                else:
                    q.bal = 0
                t.bal = 0
                return t, True

    def AjusteDir(self, p):
        if p.bal == 1:
            p.bal = 0
            return p, True
        elif p.bal == 0:
            p.bal = -1
            return p, False
        else:
            q = p.right
            if q.bal <= 0:
                self.RotDir(p)
                if q.bal == 0:
                    p.bal = -1
                    q.bal = 1
                    return q, False
                else:
                    q.bal = 0
                    p.bal = 0
                    return q, True
            else:
                t = q.right
                self.RotEsq(q)
                self.RotDir(p)
                if t.bal == 1:
                    q.bal = -1
                else:
                    q.bal = 0
                if t.bal == -1:
                    p.bal = 1
                else:
                    p.bal = 0
                t.bal = 0
                return t, True

    def RotEsq(self, node):
        aux = node.right
        node.right = aux.left
        if aux.left != None:
            aux.left.parent = node
        aux.left = node
        aux.parent = node.parent
        node.parent = aux
        if aux.parent != None:
            p = aux.parent
            if p.left == node:
                p.left = aux
            else:
                p.right = aux
        self.Atualiza(node)
        self.Atualiza(aux)
    
    def RotDir(self, node):
        aux  = node.left
        node.left = aux.right
        aux.right = node
        if node.left != None:
            node.left.parent = node
        aux.parent = node.parent
        node.parent = aux
        if aux.parent != None:
            p = aux.parent
            if p.left == node:
                p.left = aux
            else:
                p.right = aux
        self.Atualiza(node)
        self.Atualiza(aux)
    
    def subArvore(self, node, time, value, op):
        parent = node.parent
        new = NodeH(True, time, None, None, value, op, op, None, None, None, 0)
        if time > node.max_left_time:
            direita = new
            esquerda = node
        else:
            direita = node
            esquerda = new
        subRoot = NodeH(False, None, esquerda, direita, None, None, None, None, None, parent, 0)
        subRoot.max_left_time = subRoot.left.max_left_time
        self.Atualiza(subRoot)
        node.parent = subRoot
        new.parent = subRoot
        if parent != None:
            if parent.right == node:
                parent.right = subRoot
            else:
                parent.left = subRoot
        return subRoot

    def Weight(self, node):
        return 0 if node == None else node.weight
    
    def Smin(self, node):
        return 0 if node == None else node.smin

    def min3(self, a, b, c):
        if a > b:
            if a > c:
                return a
            else:
                return c
        else:
            if b > c:
                return b
            else:
                return c

    def Fvmax(self, node):
        return None if node == None else node.fvmax
    
    def Value(self, node):
        return None if node == None else node.value

    def MaxVal(self, node1, node2):
        val1 = self.Value(node1)
        val2 = self.Value(node2)
        if val1 == None:
            return node2
        if val2 == None:
            return node1
        return node1 if val1 > val2 else node2
        
    def Fvmin(self, node):
        return None if node == None else node.fvmin
    
    def MinVal(self, node1, node2):
        val1 = self.Value(node1)
        val2 = self.Value(node2)
        if val1 == None:
            return node2
        if val2 == None:
            return node1
        return node1 if val1 < val2 else node2

    def Atualiza(self, node):
        node.weight = self.Weight(node.right) + self.Weight(node.left)
        node.smin = self.min3(0, self.Smin(node.right), self.Smin(node.right) + self.Smin(node.left))
        node.fvmax = self.MaxVal(self.Fvmax(node.right), self.Fvmax(node.left))
        node.fvmin = self.MinVal(self.Fvmin(node.right), self.Fvmin(node.left))
    
    def maxK(self, t):
        node = self.ABBB
        k = 0
        if node == None:
            return None
        while not node.is_leaf:
            if node.left.max_left_time < t:
                k += self.Weight(node.left)
                node = node.right
            else:
                node = node.left
        k += node.weight
        if k != 0:
            aux = node.parent
            while aux != None and aux.left == node:
                node = aux
                aux = node.parent
            while aux != None and aux.left.smin > -k: 
                if aux.right == node:
                    k -= aux.left.weight
                node = aux
                aux = node.parent
            if aux == None:
                return None
            aux = aux.left
            while not aux.is_leaf:
                if aux.left.smin <= -k:
                    aux = aux.right
                else:
                    k -= aux.right.weight
                    aux = aux.left
            ponte = aux
        else:
            ponte = node
        aux = ponte.parent
        max = None
        while aux != None:
            if aux.right == ponte:
                ponte = aux
                aux = ponte.parent
            else:
                if max == None:
                    max = aux.right.fvmax
                if aux.right.fvmax != None and aux.right.fvmax.value > max.value:
                    max = aux.right.fvmax
                ponte = aux
                aux = ponte.parent
        return max

    def minK(self, t):
        node = self.ABBB
        k = 0
        while not node.is_leaf:
            if node.left.max_left_time < t:
                k += self.Weight(node.left)
                node = node.right
            else:
                node = node.left
        k += node.weight
        if k != 0:
            aux = node.parent
            while aux.right == node:
                node = aux
                aux = node.parent
            while k > aux.right.weight - aux.right.smin:
                if aux.left == node:
                    k += aux.right.weight
                node = aux
                aux = node.parent
            aux = aux.right
            while not aux.is_leaf:
                if k <= aux.right.weight - aux.right.smin:
                    aux = aux.left
                else:
                    k += aux.left.weight
                    aux = aux.right
            ponte = aux
        else:
            ponte = node
        aux = ponte.parent
        if aux == None:
            return self.ABBB.fvmin
        min = None
        while aux != None:
            if aux.left == ponte:
                ponte = aux
                aux = ponte.parent
            else:
                if min == None:
                    min = aux.left.fvmin
                if aux.left.fvmin != None and aux.left.fvmin.value < min.value:
                    min = aux.left.fvmin
                ponte = aux
                aux = ponte.parent
        return min
        
    def Search(self, time):
        node = self.ABBB
        while not node.is_leaf:
            if node.max_left_time < time:
                node = node.right
            else:
                node = node.left
        return node
            

    def Print(self):
        self.PrintAux(self.ABBB, 0)

    def PrintAux(self, node, d):
        if node == None:
            return
        self.PrintAux(node.right, d + 1)
        for i in range(d):
            print("    ", end = "")
        print(node.max_left_time, "-", node.weight)
        self.PrintAux(node.left, d + 1)
        

class HeapR:
    def __init__(self):
        self.qnow = Qnow()
        self.ops = ABBB_OP()
    
    def insert(self, t, val, op):
        if op == 1:
            max_node = self.ops.maxK(t)
            if max_node == None:
                self.ops.insert(t, val, 0)
                self.qnow.insert(val)
                return
            if max_node.value < val:
                self.ops.insert(t, val, 0)
                self.qnow.insert(val)
            else:
                max_node.weight = 0
                max_node.smin = 0
                max_node.fvmax = None
                max_node.fvmin = max_node
                aux = max_node.parent
                while aux != None:
                    self.ops.Atualiza(aux)
                    aux = aux.parent
                self.ops.insert(t, val, 1)
        else:
            min_node = self.ops.minK(t)
            min_node.weight = 1
            min_node.smin = 1
            min_node.fvmax = min_node
            min_node.fvmin = None
            aux = min_node.parent
            while aux != None:
                self.ops.Atualiza(aux)
                aux = aux.parent
            self.ops.insert(t, val, -1)
            self.qnow.delete(min_node.value)

    def delete(self, t):
        node = self.ops.Search(t)
        if node.weight == 0:
            self.ops.delete(t)
            self.qnow.delete(node.value)
        elif node.weight == 1:
            min_node = self.ops.minK(t)
            min_node.weight = 1
            min_node.smin = 1
            min_node.fvmax = min_node
            min_node.fvmin = None
            aux = min_node.parent
            while aux != None:
                self.ops.Atualiza(aux)
                aux = aux.parent
            self.ops.delete(t)
            self.qnow.delete(min_node.value)
        else:
            max_node = self.ops.maxK(t)
            if max_node == None:
                max_node = self.ops.ABBB.fvmax
            max_node.weight = 0
            max_node.smin = 0
            max_node.fvmax = None
            max_node.fvmin = max_node
            aux = max_node.parent
            while aux != None:
                self.ops.Atualiza(aux)
                aux = aux.parent
            self.ops.delete(t)
            self.qnow.insert(max_node.value)
                



    def Min(self):
        return self.qnow.Min()


heap = HeapR()
#heap.insert(3, 3, 1)
#heap.insert(0, 0, 1)
#heap.insert(2, 2, -1)
#heap.insert(1, 1, 1)
#heap.insert(5, 0, 1)
#heap.insert(4, 4, -1)
#print(heap.Min())
#heap.ops.Print()
#heap.delete(4)
#heap.ops.Print()
#print(heap.Min())
#heap.ops.Print()
heap.insert(10, 10 , 1)
heap.insert(20, 20, 1)
heap.insert(30, 30, 1)
heap.insert(25, 25, -1)
heap.insert(15, 21, 1)
heap.insert(19, 19, -1)
heap.ops.Print()

