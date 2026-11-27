import math
from random import choice


class Student:
    def __init__(self,name,chinese,math,english):
        self.name = name
        self.chinese=chinese
        self.math=math
        self.english=english
    def __str__(self):
        return f"{self.name} {self.chinese} {self.math} {self.english}"
    def update_score(self,chinese=None,math=None,english=None):
        if chinese is not None:
         self.chinese=chinese
        if math is not None:
         self.math=math
        if english is not None:
         self.english=english



# if __name__=="__main__":
#     stu = Student("陈尧", 20, "30 ", 74)
#     print(stu)
#     stu.update_score(chinese=80)
#     print(stu)


class EduManagement:
    system_version="1.0"
    system_name="Edu Management"
    def __init__(self):
        self.student_list=[]
    #添加学生成绩
    def add_student(self):
        name=input("请输入学生姓名：")
        for i in self.student_list:
            if i.name==name:
                return


        chinese=int(input("请输入学生语文成绩："))
        math=int(input("请输入学生数学成绩："))
        english=int(input("请输入学生英语成绩："))
        if 0<=chinese<=100 and 0<=math<=100 and 0<=english<=100:
         stu=Student(name,chinese,math,english)
         self.student_list.append(stu)
         print("学生成绩添加成功")
        else:
            print("各科成绩需要在0-100之间")
    def update_score(self):
        name = input("请输入要修改的学生姓名：")
        #找到学生信息然后修改
        for i in self.student_list:
            if i.name==name:
                print(f"姓名:{i.name} 语文：{i.chinese} 数学：{i.math} 英语：{i.english}")
                chinese = int(input("请输入学生语文成绩："))
                math = int(input("请输入学生数学成绩："))
                english = int(input("请输入学生英语成绩："))
                if 0 <= chinese <= 100 and 0 <= math <= 100 and 0 <= english <= 100:
                    stu = Student(name, chinese, math, english)
                    print("成绩修改成功")
                    print(f"修改后成绩：{stu}")
                    return
                else:
                    print("各科成绩需要在0-100之间")
                    return
        print("没有找到该学生信息")
    def delete_student(self):
        for i in self.student_list:
            name = input("请输入要删除的学生姓名：")

            if i.name==name:
                self.student_list.remove(i)
                print("学生信息删除成功")
                return
            print("没有找到该学生信息")
    def query_student(self):
        name = input("请输入要查询的学生姓名：")
        for i in self.student_list:
            if i.name==name:
                print(f"姓名：{i.name} 语文：{i.chinese} 数学：{i.math} 英语：{i.english}")
                return
        print("没有找到该学生信息")
    def list_student(self):
        for i in self.student_list:
            print(i)


    def run(self):
        print(f"欢迎使用教务系统{EduManagement.system_version}")
        while True:
            print()
            print("****************************************************************")
            print("1.添加学生 2.修改学生 3.删除学生 4.查询指定学生 5.查询所有学生 6.退出系统")
            print("****************************************************************")
            choice=input("请输入要执行的操作1-6:")
            match choice:
                case "1":
                    self.add_student()
                case "2":
                    self.update_score()
                case "3":
                    self.delete_student()
                case "4":
                    self.query_student()
                case "5":
                    self.list_student()
                case "6":
                    print("bye~")
                case _:
                    print("输入错误，请输入1-6之间的数字")




a=EduManagement()
a.run()













