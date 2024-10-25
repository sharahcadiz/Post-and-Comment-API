##########################################################################################################
#   In this activity, we are going to try to use an external API to manipulate and play with.
#   Our end goal here is to
#   1. Understand how to get values from an API
#   2. Use the values from the API and manipulate it accordingly using Python
#   3. Create another API that utilizes multiple APIs
#   4. Return data from Python into a valid JSON string.
#

# `requests` is a module that enables users to perform API calls
# You can download this by doing pip install requests (or just install the requirements.txt file that comes with this code.)
import requests

# `json` is native module in Python that enables users to parse JSON strings into Python data types (list, dictionary, tuples, etc.)
# and vice versa. This is a native module so there is no need to install this as this comes with the installation of Python
import json 

# FastAPI imports
from fastapi import FastAPI
from typing import Optional

# Instantiates the FastAPI class
app = FastAPI()

# Example # 1: We are trying to get the values from an external API. We used a query parameter to make the API scalable to different API calls
# to the external API
@app.get("/detailed_post/{userID}")
def get_user_posts_and_comments(userID: Optional[int] = None):

    #this will fetch the user posts
    posts_response = requests.get(f"https://jsonplaceholder.typicode.com/posts?userId={userID}")
    posts = posts_response.json() #this is a list of posts for the user

    #this will fetch the comments for each post
    for post in posts:
        post_id = post['id']
        comments_response = requests.get(f"https://jsonplaceholder.typicode.com/comments?postId={post_id}")
        post['comments'] = comments_response.json()

    #this is the output format
    output = {
        "userID": userID,
        "posts":[{
            "post_title": post["title"],
            "post_body": post["body"],
            "comments": post["comments"]
        }for post in posts ]
    }
    return output #this will return the output based on the format provided above
    

@app.get("/comments/")
def get_comments(postID: Optional[int] = None):
    if postID is None:
        #this will fetch all the comments if no provided specific postID
        comments_response = requests.get("https://jsonplaceholder.typicode.com/comments")
    else:
        #this will fetch the comments for a specific post if there is provided postID
        comments_response = requests.get(f"https://jsonplaceholder.typicode.com/comments?postId={postID}")
    
    comments = comments_response.json()
    return comments #this will return the converted comments data --a json format-- into a list of dictionaries in python, where each dictionary will represent a comment


############################################################################################################
##      PUT YOUR LAB ACTIVITY 4 ANSWER BELOW
##      - Create a new API that has the following specs:
##              Endpoint: /detailed_post/{userID}
##              Method: GET
##      - Given the userID, you should show all the post of that specific user and all comments per each post.
##      - Use necessary key names based on the value to be outputted.
############################################################################################################