import numpy as np
#global S1
S = []

def fill(A,p,i,j,v):
    n = 9
    sn = 3
    A[i][j] = v
    p[i][j][:] = 1
    p[:,j,A[i][j]] = 1
    p[i,:,A[i][j]] = 1
    l = i // sn
    h = j // sn
    p[l*sn:(l+1)*sn,h*sn:(h+1)*sn,A[i][j]] = 1
   

def cal(A,p,depth,n):
    n = 9
    sn =3
    pp = np.zeros((n,n,n+1))
    AA = np.zeros((n,n))
    inte = 0
    p2 = 0

    while((A==0).sum()>0 and inte < 100000):
        inte += 1

        for k in range(n):
            m = p[:,:,k+1]
            t = m.sum(axis=0)
            a = np.where(t==n-1)[0]
            if len(a)>0:
                for y in a:
                    ll = m[:,y].reshape(-1).tolist()
                    
                    x = ll.index(0)
                if A[x][y] == 0:
                    fill(A,p,x,y,k+1)

            m = p[:,:,k+1]
            t = m.sum(axis=1)
            a = np.where(t==n-1)[0]
            if len(a)>0:
                for x in a:
                    ll = m[x].reshape(-1).tolist()
                    y = ll.index(0)
                if A[x][y] == 0:
                    fill(A,p,x,y,k+1)

            m = p[:,:,k+1]        
            for l in range(sn):
                for r in range(sn):
                    ma = m[l*sn:(l+1)*sn,r*sn:(r+1)*sn]
                    if ma.sum() == n-1:
                        a,b = np.where(ma==0)
                        x = l*sn+a[0]
                        y = r*sn+b[0]
                        if A[x][y] == 0:
                            fill(A,p,x,y,k+1)


        s = (p[:,:,1:].sum(axis=-1))
        
        a,b = (np.where(s==n-1))  
        if len(a) > 0:
            for idx in range(len(a)):
                x = a[idx]
                y = b[idx]
                if A[x][y] == 0:

                    try:
                        v = p[x][y][1:].tolist().index(0)+1
                    except:return 0
                    fill(A,p,x,y,v)

        if p[:,:,1:].sum() == p2: 
            if  (A==0).sum()>0 and (p[:,:,1:]==0).sum()==0:
                return 0        
            if  (A==0).sum()==0: return 1
            s = (p[:,:,1:].sum(axis=-1))
            
            relax = n-2
            while ((s==relax).sum()==0 and relax >0): relax -= 1

            a,b = (np.where(s==relax))  
            
            x = a[0]
            y = b[0]
            
            if A[x][y] == 0:
                V = p[x][y][1:].tolist()
               
                for v in range(len(V)-1,-1,-1):
                    if V[v] == 0:
                        #v = p[x][y][1:].tolist().index(0)+1

                        for i in range(n):
                            for j in range(n):
                                AA[i][j] = A[i][j]
                                
                        for i in range(n):
                            for j in range(n):
                                for k in range(n+1):
                                     pp[i][j][k] = p[i][j][k]
                        fill(A,p,x,y,v+1)
                        
                        cal(A,p,depth+1,n)
                            

                        for i in range(n):
                            for j in range(n):
                                A[i][j] = AA[i][j]

                        for i in range(n):
                            for j in range(n):
                                for k in range(n+1):
                                    p[i][j][k] = pp[i][j][k]
        
            break
        p2 = p[:,:,1:].sum() 


    if  (A==0).sum()>0 and (p[:,:,1:]==0).sum()==0:
        return 0        
    if  (A==0).sum()==0: 
        #print('result:')
        add = 1
        #print(A)
        for i in S:
            
            if ((A==i)==0).sum()==0: add = 0

        if add: S.append(A.copy())
        return 1
    
if __name__ == '__main__':
    

    n = 9
    sn = int(np.sqrt(n))
    A=np.array([[8,9,0,7,0,0,1,2,0],
                [0,0,0,0,0,3,0,0,0],
                [0,0,0,0,5,0,0,0,0],
                [9,0,0,0,0,8,0,0,0],
                [0,0,8,5,0,0,0,0,0],
                [0,5,7,1,0,9,0,0,3],
                [6,0,0,0,0,0,4,0,8],
                [0,0,0,2,0,1,0,0,0],
                [0,0,0,0,8,0,6,7,0]])

    A = np.array([[0,0,0,0,0,0,0,3,0],
                [0,0,0,1,0,9,0,0,0],
                [0,0,9,3,0,0,4,0,0],
                [2,0,0,0,0,8,0,0,0],
                [0,0,0,5,0,2,6,0,8],
                [8,0,0,6,1,4,0,0,0],
                [0,6,0,0,0,5,0,2,0],
                [0,0,5,9,0,0,0,0,0],
                [0,9,0,0,8,0,0,1,0]])

    # A=np.array([[0,0,0,0,0,9,0,7,0],
    #             [0,0,0,0,0,0,0,0,2],
    #             [0,0,0,0,5,0,0,0,0],
    #             [0,0,0,7,0,0,0,8,0],
    #             [0,0,0,0,0,2,0,5,6],
    #             [0,4,0,0,0,6,0,0,0],
    #             [0,0,0,0,0,0,0,4,5],
    #             [9,0,0,0,0,0,7,0,0],
    #             [0,8,0,2,0,0,0,0,0]])
    S = []
    p = np.zeros((n,n,n+1))
    v = np.zeros((n,n))
    v[A>0] = 1
    p[A>0] = 1 
    for i in range(n):
        for j in range(n):
            if A[i][j]>0 :
                p[:,j,A[i][j]] = 1
                p[i,:,A[i][j]] = 1
                l = i // sn
                h = j // sn
                p[l*sn:(l+1)*sn,h*sn:(h+1)*sn,A[i][j]] = 1
    print('input')
    print(A)

    cal(A,p,0)
    for idx,i in enumerate(S):
        print('result:',idx+1)
        for j in range(n):
            s = ''
            for k in range(n):
                if v[j,k] == 0:
                    s = s+'\033[1;31m %d\033[0m'%i[j,k]
                else: s = s+'\033[1;37m %d\033[0m'%i[j,k]
            print(s)
            #print('')
