from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from .models import NormalUser
from author.models import Author
from work.models import Work
import re
import work
from django.conf import settings
# Create your views here.
def forget(request):
    if request.method == 'POST':
        try:
            if request.POST['email']:
                nuser = NormalUser.get_object_or_404(email = request.POST['email'])
                username = nuser.user.username
                password = nuser.user.password
                email_to_send = request.POST['email']

                msg = ' Your Credentials:\n ' + 'Username: ' + str(username) + '\nPassword:' + str(password) + '\nDo not share with anyone!'
                subject = 'LitWorld Credentials'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [email_to_send,]
                send_mail( subject, msg, email_from, recipient_list )
                return render(request, 'accounts/forget.html', {'msg' : 'Check Email - Do Not share With Anyone!' })
            else:
                return render(request, 'accounts/forget.html', {'error' : 'Fill the single detail dude' })
        except:
            return render(request, 'accounts/forget.html', {'error' : 'You do not exist in LitWorld!' })
    else:
        return render(request, 'accounts/forget.html')


def convert_author(request):
    if request.method == 'POST':
        user = request.user
        if request.POST['coolname'] and request.POST['bio'] and request.POST['title'] and request.POST['genre'] and request.POST['type'] and request.POST['workbody']:
            all_authors = Author.objects.all()
            for author in all_authors:
                if request.POST['coolname'] == author.coolname:
                    return render(request, 'accounts/convert_author.html', {'error': 'Think of a New Coolname - Yours is already taken'})

            new_author = Author()
            new_author.user = user
            new_author.coolname = request.POST['coolname']
            new_author.bio = request.POST['bio']
            new_author.email = user.normaluser.email
            new_author.photo = user.normaluser.photo
            # find the damn rank
            authors = Author.objects.all()
            new_author.ranking = len(authors) + 1
            new_author.save()
            # new_author created , can be seen in admin , admin has to make active after reading the first LitPost
            new_work = Work()
            new_work.author = new_author
            new_work.title = request.POST['title']
            new_work.genre = request.POST['genre']
            new_work.type = request.POST['type']
            new_work.body =  request.POST['workbody']
            title_words = new_work.title.split(' ')
            new_work.slug = '-'.join(title_words)
            new_work.save()
            # new_work created , admin has to check and active it , then make the author active
            # auth.logout(request)
            # auth.login(request,user) - do not login - rather send the message - and ask to read carefully the note below
            user.normaluser.save()
            user.save()
            return render(request, 'accounts/convert_author.html', {'msg': 'Wait For Admin Approval to become Author - read the note below'})
        else:
            return render(request, 'accounts/convert_author.html', {'error': 'Arrgh! Complete the Form'})

    return render(request, 'accounts/convert_author.html')

def signup_info(request):
    return render(request, 'accounts/signup-info.html')


def signup_as_user(request):
    if request.method == 'POST':
        try:
            # User has info and wants an account now
            if request.POST['password1'] == request.POST['password2']:
                try:
                    user = User.objects.get(username=request.POST['username'])
                    return render(request, 'accounts/signup-as-user.html', {'error':
                    'Username Has Already Been Taken!'})
                except User.DoesNotExist:
                    if len(request.POST['password1']) < 8 or len(request.POST['password1']) > 20:
                        return render(request, 'accounts/signup-as-user.html', {'error':
                        'Provide A Strong Password!'})
                    if request.POST['email'] and request.FILES['photo']:
                        user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                        # create a new NormalUser , and assign all the values
                        new_normal_user = NormalUser()
                        new_normal_user.user = user
                        new_normal_user.photo = request.FILES['photo']
                        new_normal_user.email = request.POST['email']
                        new_normal_user.save()
                        new_normal_user.subscribed_author.set([])

                        auth.login(request,user)
                        return redirect('home')
                    else:
                        return render(request, 'accounts/signup-as-user.html', {'error':
                        'Arrgh! Complete the Form'})
            else:
                return render(request, 'accounts/signup-as-user.html', {'error':
                'Password Mismatch!'})
        except:
            return render(request, 'accounts/signup-as-user.html', {'error':
            'Arrgh! Complete the Form'})

    else:
        # USER wants to enter info
        return render(request, 'accounts/signup-as-user.html')

def login(request):
    if request.method == 'POST':

        user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])

        if user is not None:
            flag = 0
            authors = Author.objects.all()
            for author in authors:
                if author.user.username == user.username:
                    flag = 1
                    if author.active:
                        auth.login(request, user)
                        return redirect('home')

            normalusers = NormalUser.objects.all()
            if not flag:
                for normaluser in normalusers:
                    if normaluser.user.username == user.username:
                        auth.login(request, user)
                        return redirect('home')


            return render(request, 'accounts/login.html',
            {'error':'Not An Active Author - Your First LitPost was not approved!'})

        else:
            return render(request, 'accounts/login.html',
            {'error':'Username or Password incorrect'})

    else:
        return render(request, 'accounts/login.html')

def logout(request):
    # NEED TO ROUTE TO HOME PAGE
    # AND DON'T FORGET TO LOGOUT
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')
