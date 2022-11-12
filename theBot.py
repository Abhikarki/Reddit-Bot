import praw
import re
import os

# Get the top news as a reply
def getReply():
    s = "Top Headlines: \n  "
    a = 1
    # my_Bot from praw.ini file.
    reddit = praw.Reddit('my_Bot')
    # Get the news from subreddit 'r/news'
    subreddit = reddit.subreddit("news")
    for submission in subreddit.hot(limit = 5):
        s = s + str(a) +  ".   " 
        s = s + submission.title + "\n "
        a += 1
    return s


def main():
    reddit = praw.Reddit('my_Bot')

    # create an empty list if a file with replied posts does not exist
    if not os.path.isfile("repliedPosts.txt"):
        repliedPosts = []
    # else open the file and read the content to  the list.
    else:
        with open("repliedPosts.txt", "r") as f:
            repliedPosts = f.read()
            # Split on new lines to create a list. 
            repliedPosts = repliedPosts.split("\n")
            # Get rid of the empty values.
            repliedPosts = list(filter(None, repliedPosts))

    subreddit = reddit.subreddit('whatsnew_s')
    for submission in subreddit.hot(limit = 5):
        if submission.id not in repliedPosts:
            # Check for the phrase 'whats new'
            if re.search("whats new", submission.title, re.IGNORECASE):
                #reply to the post
                rep = getReply()
                submission.reply(rep)
                # Add the post to replied post list.
                repliedPosts.append(submission.id)

    # Update the repliedPosts file with the updated list.
    with open("repliedPosts.txt", "w") as f:
        for postId in repliedPosts:
            f.write(postId + "\n")

main()