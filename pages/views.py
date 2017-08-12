from django.shortcuts import render

def show_main(request):
    return render(request, 'pages/MainPage.html', {})
# Create your views here.
