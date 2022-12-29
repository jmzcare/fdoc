from ..models import *
from django.shortcuts import render

def index(request):
    return render(request, 'ftrace/ftrace_index.html', locals())