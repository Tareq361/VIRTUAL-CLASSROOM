from django.db import models
from requests import request
from django.urls import reverse
from django.utils import timezone #for get current time
# Create your models here.
#teacher model
from django.utils.crypto import get_random_string


class teacher(models.Model):
    Fname=models.CharField(max_length=120)
    Lname=models.CharField(max_length=120)
    Email=models.EmailField(max_length=50)
    AccountType = models.CharField(max_length=200)
    image = models.ImageField(blank=True, upload_to="""profilePic\\""")
    Password=models.TextField()
    def __str__(self):
        return self.Fname
#student model
class student(models.Model):
    Fname = models.CharField(max_length=120)
    Lname = models.CharField(max_length=120)
    Email = models.EmailField(max_length=50)
    AccountType = models.CharField(max_length=20)
    image = models.ImageField(blank=True, upload_to="""profilePic\\""")
    Password = models.TextField()
    classJoin = models.ManyToManyField('Class')
    def __str__(self):
        return self.Fname
#class model
class Class(models.Model):
    name = models.CharField(max_length=120)
    section = models.CharField(max_length=120)
    subject = models.CharField(max_length=120)
    room = models.CharField(max_length=120)
    class_code = models.CharField(max_length=120,default=get_random_string(length=8))
    teacherId = models.ForeignKey(teacher,on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.name
    def get_absolute_url(self):      #for individul class view with dynamic link
        return reverse("class:classview",args=[self.id])
class Material(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    file = models.FileField(blank=True,upload_to="material/")
    created_at = models.DateTimeField(default=timezone.now)
    classId = models.ForeignKey(Class, on_delete=models.CASCADE)
    dueTime= models.DateTimeField(null=True,blank=True,default=timezone.now)

    def get_question(self):
        return Question.objects.filter(material_id=self);
    def __str__(self):
        return self.title
    def get_absolute_url(self):      #for post material view with dynamic link
        return reverse("class:pdfView",args=[self.id])
    def get_absolute_url_material(self):      #for post material view with dynamic link
        return reverse("class:materialView",args=[self.id])
    def get_absolute_url_reviewmaterial(self):      #for post material view with dynamic link
        return reverse("class:review",args=[self.id])
class Question(models.Model):
    question=models.TextField(blank=True)
    AudioQuestion = models.FileField(blank=True, upload_to="AudioQustion/")
    #student_id=models.ForeignKey(student,on_delete=models.CASCADE)
    time=models.DateTimeField(default=timezone.now)
    page_no=models.IntegerField()
    width = models.TextField(blank=True)
    top = models.TextField(blank=True)
    left = models.TextField(blank=True)
    material_id=models.ForeignKey(Material,on_delete=models.CASCADE)
    def get_all_answer(self):

        return Answer.objects.filter(questionId=self);

    def answered(self,request):
        print("found")
        return Answer.objects.filter(questionId=self,studentId=student.objects.get(id=request.session['student_id'])).exists();

    def __str__(self):
        return self.question
class Answer(models.Model):
    questionId=models.ForeignKey(Question,on_delete=models.CASCADE)
    studentId=models.ForeignKey(student,on_delete=models.CASCADE)
    page_no = models.IntegerField()
    answer = models.TextField(blank=True)
    time = models.DateTimeField(default=timezone.now)
class readingReview(models.Model):
    materialId=models.ForeignKey(Material,on_delete=models.CASCADE)
    studentId=models.ForeignKey(student,on_delete=models.CASCADE)
    comTime=models.DateTimeField(blank=True,null=True)
    status=models.CharField(max_length=20,default="incomplete")
    def get_absolute_url_reviewmaterialstudent(self):      #for post material view with dynamic link
        return reverse("class:reviewstudent",args=[self.id])
class Image(models.Model):
    image = models.ImageField(blank=True, upload_to="""readingtimeImage\\""")
    time=models.DateTimeField(default=timezone.now)
    pageNo=models.IntegerField(default=0)
    status=models.BooleanField(default=False)
    reviewId=models.ForeignKey(readingReview,on_delete=models.CASCADE,default=0)