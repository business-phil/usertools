from django.shortcuts import render, redirect
from .models import Email

def index(request):
    request.session.clear()
    return render(request, 'email_val/index.html')

def register(request):
    email = request.POST['email']
    reg_result = Email.emailManager.register(email)
    if reg_result[0] == True:
        request.session['alert'] = reg_result[1]
        Email.objects.create(email=email)
        return redirect('/email/success')
    else:
        request.session['alert'] = reg_result[1]
        return redirect('/email')

def success(request):
    email_query = Email.objects.all()
    context = { 'emails': email_query }
    return render(request, 'email_val/success.html', context)
