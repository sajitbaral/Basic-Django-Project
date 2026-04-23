from django.shortcuts import render, get_object_or_404, redirect
from .models import Tweet
from .forms import TweetForm

def index(request):
    return render(request, 'index.html')

def tweet_list(request):
    tweets= Tweet.objects.all().order_by('-created_at')
    return render(request, 'tweet_list.html', {'tweets':tweets})

def create_tweet(request):
    if request.method == 'POST':
        form= TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet= form.save(commit=False)
            tweet.user= request.user
            tweet.save()
            return redirect('tweet_list')
        
    else:
        form= TweetForm()

    return render(request, 'create_tweet.html', {'form':form})

def edit_tweet(request, tweet_id):
    tweet= get_object_or_404(Tweet, pk=tweet_id, user= request.user)    #here  by adding user=request.user, we prevent a "Hacker" from changing someone else's tweet just by guessing the ID number
    if request.method=='POST':
        form= TweetForm(request.POST, request.FILES, instance=tweet)    #instance=tweet updates the existing value of tweet in db. doesnot makes duplicate. It tells Django, "Don't make a new tweet; just apply these changes to the specific tweet we found in line 2
        if form.is_valid():
            tweet=form.save(commit=False)
            tweet.user= request.user
            tweet.save()
            return redirect('tweet_list')
        
    else:
        form= TweetForm(instance= tweet)                        #This runs if the user is just opening the "Edit" page for the first time (a GET request).here instance= tweet, It pre-fills the text box on our website so the user can see their old tweet while they edit it.

    return render(request, 'create_tweet.html', {'form':form})

def delete_tweet(request, tweet_id):
    tweet= get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method=='POST':
        tweet.delete()
        return redirect('tweet_list')
    
    return render(request, 'delete_tweet.html', {'tweet':tweet})