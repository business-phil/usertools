from __future__ import unicode_literals
from django.db import models
from re import match, search
from bcrypt import hashpw, gensalt

class UserManager(models.Manager):
    def register(self, first_name, last_name, email, password, conf_password, csrfmiddlewaretoken):
        messagelist = []
        # Validate first_name
        first_name = first_name[0]
        if len(first_name) < 2:
            messagelist.append("First Name must be at least 2 characters long")
        elif search(r'[^a-zA-Z]', first_name):
            messagelist.append("First Name must only contain letters")
        # Validate last_name
        last_name = last_name[0]
        if len(last_name) < 2:
            messagelist.append("Last Name must be at least 2 characters long")
        elif search(r'[^a-zA-Z]', last_name):
            messagelist.append("Last Name must only contain letters")
        # Validate email
        email = email[0]
        if not match(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$', email):
            messagelist.append("Invalid email address")
        elif User.objects.filter(email=email):
            messagelist.append("Email Address already in use")
        # Validate password
        password = password[0]
        if len(password) < 8:
            messagelist.append("Password must be at least 8 characters long")
        # Validate conf_password
        conf_password = conf_password[0]
        if conf_password != password:
            messagelist.append("Password does not match")
        # Check if all validation checks passed
        if len(messagelist) == 0:
            pw_hash = hashpw(password.encode(), gensalt())
            new_user = User.objects.create(first_name=first_name, last_name=last_name, email=email, password=pw_hash)
            return (True, new_user.id)
        else:
            return (False, messagelist)
    def login(self, email, password):
        if User.objects.filter(email=email):
            user = User.objects.get(email=email)
            if hashpw(password.encode(), user.password.encode()) == user.password:
                return (True, user.id)
            else:
                return (False, "Invalid password")
        else:
            return (False, "Invalid email address")

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=90)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    userManager = UserManager()
    objects = models.Manager()
