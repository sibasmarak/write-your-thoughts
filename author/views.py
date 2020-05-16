from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Author, Blog
from work.models import Work
from django.contrib.auth.models import User
from accounts.models import NormalUser
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.

def signup_as_author(request):
    if request.method == 'POST':
        try:
            # User has info and wants an account now
            if request.POST['password1'] == request.POST['password2']:
                try:
                    user = User.objects.get(username=request.POST['username'])
                    return render(request, 'author/signup-as-author.html', {'error':
                    'Username Has Already Been Taken!'})
                except User.DoesNotExist:
                    if request.POST['coolname'] and request.POST['bio'] and request.POST['email'] and request.FILES['photo'] and request.POST['title'] and request.POST['genre'] and request.POST['type'] and request.POST['workbody']:
                        all_authors = Author.objects.all()
                        for author in all_authors:
                            if request.POST['coolname'] == author.coolname:
                                return render(request, 'author/signup-as-author.html', {'error': 'Think of a New Coolname - Yours is already taken'})

                        user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                        new_author = Author()
                        new_author.user = user
                        new_author.coolname = request.POST['coolname']
                        new_author.bio = request.POST['bio']
                        new_author.email = request.POST['email']
                        new_author.photo = request.FILES['photo']

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

                        new_normal_user = NormalUser()
                        new_normal_user.user = user
                        new_normal_user.photo = request.FILES['photo']
                        new_normal_user.email = request.POST['email']
                        new_normal_user.save()
                        new_normal_user.subscribed_author.set([])


                        return render(request, 'author/signup-as-author.html', {'msg': 'Wait For Admin Approval to become Author - read the note below'})

                    else:
                        return render(request, 'author/signup-as-author.html', {'error': 'Arrgh! Complete the Form'})

            else:
                return render(request, 'author/signup-as-author.html', {'error':
                'Password Mismatch!'})

        except:
            return render(request, 'author/signup-as-author.html', {'error': 'Arrgh! Complete the Form'})

    else:
        # USER wants to enter info
        return render(request, 'author/signup-as-author.html')


def detail_author(request, author_id, author_coolname, msg=None):
    author = get_object_or_404(Author, pk=author_id)
    u = request.user
    # check if the u has subscribed and is not the author
    subscribed_authors = None
    has_subscribed = False
    try:
        subscribed_authors = u.normaluser.subscribed_author.get(pk=author_id)
    except:
        subscribed_authors = None

    if subscribed_authors:
        has_subscribed = True

    works = author.work.filter(active=True).all()
    works = sorted(works, key=Work.get_pub_date, reverse=True)
    blogs = author.bloglinks.all()
    return render(request, 'author/author_detail.html', {'msg': msg, 'has_subscribed':has_subscribed, 'author':author, 'works':works, 'blogs':blogs})

@login_required
def subscribe(request, author_id, author_coolname):
    subscriber = request.user
    author = get_object_or_404(Author, pk=author_id)
    # subscriber wants to subscribe the author
    subscriber.normaluser.subscribed_author.add(author)
    msg = ' Congratulations! New Subscriber: ' + subscriber.username + '. Keep rocking LitWorld!'
    subject = 'Congratulations! New Subscriber'
    return email(request, author_id, author_coolname, subscriber, author, msg, subject)

def email(request, author_id, author_coolname, subscriber, author, msg, subject):
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [author.email,]
    send_mail( subject, msg, email_from, recipient_list )
    return detail_author(request, author_id, author_coolname)


@login_required
def unsubscribe(request, author_id, author_coolname):
    subscriber = request.user
    author = get_object_or_404(Author, pk=author_id)
    # subscriber wants to unsubscribe the author
    subscriber.normaluser.subscribed_author.remove(author)
    subject = 'Unsubsription Notice - We Feel Sorry'
    msg = ' ' + subscriber.username + ' has unsubscribed. We feel sorry for you. Do not lose hope - You still are our one of the best authors!'
    return email(request, author_id, author_coolname, subscriber, author, msg, subject)


def author_leader(request):
    authors = author_ordered_list = Author.objects.order_by('-rating')
    leaders = authors[:20]
    return render(request, 'author/author_leader.html', {'authors': leaders})

def subscribed_author_list(request):
    user = request.user
    subscribed_authors = user.normaluser.subscribed_author.order_by('-rating')
    return render(request, 'author/subscribed_author_list.html', {'authors':subscribed_authors})

@login_required
def create(request, author_id, author_coolname):
    if request.method == 'POST':
        author = get_object_or_404(Author, pk=author_id)
        if request.POST['title'] and request.POST['genre'] and request.POST['type'] and request.POST['workbody']:
            new_work = Work()
            new_work.author = author
            new_work.title = request.POST['title']
            new_work.genre = request.POST['genre']
            new_work.type = request.POST['type']
            new_work.body =  request.POST['workbody']
            title_words = new_work.title.split(' ')
            new_work.slug = '-'.join(title_words)
            new_work.save()

            return detail_author(request, author_id, author_coolname, msg='Wait For Admin Approval!')
        else:
            return render(request, 'author/create.html', {'error': 'Complete the Form Below!'})

    else:
        return render(request, 'author/create.html')

@login_required
def addblog(request, author_id, author_coolname):
    if request.method == 'POST':
        author = get_object_or_404(Author, pk=author_id)
        if request.POST['url'] and request.POST['sitename']:
            new_blog = Blog()
            new_blog.author = author
            new_blog.url = request.POST['url']
            new_blog.sitename = request.POST['sitename']
            new_blog.save()
            return detail_author(request, author_id, author_coolname)
        else:
            return render(request, 'author/addblog.html', {'error': 'Complete the Form Below!'})

    else:
        return render(request, 'author/addblog.html')


@login_required
def update(request, author_id, author_coolname):
    if request.method == 'POST':
            i = 0
            # if request.POST['new_coolname'] or request.FILES['new_photo'] or request.POST['new_bio']:
            author = get_object_or_404(Author, pk=author_id)
            try:
                if request.POST['new_coolname']:
                    author.coolname = request.POST['new_coolname']
                    i += 1
            except:
                pass
            try:
                if request.FILES['new_photo']:
                    author.photo = request.FILES['new_photo']
                    i += 1
            except:
                pass
            try:
                if request.POST['new_bio']:
                    author.bio = request.POST['new_bio']
                    i += 1
            except:
                pass

            try:
                if request.POST['email']:
                    author.email = request.POST['email']
                    i += 1
            except:
                pass

            if i > 0:
                author.save()
                msg = 'Successfully Updated!'
                return detail_author(request, author_id, author_coolname, msg=msg)
            else:
                return render(request, 'author/update.html', {'error': 'You Can not leave All The fields Empty!'})

    else:
        return render(request, 'author/update.html')
