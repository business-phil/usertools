from __future__ import unicode_literals
from django.db import models
from re import match

class EmailManager(models.Manager):
    def register(self, email):
        if not match(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$', email):
            return (False, "Invalid email address.")
        elif Email.objects.filter(email=email):
            return (False, "Email already in use.")
        else:
            return (True, "Success! " + str(email) + " is a valid email address!")

class Email(models.Model):
    email = models.CharField(max_length=90)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    emailManager = EmailManager()
    objects = models.Manager()
