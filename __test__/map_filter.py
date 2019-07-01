
it = map(lambda x: print(x, end=' '),[1,2,3,4,5])

next(it)
next(it)
next(it)
next(it)
next(it)
print()
print("##################")
lst = list(map(lambda x: x**2, [1, 2, 3, 4, 5]))
print(lst)
print("##################")

list(map(lambda x: print(x, end=' '), [1, 2, 3, 4, 5]))

print()
print("##################")
# filter
print(list(filter(lambda x:x%2 == 0,[1,2,3,4])))





