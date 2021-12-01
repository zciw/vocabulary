a=[1,2,3]
b=[]
def c():
    for i in a:
        if i in b:
            print('i in b')
        else:
            b.append(i)
            return i

d = c()
print('d po raz pierszy ', d)
# d = c()
print('d poraz drugi ', d)
e = d
print('e równa sie d', e)
print(b)
