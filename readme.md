# Task Details

## Model:
Define models for users, posts, and comments. The Post model should include fields like title, content, author (a relation to the user), and publication date. 
The Comment model should relate to both the post and the user, including fields for the comment text and timestamp. 

## Views and URLs:
Implement views for listing all posts, viewing a single post with comments, creating new posts, and adding comments to a post. Ensure proper URL configurations. 

## Forms:
Utilize Django forms for post and comment submissions. 

## Celery Task: 
Implement a Celery task that runs periodically to delete comments older than a certain threshold (e.g., 30 days) to demonstrate background task processing. 

## Testing: 
Write basic tests for your models and views.