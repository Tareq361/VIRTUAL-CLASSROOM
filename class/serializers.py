from rest_framework import serializers
from .models import Material,student,teacher,Class
class postSerializers(serializers.ModelSerializer):
    class Meta:
        model= Material
        fields='__all__'
        created_at = serializers.DateTimeField(format="%m/%d/%Y %H:%M", required=False, read_only=True)
class studentSerializers(serializers.ModelSerializer):
    class Meta:
        model= student
        fields=['id','Fname','Lname','Email','AccountType','image']

class teacherSerializers(serializers.ModelSerializer):
    class Meta:
        model= teacher
        fields=['id','Fname','Lname','Email','AccountType','image']
class classSerializers(serializers.ModelSerializer):
    class Meta:
        model= Class
        fields=['id','name','section','class_code']
