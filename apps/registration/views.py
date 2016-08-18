from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import User

def index(request):
    request.session.clear()
    return render(request, 'registration/index.html')

def view(request):
    if 'user_id' in request.session:
        user_query = User.objects.get(id=request.session['user_id'])
        context = { 'user': user_query }
        return render(request, 'registration/view.html', context)
    else:
        return redirect(reverse('loginreg:index'))

def create(request):
    regstatus = User.userManager.register(**request.POST)
    if regstatus[0]:
        messages.success(request, 'You have successfully registered!')
        request.session['user_id'] = regstatus[1]
        return redirect(reverse('loginreg:view-page'))
    else:
        for message in regstatus[1]:
            messages.warning(request, message)
        return redirect(reverse('loginreg:index'))

def login(request):
    loginstatus = User.userManager.login(request.POST['email'], request.POST['password'])
    if loginstatus[0]:
        request.session['user_id'] = loginstatus[1]
        return redirect(reverse('loginreg:view-page'))
    else:
        messages.warning(request, loginstatus[1])
        return redirect(reverse('loginreg:index'))
