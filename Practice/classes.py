class student:
    college_name="NMIET"
    def __init__(self,roll_no,name,age,percente):
        self.roll_no=roll_no
        self.name=name
        self.age=age
        self.percente=percente
        self.email=self.name+str(self.roll_no)+"@"+"college_name"+"."+"in"


    def student_details(self):
        print(f"Roll no.={self.roll_no}")
        print(f"Name={self.name}")
        print(f"Age={self.age}")
        print(f"Percente={self.percente}")
        print(f"Email={self.email}")

s1=student(1,"ABC",19,98.32)

s2=student(2,"XYZ",20,48.32)

s1.student_details()
print("-----------------------------------------------------")
s2.student_details()

print(type(s1))