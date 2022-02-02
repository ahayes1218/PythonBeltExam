from django.db import models
import re, bcrypt

# Create your models here.
class UserManager(models.Manager):
    def RegistrationValidator(self, postData):
        errors = {}
        if len(postData['Fname'])<2:
            errors['FirstNameLength'] = "Your first name must be at least 2 letters long."
        if len(postData['Lname'])<2:
            errors['LastNameLength'] = "Your last name must be at least 2 letters long."
        if len(User.objects.filter(email=postData['email']))>0:
            errors['EmailExists'] = "There's a user already using this email address."
        if len(postData['password'])<8:
            errors['PasswordLength'] = "Password must at least 8 characters long."
        if postData['password'] != postData['pwconfirm']:
            errors['PasswordConfirmation'] = "Please confirm your password"
        FNAME_REGEX = re.compile(r'^[a-zA-Z]+$')
        if not FNAME_REGEX.match(postData['Fname']):
            errors['FirstName'] = "Letters only"
        LNAME_REGEX = re.compile(r'^[a-zA-Z]+$')
        if not LNAME_REGEX.match(postData['Lname']):
            errors['LastName'] = "Letters only"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['Email'] = "Invalid email address."
        return errors
    def LoginValidator(self, postData):
        errors = {}
        checkUser = User.objects.filter(email=postData['logemail'])
        if len(checkUser)<1:
            errors['NoUser'] = "Invalid Email or Password"
        elif not bcrypt.checkpw(postData['logpassword'].encode(),checkUser[0].password.encode()):
            errors['PasswordDoesNotMatch'] = "Invalid Email or Password"
        return errors



class User(models.Model):
    Fname = models.CharField(max_length=30)
    Lname = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class JobManager(models.Manager):
    def JobValidator(self, postData):
        errors = {}
        if len(postData['title']) <4:
            errors['titleLength'] = "Title must be more than 3 characters long."
        if len(postData['desc']) < 11:
            errors['descLength'] = "Description must be more than 10 characters long."
        if len(postData['location']) < 1:
            errors['locationEmpty'] = "Do not leave location empty."
        return errors

class Job(models.Model):
    title = models.CharField(max_length=60)
    desc = models.TextField()
    location = models.CharField(max_length=60)
    user = models.ForeignKey(User, related_name="jobs", default=None,on_delete=models.CASCADE)
    usersjob = models.ManyToManyField(User, related_name="myjobs")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = JobManager()