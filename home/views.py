from django.db import connection
from django.shortcuts import render


def index(request):
    return render(request, "home/index.html", {"database": connection.vendor})
