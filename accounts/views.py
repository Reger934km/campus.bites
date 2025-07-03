from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from django.shortcuts import render

def home(request):
    return render(request, 'home.html')  # Adjust the template name if needed


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # name of login path
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


# Create your views here.
