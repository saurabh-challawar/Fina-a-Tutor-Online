from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .forms import ClientRegistrationForm, CommentForm
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json
from django.db.models import Q

# Create your views here.
def tutors(request):
    tutors = Tutor.objects.order_by('-updated_at')
    favourites = []
    strval = request.GET.get("search", False)

    if strval:
        query = Q(subjects__contains=strval)
        # query.add(Q(name__contains=strval), Q.OR)
        tutors = Tutor.objects.filter(query).select_related()[:10]

    try:
        for tutor in tutors:
            print(tutor.favourite_set.all())

    except:
        favourites = None

    context = {'tutors': tutors, 'favourites': favourites, 'search': strval}
    return render(request,'tutor/tutor_list.html', context)

@login_required(login_url='login')
def details(request, pk):
    print(pk)
    tutor = Tutor.objects.get(pk = pk)
    current_user = UserInfo.objects.get(user=request.user)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            print(comment_form)
            text = comment_form.cleaned_data['text']
            comment = Comment.objects.create(text=text, owner=current_user, tutor=tutor)
            comment.save()
            return HttpResponseRedirect(reverse('detail', args=[pk]))

    else:
        comment_form = CommentForm()

    try:
        comments = Comment.objects.filter(tutor=tutor).order_by('-updated_at')
    except:
        comments = {}
        pass

    context = {'tutor': tutor, 'comments': comments, 'current_user' : current_user, 'comment_form' : comment_form}
    return render(request,'tutor/tutor_detail.html', context)


@login_required(login_url='login')
def favourites(request):
    try:
        favourites = Favourite.objects.filter(user=request.user)
    except:
        favourites = None

    context = {'favourites': favourites}

    return render(request,'tutor/favourite_list.html', context)


def registerClientPage(request):
    user_form = UserCreationForm()
    client_form = ClientRegistrationForm()
    error_messages = []


    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        client_form = ClientRegistrationForm(request.POST, request.FILES)
        if user_form.is_valid() and client_form.is_valid():
            username = user_form.cleaned_data['username']
            user_form.save()
            user = User.objects.get(username=username)
            name = client_form.cleaned_data['name']
            email = client_form.cleaned_data['email']
            image = client_form.cleaned_data['image']
            userInfo = UserInfo.objects.create(user=user, name= name, email= email, image=image)
            userInfo.save()
            client = Client.objects.create(userInfo=userInfo)
            client.save()
            return redirect('login')
        else:
            error_messages.append('Registration Unsuccessful.')
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('all'))

    context = {'user_form': user_form, 'client_form': client_form, 'error_meaages': error_messages}
    return render(request, 'tutor/register_client.html', context)


def loginPage(request):
    error_messages = []
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')


        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'User logged in')
            return redirect('all')
        else:
            error_messages.append('Login credentials are incorrect.')

    else:
        if request.user.is_authenticated:

            return HttpResponseRedirect(reverse('all'))
    context = {'error_messages':error_messages}
    return render(request, 'tutor/login.html', context)

def logoutPage(request):
    logout(request)
    return redirect('login')

def updateFavs(request):
    data = json.loads(request.body)
    action = data['action']
    tutorId = data['tutorId']
    tutor = Tutor.objects.get(id=tutorId)
    if action == 'unFavourite':
        favourite_item = Favourite.objects.get(user=request.user, tutor=tutor)
        favourite_item.delete()
    elif action == 'favourite':
        favourite_item = Favourite.objects.create(user=request.user, tutor=tutor)
        favourite_item.save()
    return JsonResponse('Favourites updated.', safe=False)