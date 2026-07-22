# 이 파일은 파이썬에서 클래스를 배우는 예제 파일입니다.
# 클래스는 '설계도'와 비슷해요.
# 설계도대로 만든 실제 물건을 객체(인스턴스)라고 해요.

# Person 클래스는 사람의 기본 정보를 담는 설계도예요.
class Person:
    # __init__ 함수는 객체를 만들 때 자동으로 실행되는 특별한 함수예요.
    # 이 함수 안에서 객체가 가진 값을 처음 만들어 줘요.
    def __init__(self, id, name):
        # id는 사람을 구분하는 번호예요.
        self.id = id
        # name은 사람의 이름이에요.
        self.name = name

    # printInfo() 함수는 저장된 정보를 화면에 보여줘요.
    def printInfo(self):
        print(f"Person: id={self.id}, name={self.name}")


# Manager 클래스는 Person 클래스를 상속받아요.
# 즉, Person이 가진 기능을 그대로 사용하면서
# 새로 title이라는 정보를 추가해요.
class Manager(Person):
    def __init__(self, id, name, title):
        # super()는 부모 클래스(Person)의 기능을 가져올 때 사용해요.
        super().__init__(id, name)
        # title은 관리자 직책을 뜻해요.
        self.title = title

    # 부모 클래스의 printInfo()를 새로 만들어서
    # id, name, title을 모두 출력해요.
    def printInfo(self):
        print(f"Manager: id={self.id}, name={self.name}, title={self.title}")


# Employee 클래스도 Person 클래스를 상속받아요.
# Employee는 skill라는 새로운 정보를 추가해요.
class Employee(Person):
    def __init__(self, id, name, skill):
        super().__init__(id, name)
        # skill는 일을 할 때 사용하는 기술이나 능력이에요.
        self.skill = skill

    # Employee의 정보도 새로 출력해요.
    def printInfo(self):
        print(f"Employee: id={self.id}, name={self.name}, skill={self.skill}")


# 이제 10개의 객체를 만들어 볼 거예요.
# 객체를 만드는 것을 '인스턴스 생성'이라고 해요.
people = [
    Person(1, "홍길동"),
    Person(2, "김철수"),
    Person(3, "이영희"),
    Person(4, "박민수"),
    Manager(5, "최지우", "팀장"),
    Manager(6, "정해인", "부장"),
    Manager(7, "한소희", "대리"),
    Employee(8, "장민호", "파이썬"),
    Employee(9, "오세훈", "Java"),
    Employee(10, "윤서연", "C++"),
]

# 리스트에 들어 있는 모든 객체를 하나씩 꺼내서 출력해요.
print("=== 객체 정보 출력 ===")
for index, person in enumerate(people, start=1):
    print(f"{index}. ", end="")
    person.printInfo()