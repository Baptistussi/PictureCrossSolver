#-*-coding:UTF-8-*-

class Tools: 
    def findIntersec(self,SEQ_P):
        def cross(n1,n2):
            try:
                len(n1)
                return [cross(c1,c2) for c1,c2 in zip(n1,n2)]
            except:
                truthTable=[ [-1,0,0], [0,0,0], [0,0,1] ]
                return truthTable[n1+1][n2+1]
        seq_f=SEQ_P[0]        
        for seq in SEQ_P:
            seq_f=cross(seq_f,seq)        
        return seq_f
    
    def findPossibles(self, master, SEQS):
        def isPossible(master,seq):
            if len(master)!=len(seq): return False
            else:
                possible=True
                truthTable=[ [1,1,0], [0,1,0], [0,1,1] ]
                for i in range(len(seq)):
                    possible&=truthTable[seq[i]+1][master[i]+1]
                return possible
        SEQ_P=[]
        for s in SEQS:
            if isPossible(master,s): SEQ_P.append(s)
        return SEQ_P
    
    def minlen(self,nums):
        return sum(nums)+len(nums)-1
    
    def generate(self,previous,nums,size):
        minl=self.minlen(nums)
        n=nums[0]
        SEQS=[]
        #print("Report stats:\nminl: {}\nnums: {}\nsize: {}\n".format(minl,nums,size) )   
        if len(nums)>1:
            rest=nums[1:]
            for i in range(size-minl+1):
                seq=previous+[-1]*i+[1]*n+[-1]
                SEQS.extend( self.generate(seq,rest,self.dim-len(seq)) )
            return SEQS
        else:
            for i in range(size-n+1):
                seq=previous+[-1]*i+[1]*n
                if len(seq)<self.dim: seq+=[-1]*(self.dim-len(seq))
                SEQS.append(seq)
            return SEQS

class Solver(Tools):
    def __init__(self, dim, N):
        self.dim=dim
        self.M=[[0]*dim]*dim
        self.N=N
        self.R, self.C = self.N["rows"], self.N["columns"]
        if len(self.R)!=len(self.M) or len(self.C)!=len(self.M): return False
        self.solved={ "rows": [False]*dim, "columns": [False]*dim }
        self.all_solved=False
    
    def solve_M(self):
        cont=0
        while not self.all_solved:
            cont+=1
            for i in range(self.dim):
                master=self.M[i]
                self.M[i]=self.solve_L(master, self.R[i])
            for j in range(self.dim):
                master=[self.M[k][j] for k in range(self.dim)]
                c=self.solve_L(master,self.C[j])
                for k in range(self.dim):
                    self.M[k][j]=c[k]
            self.checkSolved_M()
            print("Iteração: {}".format(cont))
    
    def solve_L(self,seq,nums):
        SEQS=self.generate([],nums,self.dim)
        #print SEQS
        SEQ_P=self.findPossibles(seq,SEQS)
        #print SEQ_P
        seq_f=self.findIntersec(SEQ_P)
        return seq_f
    
    def checkSolved_M(self):
        all_solved=True
        #check rows
        for i in range(self.dim):
            line_solved = self.checkSolved_L( self.M[i], self.R[i] )
            self.solved["rows"][i] = line_solved
            all_solved &= line_solved
        #check columns
        c=[False]*self.dim
        for j in range(self.dim):
            for k in range(self.dim):
                c[k]=self.M[k][j]
            line_solved = self.checkSolved_L( c, self.C[j] )
            self.solved["columns"][j] = line_solved
            all_solved &= line_solved
        self.all_solved=all_solved
        
    def checkSolved_L(self,seq, nums):
        cont=0
        for cell in seq:
            if cell==1: cont+=1
        return cont==sum(nums)

class Game():
    def __init__(self, userFeedN=True):
        dim=input("Dimensão: ")
        self.dim=dim        
        self.M=[["_"]*dim]*dim
        if userFeedN: self.N=self.readN(dim)
    
    def encode(self,s):
        if len(s)>1:
            return [self.encode(c) for c in s]
        else:
            t=["X","_","O"]
            return t.index(s)-1
    
    def decode(self,n):
        try:
            len(n)
            return [self.decode(c) for c in n]
        except:
            t=["_","_","O"]#X,_,O
            return t[n+1]
    
    def readN(self,d):
        def readNums(d,label):
            Ns=[] # numbers matrix
            for i in range(d):
                nl=raw_input("{} {}: ".format(label,i+1)).split(",")
                Ns.append( [int(ns) for ns in nl] )
            return Ns    
        columnNums=readNums(d,"Coluna")
        rowNums=readNums(d,"Linha")
        return {"rows":rowNums,"columns":columnNums}
    
    def get_M(self, Mex):
        if len(Mex)!=self.dim:
            print("Dimensões diferentes!")
            return False
        else:
            for i in range(self.dim): 
                self.M[i]=self.decode(Mex[i])
            return True
    
    def imprime(self):
        letters=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'][:self.dim]
        print("\t"+" ".join(letters))
        for i in range(self.dim): 
            print("{}:\t".format(i)+" ".join(self.M[i]))
