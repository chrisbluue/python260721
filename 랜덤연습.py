#랜덤연습.py

import random

print(random.random())  
print(random.random())
print(random.uniform(2.0, 5.0))
print([random.randrange(20) for i in range(10)])
print([random.randrange(20) for i in range(10)])
print(random.sample(range(20), 5))

# 로또번호 만들기
print(random.sample(range(1,46),5))

from os.path import *
print(abspath("python.exe"))
print(abspath("C:\\python313\\python.exe"))
fileName = "C:\\python313\\python.exe"
if exists(fileName):
    print("파일이 존재합니다.")
    print(getsize(fileName))
else:
    print("파일이 존재하지 않습니다.")

import os
print("운영체제명:", os.name)

#파일목록
import glob
print(glob.glob("C:\\work\\*.py"))