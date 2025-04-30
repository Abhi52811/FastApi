from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Post(BaseModel):
    """
    Pydantic model for a blog post.

    This model represents the structure of a blog post. The attributes define the 
    necessary fields for a blog post, including the title, content, publication status, and an optional rating.

    Attributes:
        title (str): The title of the blog post.
        content (str): The content or body of the blog post.
        published (bool): Flag to indicate whether the post is published or not. Defaults to `True`.
        rating (Optional[int]): An optional rating for the post. Defaults to `None`.
    """
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

# Sample in-memory data storage simulating a database
my_posts = [
    {"title": "title of post 1", "content": "content of post 1", "id": 1},
    {"title": "Favourite food", "content": "Pav bhaji", "id": 2}
]

@app.get("/")
def root():
    """
    Root endpoint.

    This endpoint serves as the root of the FastAPI application. When accessed, it returns a 
    simple message to welcome the user to the API.

    Returns:
        dict: A dictionary with a message key and a value "Hello world".
    """
    return {"message": "Hello world"}

@app.get("/posts")
def get_posts():
    """
    Fetch all blog posts.

    This endpoint retrieves all the posts stored in the in-memory `my_posts` list, simulating 
    a database. It returns all posts as a JSON response.

    Returns:
        dict: A dictionary with a key `"data"` containing a list of all posts in the `my_posts` list.
    """
    return {"data": my_posts}

@app.post("/createPosts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    """
    Create a new blog post.

    This endpoint accepts a POST request to create a new blog post. It requires a `Post` object 
    with the attributes `title`, `content`, `published`, and optionally `rating`. Upon receiving 
    the data, the function generates a random ID for the new post, appends it to the `my_posts` list, 
    and returns the newly created post.

    Args:
        post (Post): A Pydantic `Post` object that contains the details of the post being created.
    
    Returns:
        dict: A dictionary with the key `"data"`, which contains the newly created post with the 
              randomly generated `id`.
    """
    post_dict = post.dict()  # Converts the Post model into a dictionary
    post_dict['id'] = randrange(0, 100000000)  # Randomly generates a new ID for the post
    my_posts.append(post_dict)  # Adds the new post to the in-memory data storage
    return {"data": post_dict}


def find_post(id: int):
    """
    Find a post by its ID.

    This helper function searches for a post in the `my_posts` list by its `id`. If a post 
    with the specified ID exists, it returns the post as a dictionary; otherwise, it returns `None`.

    Args:
        id (int): The ID of the post to search for.

    Returns:
        dict or None: The post if found, or `None` if no post with the given ID exists.
    """
    for p in my_posts:
        if p["id"] == id:
            return p
    return None


# Now for the below 2 functions order matters as if we have id function first and 
# we then make a request for /posts/latest then it will give an error as it will take
# latest as an id on other hand if we take /posts/latest it will work as we can make both the
# call if we make call of /posts/1 then it will move to another function

@app.get("/posts/latest")
def last_post():
    """
    Fetch the latest post.

    This endpoint returns the last post from the `my_posts` list, which simulates retrieving the most 
    recent post. It fetches the last item in the list and returns it as a JSON response.

    Returns:
        dict: A dictionary with the key `"post_detail"` containing the latest post from the `my_posts` list.
    """
    n = int(len(my_posts) - 1)  # Retrieves the index of the last post
    return {"post_detail": f"{my_posts[n]}."}

# id is called path parameter
@app.get("/posts/{id}")
def get_post_by_id(id: int, response: Response):
    """
    Fetch a post by its ID.

    This endpoint retrieves a specific post based on its ID, which is provided as a path parameter. 
    If the post with the specified ID exists in the `my_posts` list, it returns the post details. 
    If not, it raises an HTTPException with a 404 status code.

    Args:
        id (int): The ID of the post to retrieve.
        response (Response): The FastAPI `Response` object, which allows modifying the response details.
    
    Returns:
        dict: A dictionary with the key `"post_detail"`, containing the post data if found.
    
    Raises:
        HTTPException: If no post with the given ID is found, it raises a 404 HTTPException with an error message.
    """
    post = find_post(id)  # Calls the helper function to search for the post
    if not post:
        # response.status_code = 404
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"messagee": f"Post with id: {id} not found."}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found.")
    # return {"post_detail": f"This is the post you're intested in {my_posts[int(id)]}."}
    # return {"post_detail": f"This is the post you're intested in {my_posts["id"]}."}
    return {"post_detail": f"{find_post(id)}."}
def find_index_post(id):
    """
    Finds the index of a post in the my_posts list by its ID.

    Args:
        id (int): ID of the post to find.

    Returns:
        int or None: Index of the post if found; otherwise, None.
    """
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i
    return None


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    """
    Deletes a post by its ID.

    Args:
        id (int): ID of the post to delete.

    Raises:
        HTTPException: If the post with the given ID is not found.

    Returns:
        Response: Empty response with status code 204 (No Content) indicating successful deletion.
    """
    index = find_index_post(id)
    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with {id} not found."
        )
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    """
    Updates an existing post by its ID.

    Args:
        id (int): ID of the post to update.
        post (Post): A Post model object containing the updated title, content, etc.

    Raises:
        HTTPException: If the post with the given ID is not found.

    Returns:
        dict: A dictionary with a key `data` containing the updated post object.
    """
    index = find_index_post(id)
    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with {id} not found."
        )
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data": post_dict}