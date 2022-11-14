jo = [1,2]
bo = [3,1,4,5]
go = 'oiu'
lo = 'oiu'
#jo += [x for x in bo if x in jo]
for i in jo:
    print(i)
    if i == 2:
        jo += [x for x in bo if x in jo]
if len([x for x in jo if x in bo]) == 0:
    print('yeah')

matta = [0,8]
print(matta + [9])