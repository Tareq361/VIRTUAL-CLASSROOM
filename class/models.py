from django.db import models
from django.urls import reverse
from django.utils import timezone #for get current time
# Create your models here.
#teacher model
class teacher(models.Model):
    Fname=models.CharField(max_length=120)
    Lname=models.CharField(max_length=120)
    Email=models.EmailField(max_length=50)
    AccountType = models.CharField(max_length=200)
    image = models.ImageField(blank=True, upload_to="profilePic/")
    Password=models.TextField()
#student model
class student(models.Model):
    Fname = models.CharField(max_length=120)
    Lname = models.CharField(max_length=120)
    Email = models.EmailField(max_length=50)
    AccountType = models.CharField(max_length=20)
    image = models.ImageField(blank=True, upload_to="profilePic/")
    Password = models.TextField()
    classJoin = models.ManyToManyField('Class')
#class model
class Class(models.Model):
    name = models.CharField(max_length=120)
    section = models.CharField(max_length=120)
    subject = models.CharField(max_length=120)
    room = models.CharField(max_length=120)
    class_code = models.CharField(max_length=120)
    teacherId = models.ForeignKey(teacher,on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    def get_absolute_url(self):      #for individul class view with dynamic link
        return reverse("class:classview",args=[self.id])
class Material(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    file = models.FileField(blank=True,upload_to="material/")
    created_at = models.DateTimeField(default=timezone.now)
    classId = models.ForeignKey(Class, on_delete=models.CASCADE)
    def get_absolute_url(self):      #for post material view with dynamic link
        return reverse("class:pdfView",args=[self.id])
class TextQuestion(models.Model):
    question=models.TextField(blank=True)
    AudioQuestion = models.FileField(blank=True, upload_to="AudioQustion/")
    student_id=models.ForeignKey(student,on_delete=models.CASCADE)
    time=models.DateTimeField(default=timezone.now)
    page_no=models.IntegerField()
    width=models.TextField(blank=True)
    top = models.TextField(blank=True)
    left = models.TextField(blank=True)
    material_id=models.ForeignKey(Material,on_delete=models.CASCADE)
class audioQuestion(models.Model):
    file=models.FileField(blank=True,upload_to="audioQ/")