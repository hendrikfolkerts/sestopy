NumCores = [[1, 2], [1, 2, 1]]
NumRepInPool = [2, 3]

#with for loop
for el in range(len(NumCores)):
    a = len(NumCores[el])
    print("a=")
    print(a)
    b = NumRepInPool[el]
    print("b=")
    print(b)

#with list comprehension
retdata = all([len(NumCores[el])==NumRepInPool[el] for el in range(len(NumCores))])
print(retdata)
