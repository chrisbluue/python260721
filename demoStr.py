#demoStr.py

strC = """이 문자열은
여러 라인으로 
저장되어
있습니다."""

print(strC)

strA = "python"
strB = "파이썬은  강력해"
print("------------------")
print(strA)
print(strB)
print(len(strA))
print(len(strB))
print(strA[1])
print(strA[0])
print(strB[0:3])
print(strB[:3])
print(strB[-3:])
print("--------------")

#리스트
lst = ["red", "blue", "green"]
print(lst)
print(len(lst))
lst.append("white")
print(lst)
lst.remove("blue")
print(lst)
lst.extend(["yellow", "blue", "black"])
print(lst)
lst.sort()
print(lst)
print("----------------")

#Set 형식
a = {1, 2, 3, 3}
b = {3, 4, 4, 5}
print(a)
print(b)
print(type(a))
print(a.union(b))
print(a.intersection(b))
print(a.difference(b))
print("-------------------")

#Tuple 형식
tp = (100, 200, 300)
print(type(tp))
print(len(tp))
print(tp[0])
print(tp.index(300))
print(tp.count(200))
print("---------------")

