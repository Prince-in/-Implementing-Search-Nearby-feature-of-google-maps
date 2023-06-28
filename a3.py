def merge(L1,L2):
    n=len(L1)
    m=len(L2)
    i=0
    j=0
    S=[]
    while i<n and j<m:
        if L1[i][1]<=L2[j][1]:
            S.append(L1[i])
            i+=1
        else:
            S.append(L2[j])
            j+=1
    while i<n:
        S.append(L1[i])
        i+=1
    while j<m:
        S.append(L2[j])
        j+=1
    return S        
                
def mergesort(L):
    if len(L)==1:
        return L
    n=len(L)    
    return merge(mergesort(L[0:n//2]),mergesort(L[n//2:n]))    
class Node:
    def __init__(self,data):
        self.data = data
        self.right = None
        self.left = None
        self.height = 1
        self.checkleaf = False
        self.linked = None
class AVL:
    def getheight(self,root):
        if not root:
            return 0
        return root.height
    def heightbalance(self,root):
        if not root:
            return 0
        return self.getheight(root.left)-self.getheight(root.right)
    def leftrotate(self,z):
        r =  z.right
        l2 = r.left
        r.left = z
        z.right = l2
        z.height = 1 + max(self.getheight(z.left),self.getheight(z.right))
        r.height = 1 + max(self.getheight(r.left),self.getheight(r.right))
        return r
    def rightrotate(self,z):
        l =  z.left
        r2 = l.right
        l.right = z
        z.left = r2
        z.height = 1 + max(self.getheight(z.left),self.getheight(z.right))
        l.height = 1 + max(self.getheight(l.left),self.getheight(l.right))
        return l
    def insert_node(self,root,data):
        if not root:
            return Node(data)
        elif data < root.data:
            root.left = self.insert_node(root.left,data)
        else:
            root.right = self.insert_node(root.right,data)
        root.height = 1 + max(self.getheight(root.left),self.getheight(root.height))
        balancefactor = self.heightbalance(root)
        if balancefactor > 1:
            if data < root.left.data:
                return self.rightrotate(root)
            else:
                root.left = self.leftrotate(root.left)
                return self.rightrotate(root)
        if balancefactor < -1:
            if data > root.left.data:
                return self.leftrotate(root)
            else:
                root.right = self.rightrotate(root.right)
                return self.leftrotate(root)
        return root
    def delete_node(self,root,data):
        if not root:
            return root
        elif data < root.data:
            root.left = self.delete_node(root.left,data)
        elif data > root.data:
            root.right = self.delete_node(root.right,data)
        else:
            if root.left is None:
                get = root.right
                root = None
                return get
            elif root.right is None:
                get = root.left
                root = None
                return get
            get = self.getminvalue(root.right)
            root.data = get.data
            root.right = self.delete_node(root.right,get.data)
        if root is None:
            return root

    def getminvalue(self,root):
        if root is None:
            return root
        if root.left is None:
            return root
        return self.getminvalue(root.left)
def rangetree2d(arr,build = True):
    #building range tree
    if not arr:
        return None
    arr.sort()
    if len(arr) == 1:
        node = Node(arr[0])
        node.checkleaf =True
    else:
        mid = (len(arr)-1)//2
        node = Node(arr[mid])
        node.left = rangetree2d(arr[:mid+1],build)
        node.right = rangetree2d(arr[mid+1:],build)
    if build:
        node.linked = rangetree2d( sorted(arr, key=lambda x: x[1]), build=False)
        #thus stores link to each to y sorted list
    return node
def splitnodefounder(root,point_min,point_max,dim,checker_x):
    #finding split node to help in searching
    splitnode = root
    while splitnode != None:
        if dim == 1:
            node = splitnode.data
        elif dim == 2:
            if checker_x:
                node = splitnode.data[0]
            else:
                node = splitnode.data[1]
        if node > point_max:
            splitnode = splitnode.left
        elif node < point_min:
            splitnode = splitnode.right
        elif point_min <= node <=point_max :
            break
    return splitnode
def querysearch1d(tr_node,point_1,point_2,dim,checker_x = True):
    res = []
    splitnode = splitnodefounder(tr_node,point_1,point_2,dim,checker_x)
    if splitnode == None:
        return res
    elif dim == 1:
        if (point_1 <= splitnode.data <= point_2):
            res.append(splitnode.data)
    else:
        if checker_x:
            if point_1 <= splitnode.data[0] <= point_2:
                res.append(splitnode.data)
        else:
            if point_1 <= splitnode.data[1] <= point_2:
                res.append(splitnode.data)
    res += querysearch1d(splitnode.left,point_1,point_2,dim,checker_x)
    res += querysearch1d(splitnode.right,point_1,point_2,dim,checker_x)
    return res
def querysearch2d(tr_node,x_o1,x_o2,y_o1,y_o2,dim):
    #going through  cases to search
    res = []
    splitnode = splitnodefounder(tr_node,x_o1,x_o2,2,True)
    if splitnode == None:
        return res
    elif ((x_o1 <=splitnode.data[0] <= x_o2) and (y_o1 <=splitnode.data[1]<= y_o2)):
        res.append(splitnode.data)
        l = splitnode.left
        while(l!= None):
            if ((x_o1 <=l.data[0] <= x_o2) and (y_o1 <=l.data[1]<= y_o2)):
                res.append(l.data)
            if (x_o1<=l.data[0]):
                if l.right != None:
                    res += querysearch1d(l.right.linked,y_o1,y_o2,dim,False)
                l = l.left
            else:
                l = l.right
        r = splitnode.right
        while(r!= None):
            if ((x_o1 <=r.data[0] <= x_o2) and (y_o1 <=r.data[1]<= y_o2)):
                res.append(r.data)
            if (x_o2>=r.data[0]):
                if r.left != None:
                    res += querysearch1d(r.left.linked,y_o1,y_o2,dim,False)
                r = r.right
            else:
                r = r.left
        return res
    else:
        l = splitnode.left
        while(l!= None):
            if ((x_o1 <=l.data[0] <= x_o2) and (y_o1 <=l.data[1]<= y_o2)):
                res.append(l.data)
            if (x_o1<=l.data[0]):
                if l.right != None:
                    res += querysearch1d(l.right.linked,y_o1,y_o2,dim,False)
                l = l.left
            else:
                l = l.right
        r = splitnode.right
        while(r!= None):
            if ((x_o1 <=r.data[0] <= x_o2) and (y_o1 <=r.data[1]<= y_o2)):
                res.append(r.data)
            if (x_o2>=r.data[0]):
                if r.left != None:
                    res += querysearch1d(r.left.linked,y_o1,y_o2,dim,False)
                r = r.right
            else:
                r = r.left
        return (res)
class PointDatabase:
    def __init__(self,pointlist):
        self.datastr = rangetree2d(pointlist)
    def searchNearby(self,q,d):
        res =  querysearch2d(self.datastr,q[0]-d,q[0]+d,q[1]-d,q[1]+d,2)
        res_norepeat = set(res)
        return list(res_norepeat)
# pointDbObject = PointDatabase([(1,6), (2,4), (3,7), (4,9), (5,1), (6,3), (7,8), (8,10),(9,2), (10,5)])
# print(pointDbObject.searchNearby((5,5), 1))
# print(pointDbObject.searchNearby((4,8), 2))
# print(pointDbObject.searchNearby((3,7), 5))
# pointDbObject = PointDatabase([(33,22),(40,29),(38, 26), (43, 24), (5, 25), (30, 2), (29, 7), (37, 16), (51, 15), (40, 23), (23, 20), (8, 49), (34, 45), (42, 12), (32, 39), (17, 19), (12, 4)] 
# )
# print(pointDbObject.searchNearby((37,26),4))
# print(mergesort([(1,4),(4,3)]))


     
