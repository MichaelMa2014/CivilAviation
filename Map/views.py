from django.shortcuts import render

# Create your views here.
# 渲染index主页
def index(request):
    return render(request, 'index.html')

# 渲染航线页
def airline(request):
    return render(request, 'airline.html')