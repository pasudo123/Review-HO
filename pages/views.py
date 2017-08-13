from django.shortcuts import render

def show_main(request):
    return render(request, 'pages/MainPage.html', {})

def show_intro(request):
    return render(request, 'pages/Intro.html', {})

def show_demo(request):
    return render(request, 'pages/Demo.html', {})