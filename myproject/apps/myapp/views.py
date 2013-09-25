from django.shortcuts import render
from django.http import HttpResponse
from models import User


def index(request):
    if request.user.is_authenticated():
        user = User.objects.get(username=request.user)
    else:
        user = None
    return render(request, 'index.html', {'user': user})


def login_error(request):
    return HttpResponse()
