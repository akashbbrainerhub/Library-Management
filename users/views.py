from urllib import response

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from .forms import RegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.csrf import csrf_exempt

def home(request):
    if request.user.is_authenticated:
        return redirect('book_list')
    return redirect('login')


def register(request):
    if request.user.is_authenticated:
        return redirect('book_list')

    form = RegisterForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'Account created successfully.')
        return redirect('category_create')

    return render(request, 'users/register.html', {'form': form})

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()

            login(request, user)

            refresh = RefreshToken.for_user(user)
            response = redirect('book_list')
            response.set_cookie(key='access_token', value=str(refresh.access_token), httponly=True)
            print("Access token set in cookie:", str(refresh.access_token))

            # json response 
            # response = JsonResponse({
            #     'message': 'Login successful',
            #     'access_token': str(refresh.access_token),
            #     'refresh_token': str(refresh),
            # })

            return response
    else:
        form = AuthenticationForm()
    
    return render(request, 'registration/login.html', {'form': form})