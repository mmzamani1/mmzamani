from django.shortcuts import render

app_dir = 'mainApp'

def home_page(request):
    return render(request, f'{app_dir}/home.html')