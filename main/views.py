from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import SignupForm, LoginForm, MessageForm, ProfileForm
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from .models import Message

def index(request):
    return render(request, 'index.html', {'user': request.user})

def signup(request):
    if request.user.is_authenticated():
        return redirect('/')
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if not (form.data['login'] and form.data['password'] and form.data['password_1']):
            return redirect('/signup?missing')
        if form.data['password'] != form.data['password_1']:
            return redirect('/signup?passwords_not_match')
        try:
            user = User.objects.create_user(form.data['login'], password=form.data['password'])
            user.save()
        except IntegrityError:
            return redirect('/signup?login_used')
        login(request, authenticate(username=form.data['login'], password=form.data['password']))
        return redirect('/')
    else:
        return render(request, 'signup.html', {'login_used': 'login_used' in request.GET, 'missing': 'missing' in request.GET, 'passwords_not_match': 'passwords_not_match' in request.GET})


def signin(request):
    if request.user.is_authenticated():
        return redirect('/')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        user = authenticate(username=form.data['login'], password=form.data['password'])
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return redirect('/signin?login_error')
    else:
        return render(request, 'signin.html', {'login_error': 'login_error' in request.GET})

def profile(request):
    if not request.user.is_authenticated():
        return redirect('/')
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if not (form.data['old_password'] and form.data['password'] and form.data['password_1']):
            return redirect('/profile?missing')
        if authenticate(username=request.user.username, password=form.data['old_password']) is None:
            return redirect('/profile?wrong_old_pass')
        if form.data['password'] != form.data['password_1']:
            return redirect('/profile?passwords_not_match')
        request.user.set_password(form.data['password'])
        request.user.save()
        user = authenticate(username=request.user.username, password=form.data['password'])
        login(request, user)
        return redirect('/profile')
    else:
        return render(request, 'profile.html', {'name': request.user.username, 'missing': 'missing' in request.GET,
                                                      'wrong_old_pass': 'wrong_old_pass' in request.GET,
                                                      'passwords_not_match': 'passwords_not_match' in request.GET})

def logout_page(request):
    if not request.user.is_authenticated():
        return redirect('/')
    logout(request)
    return redirect('/')

def chat(request, chat_name):
    if not request.user.is_authenticated():
        return redirect('/')
    if len(User.objects.filter(username=chat_name)) == 0:
        return render(request, 'chat.html', {'chat_name': chat_name, 'chat_error': 1})
    if request.method == 'POST':
        form = MessageForm(request.POST)
        message = Message()
        message.inp = request.user.username
        message.outp = chat_name
        message.text = form.data['message']
        message.save()
    history_out = Message.objects.filter(inp=request.user.username, outp=chat_name)
    history_in = Message.objects.filter(inp=chat_name, outp=request.user.username)
    history = (history_out | history_in).order_by('time')
    return render(request, 'chat.html', {'chat_name': chat_name, 'history': history})

def chats(request):
    if not request.user.is_authenticated():
        return redirect('/')
    return render(request, 'chats.html', {'users': User.objects.all()})
