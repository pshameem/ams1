from django.db import models

# Create your models here.

class Login(models.Model):
    # login_id = models.AutoField()
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    usertype = models.CharField(max_length=50)

    class Meta:
        db_table = "login"

class Teacher_subject(models.Model):
    # login_id = models.AutoField()
    subject = models.ForeignKey('Subject',on_delete=models.CASCADE)
    teacher = models.ForeignKey('Teacher',on_delete=models.CASCADE)
    class Meta:
        db_table = "teacher_subject"

class Teacher(models.Model):
    # teacher_id = models.AutoField()
    name = models.CharField(max_length=100)
    fk_login = models.ForeignKey('Login',on_delete=models.CASCADE)

    class Meta:
        db_table = "teacher"

class Subject(models.Model):
    # subject_id = models.AutoField()
    name = models.CharField(max_length=100)
    sem = models.CharField(max_length=100)

    class Meta:
        db_table = "subject"

class CourseMap(models.Model):
    # course_id = models.AutoField()
    subject_id = models.ForeignKey('Subject',on_delete=models.CASCADE)
    teacher_id = models.ForeignKey('Teacher',on_delete=models.CASCADE)

    class Meta:
        db_table = "course_map"

class Batch(models.Model):
    # batch_id = models.AutoField()
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
        
    class Meta:
        db_table = "batch"

class Student(models.Model):
    # student_id = models.AutoField()
    name = models.CharField(max_length=100)
    parent_name = models.CharField(max_length=100)
    parent_mobile = models.CharField(max_length=15)
    dob = models.DateField()
    admission_no = models.CharField(max_length=50)
    status = models.BooleanField(default=False)
    fk_batch = models.ForeignKey('Batch',on_delete=models.CASCADE)

    class Meta:
        db_table = "student"

class Attendence(models.Model):
    # attendence_id = models.AutoField()
    status = models.BooleanField(default=0)
    student_id = models.ForeignKey('Student',on_delete=models.CASCADE)
    teacher_id = models.ForeignKey('Teacher',on_delete=models.CASCADE)
    taken_on = models.DateField()
    subject_id = models.ForeignKey('Subject',on_delete=models.CASCADE)
    batch = models.ForeignKey('Batch',on_delete=models.CASCADE)
    updated_on = models.DateTimeField()
    class Meta:
        db_table = "Attendence"