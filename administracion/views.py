# administracion/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistroForm

def home_view(request):
    return render(request, 'home.html')

def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})
