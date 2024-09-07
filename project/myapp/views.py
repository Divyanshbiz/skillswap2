from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django import forms 
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password, make_password
from .models import Member, VideoConference  # Ensure you import VideoConference from the correct models file
import random
from django.shortcuts import render, get_object_or_404
from myapp.models.VideoConference import VideoConference
from django.utils import timezone



def index(request):
    return render(request,'index.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        profile_pic = request.FILES.get('profile_pic')  # Get the uploaded profile picture

        # Check if username already exists
        if Member.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken!')
            return render(request, 'signup.html', {'error': 'Username already taken!'})

        # Create the new Member object
        member = Member(
            username=username,
            firstname=firstname,
            lastname=lastname,
            email=email,
            password=make_password(password),  # Hash the password before saving
            profile_pic=profile_pic  # Save the profile picture
        )
        member.save()

        # Set user_id in session without logging in the user
        request.session['user_id'] = member.id

        messages.success(request, 'User registered successfully! Please select your skills.')
        return redirect('store_skills')  # Redirect to store_skills after successful signup

    return render(request, 'signup.html')


def store_skills(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        if not user_id:
            messages.error(request, 'Session expired or user not logged in.')
            return redirect('signup')

        try:
            member = Member.objects.get(id=user_id)
        except Member.DoesNotExist:
            messages.error(request, 'Member not found. Please sign up again.')
            return redirect('signup')

        selected_skills = request.POST.getlist('skills')  # konsi skills select ke he unke list
        print(f"Selected skills: {selected_skills}") 

        # skills ko comma se alag kar ke store kar na 
        member.skills = ','.join(selected_skills)
        member.save()

        print(f"Stored skills: {member.skills}")  

        messages.success(request, 'Skills saved successfully!')
        return redirect('home')

    else:
        return render(request, 'store_skills.html')


# ------------------------------------ going from the Member table ------------------------------------------------------>

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']

        try:
            user = Member.objects.get(username=username)
            # login ho jaye too
            request.session['logged_in'] = True
            request.session['user_id'] = user.id  # user ke id jo ke db se aaye he 
            messages.success(request, 'You have been Logged In!')
            return redirect('home')
        except Member.DoesNotExist:
            messages.error(request, 'User does not exist. Please signup.')
            return render(request,'login.html',{'error':'User does not exist.Check your Username/Password or Please signup if new user.'})


    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    messages.success(request,("You have been Logged Out"))
    return render (request, 'index.html')

#------------------------ home page functions ----------------------------------

def home(request):
    user_id = request.session.get('user_id')
    
    if user_id:
        try:
            member = Member.objects.get(id=user_id)
            username = member.username
            first = member.firstname
            last = member.lastname
            skills = member.skills.split(',') if member.skills else [] 
            profile_pic_url = member.profile_pic.url if member.profile_pic and member.profile_pic.name else '/media/profile_pics/default-pic.png'
        except Member.DoesNotExist:
            username = first = last = ""
            skills = []
            profile_pic_url = '/media/profile_pics/default-pic.png'
    else:
        username = first = last = ""
        skills = []
        profile_pic_url = '/media/profile_pics/default-pic.png'
    
    # Automatically update the is_active status
    now = timezone.now()
    VideoConference.objects.filter(is_active=True, start_time__lt=now).update(is_active=False)

    # Fetch active video conferences, ordered by creation time (newest first)
    vcs = VideoConference.objects.filter(is_active=True).order_by('-created_at')

    # Safely handle the thumbnail and profile_pic URLs for each vc
    for vc in vcs:
        vc.thumbnail_url = vc.thumbnail.url if vc.thumbnail and vc.thumbnail.name else '/media/thumbnails/default-thumbnail.png'
        vc.profile_pic_url = vc.host.profile_pic.url if vc.host.profile_pic and vc.host.profile_pic.name else '/media/profile_pics/default-pic.png'

    return render(request, 'home.html', {
        'username': username,
        'first': first,
        'last': last,
        'skills': skills,
        'profile_pic_url': profile_pic_url,
        'vcs': vcs  # Pass the video conferences to the template
    })


#---------------------------------- Profile page -----------------------------------------

def profile(request):
    user_id = request.session.get('user_id')  # Get the user ID from the session
    
    if user_id:
        try:
            member = Member.objects.get(id=user_id)
            username = member.username
            first = member.firstname
            last = member.lastname
            skills = member.skills.split(',') if member.skills else []

            # Get the profile picture URL, or use the default image if not set
            profile_pic_url = member.profile_pic.url if member.profile_pic else '/media/profile_pics/default-pic.png'
        except Member.DoesNotExist:
            username = first = last = None
            skills = []
            profile_pic_url = '/media/profile_pics/default-pic.png'
    else:
        username = first = last = None
        skills = []
        profile_pic_url = '/media/profile_pics/default-pic.png'

    return render(request, 'profile.html', {
        'username': username,
        'first': first,
        'last': last,
        'skills': skills,
        'profile_pic_url': profile_pic_url  # Pass the profile picture URL to the template
    })


#---------------------------------- vc page -----------------------------------------



def create(request):
    user_id = request.session.get('user_id')
    
    if user_id:
        member = Member.objects.get(id=user_id)
        username = member.username
        first = member.firstname
        last = member.lastname
        profile_pic_url = member.profile_pic.url if member.profile_pic and member.profile_pic.name else '/media/profile_pics/default-pic.png'
    else:
        username = first = last = ""
        profile_pic_url = '/media/profile_pics/default-pic.png'
    
    if request.method == 'POST':
        title = request.POST['title']
        category = request.POST['category']
        start_time = request.POST['start_time']
        thumbnail = request.FILES.get('thumbnail')
        
        room_id = str(random.randint(1000, 9999))  # Generate a unique room ID
        
        vc = VideoConference.objects.create(
            title=title,
            category=category,
            start_time=start_time,
            thumbnail=thumbnail,
            host=member,
            room_id=room_id
        )
        
        return redirect('home')  # Redirect to the home page or wherever you want
    
    # Pass profile information to the template
    return render(request, 'create.html', {
        'username': username,
        'first': first,
        'last': last,
        'profile_pic_url': profile_pic_url  # Pass the profile picture URL
    })

def start_vc(request, vc_id):
    vc = get_object_or_404(VideoConference, id=vc_id)

    # Fetch the member details from the session
    user_id = request.session.get('user_id')
    if user_id:
        member = Member.objects.get(id=user_id)

        context = {
            'room_id': vc.room_id,
            'user_id': str(member.id),
            'user_name': member.username,  # Use the Member's username
        }

        return render(request, 'start_vc.html', context)
    else:
        return redirect('login')  # Redirect to login if the user is not authenticated



def join_vc(request, vc_id):
    vc = get_object_or_404(VideoConference, id=vc_id)

    user_id = request.session.get('user_id')
    if user_id:
        member = get_object_or_404(Member, id=user_id)
        user_name = member.username
    else:
        user_name = "Guest"

    context = {
        'room_id': vc.room_id,
        'user_id': str(user_id),
        'user_name': user_name,
    }
    return render(request, 'start_vc.html', context)

#---------------------------------- Update Profile page -----------------------------------------

def update(request):
    user_id = request.session.get('user_id') 

    if not user_id:
        return redirect('login')  # Redirect to login if the user is not logged in

    member = Member.objects.get(id=user_id)
    
    first = member.firstname
    last = member.lastname  
    username = member.username
    
    # Set profile_pic_url to the user's profile picture or a default image if not set
    profile_pic_url = member.profile_pic.url if member.profile_pic and member.profile_pic.name else '/media/profile_pics/default-pic.png'

    return render(request, 'update.html', {
        'username': username,
        'last': last,
        'first': first,
        'profile_pic_url': profile_pic_url  # Pass the profile picture URL to the template
    })


def update_profile(request):
    user_id = request.session.get('user_id')
    
    if not user_id:
        return redirect('login')  # login pe bhej do agar user nahi he to

    member = Member.objects.get(id=user_id)
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        profile_pic = request.FILES.get('profile_pic')

        # username ko he update karo
        if username:
            member.username = username

        # email ko he update karo
        if email:
            member.email = email

        # profile pic ko he update karo 
        if profile_pic:
            member.profile_pic = profile_pic

        member.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('home')

    return render(request, 'update_profile.html', {'member': member})


#---------------------------------- About page -----------------------------------------

def about(request):
    user_id = request.session.get('user_id') 

    if not user_id:
        return redirect('login')  # Redirect to login if the user is not logged in

    member = Member.objects.get(id=user_id)
    
    first = member.firstname
    last = member.lastname  
    username = member.username
    
    # Set profile_pic_url to the user's profile picture or a default image if not set
    profile_pic_url = member.profile_pic.url if member.profile_pic and member.profile_pic.name else '/media/profile_pics/default-pic.png'

    return render(request, 'about.html', {
        'username': username,
        'last': last,
        'first': first,
        'profile_pic_url': profile_pic_url  # Pass the profile picture URL to the template
    })

#---------------------------------- Contact page -----------------------------------------

def contact(request):
    user_id = request.session.get('user_id') 

    if not user_id:
        return redirect('login')  # Redirect to login if the user is not logged in

    member = Member.objects.get(id=user_id)
    
    first = member.firstname
    last = member.lastname  
    username = member.username
    
    # Set profile_pic_url to the user's profile picture or a default image if not set
    profile_pic_url = member.profile_pic.url if member.profile_pic and member.profile_pic.name else '/media/profile_pics/default-pic.png'

    return render(request, 'contact.html', {
        'username': username,
        'last': last,
        'first': first,
        'profile_pic_url': profile_pic_url  # Pass the profile picture URL to the template
    })
