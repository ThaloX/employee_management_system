from django.db import models
from django.contrib.auth.models import User


class EmployeeDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sccode = models.CharField(max_length=10, null=True)
    empdep = models.CharField(max_length=50, null=True)
    function = models.CharField(max_length=100, null=True)
    joindate = models.CharField(max_length=50, null=True)
    gender = models.CharField(max_length=50, null=True)
    contact = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.user.username


class EmployeeEducation(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    degree = models.CharField(max_length=100)
    institution = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(blank=True)
    certificates = models.FileField(upload_to='certificates/', blank=True, null=True)

    def __str__(self):
        return self.employee.username


class EmployeeExperience(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.CharField(max_length=200)
    position = models.CharField(max_length=100)
    start_date = models.DateField(null=True)  # Allow null values
    end_date = models.DateField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.employee.username
