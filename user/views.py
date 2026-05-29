from django.shortcuts import render

# Create your views here.
def register(request):
    if request.method == 'POST':
        print(request.POST)
    return render(request,"auth/register.html")