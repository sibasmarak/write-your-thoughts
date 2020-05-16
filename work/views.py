from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from .models import Comment, Vote, Work
from author.models import Author
from datetime import date, timedelta
# Create your views here.
def home(request):
    works_unsort = Work.objects.filter(active=True)
    works = sorted(works_unsort.all(), key=Work.get_pub_date, reverse=True)
    return render(request, 'work/home.html', {'works': works})

def search(request):
    searchtext = request.GET['searchtext']
    try:
        authors = get_list_or_404(Author, coolname=searchtext)
    except:
        authors = None

    try:
        works = get_list_or_404(Work, title=searchtext)
    except:
        works = None

    error = None
    if not works and not authors:
        error = 'No Result Found'
    return render(request, 'work/searchresult.html', {'error':error, 'searchtext': searchtext,'authors':authors, 'works':works})

def detail(request, work_id, work_slug):
    work = get_object_or_404(Work, pk=work_id)
    user = request.user
    comments = work.comments.all()
    try:
        has_voted = work.votedon.get(votedby=user)
    except:
        has_voted = False
    return render(request, 'work/detail.html', {'work':work, 'comments':comments, 'has_voted': has_voted})

    # return render(request, 'work/detail.html', {'work':work,'comments':comments})

@login_required
def comment(request, work_id, work_slug):
    work = get_object_or_404(Work, pk=work_id)
    comments = work.comments.all()
    new_comment = None
    is_new_comment = False
    if comments:
        is_new_comment = True
    # Comment posted
    if request.method == 'POST':
        if request.POST['To'] and request.POST['body']:
            # Create Comment object but don't save to database yet
            new_comment = Comment()
            # Assign the current post to the comment
            new_comment.work = work
            new_comment.user = request.user
            new_comment.name = request.POST['To']
            new_comment.body = request.POST['body']
            # Save the comment to the database
            new_comment.save()
            is_new_comment = True
        else:
            error = 'Your Comment Seems Incomplete'
            return render(request, 'work/detail.html', {'work':work, 'error': error, 'comments': comments, 'is_new_comment': is_new_comment})


        comments = work.comments.all()
        msg = 'Your Comment Successfully Posted!'
        return render(request, 'work/detail.html',{'work':work, 'msg':msg, 'comments': comments, 'is_new_comment': is_new_comment})
    else:
        return render(request, 'work/detail.html',{'work':work, 'comments': comments, 'is_new_comment': is_new_comment})

@login_required
def delete_comment(request, work_id, work_slug, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.delete()
    work = get_object_or_404(Work, pk=work_id)
    comments = work.comments.all()
    msg = 'Your Comment Successfully Deleted!'
    return render(request, 'work/detail.html',{'work':work, 'msg':msg, 'comments': comments})

def thought_leaderboard(request):
    all_works = Work.objects.filter(type='Thought', active=True)
    works = sorted(all_works, key=Work.get_rating, reverse=True)
    works = works[:10]
    return render(request, 'work/leaderboard.html',{'works': works})


def poems_leaderboard(request):
    all_works = Work.objects.filter(type='Poetry', active=True)
    works = sorted(all_works, key=Work.get_rating, reverse=True)
    works = works[:10]
    return render(request, 'work/leaderboard.html',{'works': works})


def stories_leaderboard(request):
    all_works = Work.objects.filter(type='Short Story', active=True)
    works = sorted(all_works, key=Work.get_rating, reverse=True)
    works = works[:10]
    return render(request, 'work/leaderboard.html',{'works': works})


def fiction_leaderboard(request):
    all_works = Work.objects.filter(genre='Fiction', active=True)
    works = sorted(all_works, key=Work.get_rating, reverse=True)
    works = works[:10]
    return render(request, 'work/leaderboard.html',{'works': works})


def non_fiction_leaderboard(request):
    all_works = Work.objects.filter(genre='Non-Fiction', active=True)
    works = sorted(all_works, key=Work.get_rating, reverse=True)
    works = works[:10]
    return render(request, 'work/leaderboard.html',{'works': works})

def notifications(request):
    user = request.user
    subscribed_authors = user.normaluser.subscribed_author.all()
    end_date = date.today() + timedelta(days=1)
    delta = timedelta(weeks=1)
    start_date = end_date - delta
    new_works = Work.objects.none()
    for author in subscribed_authors:
        new_works = new_works | author.work.filter(pub_date__range=(start_date, end_date), active=True).all()

    new_works = sorted(new_works, key=Work.get_rating, reverse=True)
    return render(request, 'work/notifications.html',{'works': new_works})


@login_required
def delete(request, work_id, work_slug):
    work = get_object_or_404(Work, pk=work_id)
    work.delete()
    work.comments.all().delete()
    msg = 'Your Work Successfully Deleted!'

    return home(request)

@login_required
def rate(request, work_id, work_slug):
    user = request.user
    work = get_object_or_404(Work, pk=work_id)
    comments = work.comments.all()
    user_voted = work.votedon.all()
    has_voted = False
    if user in user_voted:
        has_voted = True
    print(has_voted)
    if has_voted:
        return render(request, 'work/detail.html', {'work':work, 'comments':comments, 'has_voted': has_voted})
    try:
        if not (float(request.POST['rating']) >= 0 and float(request.POST['rating']) <= 5):
            return render(request, 'work/detail.html', {'work':work, 'comments':comments, 'has_voted': has_voted, 'error': 'Rating must be between 0 and 5'})
    except:
        return render(request, 'work/detail.html', {'work':work, 'comments':comments, 'has_voted': has_voted, 'error': 'Rating must be between 0 and 5'})


    new_vote = Vote()
    new_vote.votedby = user
    new_vote.votedon = work
    new_vote.save()

    num_votes = len(work.votedon.all())
    work.rating = ( work.rating * (num_votes - 1) + float(request.POST['rating'] ) )/num_votes
    work.save()

    has_voted = True
    msg = 'You rated ' + str(request.POST['rating'])  +' successfully'
    return render(request, 'work/detail.html', {'work':work, 'comments':comments, 'has_voted':has_voted, 'msg': msg})
