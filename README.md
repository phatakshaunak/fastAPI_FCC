## API for a social media application using fastAPI
Coding an API for a dummy social media application with fastAPI with Free Code Camp's fastAPI course.

The API implements the functionalities:

1. User posts
    * Create a new post
    * Get all posts or get a post by its id
    * Delete the user's post (Only allowed for the post owner)
    * Update a user's post
2. Login Endpoints
    * Create a user account (Store passwords as a hash in a database)
    * All User posts actions are allowed only when a user is logged in
3. Endpoints for Voting on posts
    * Add or remove a vote on a specific post

Database: Used a PostgreSQL database containing tables to store users, posts and votes

Implemented database creation and revisions using an ORM (SQLAlchemy) and database migration tool (Alembic)

Deployed the API to heroku. The following link provides access for trying out all the above endpoints: https://shaunak-fastapi.herokuapp.com/docs/
