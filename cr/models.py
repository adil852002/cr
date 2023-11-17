from django.db import models


# Create your models here.

class Employees(models.Model):
    name=models.CharField(max_length=200)
    department=models.CharField(max_length=200)
    salary=models.PositiveIntegerField()
    email=models.EmailField(unique=True)
    age=models.PositiveIntegerField(null=True)
    contact=models.CharField(max_length=12)
    profile_pic=models.ImageField(upload_to="images",null=True)

    def __str__(self):
        return self.name