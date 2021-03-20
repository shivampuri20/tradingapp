n,k= map(int,input().split())
s=list(map(int,input().split()))
list1=[]
for i in s:
    for j in s[1:]:
        # print(i,j)
        if i==j:
            pass
        elif (i+j)%k ==0:
            pass
            # print(i,j)
        else:
            print(i,j)

print(list1)
print(len(list1))
