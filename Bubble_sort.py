lst = [2,4,3,1,7,5,8,6]
n = len(lst)
for i in range(n-1,0,-1):
    for j in range(0,i):
        if lst[j] > lst[j+1]:
            Temp = lst[j]
            lst[j] = lst[j+1]
            lst[j+1] = Temp
print(lst)