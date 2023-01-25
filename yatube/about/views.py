from django.shortcuts import render


def about_author(request):
    return render(request, 'about/author.html')


def technologies(request):
    return render(request, 'about/tech.html')
