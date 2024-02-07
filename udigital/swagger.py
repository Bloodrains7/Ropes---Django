from drf_yasg import openapi

accept_language = openapi.Parameter(name='Accept-Language', in_=openapi.IN_HEADER, description='Accept Language',
                                    type=openapi.IN_HEADER)
id_param = openapi.Parameter(name='id', in_=openapi.IN_PATH, description='Id', type=openapi.TYPE_INTEGER, required=True)

fist_name = openapi.Schema(type=openapi.TYPE_STRING, description='First Name', example='John')
last_name = openapi.Schema(type=openapi.TYPE_STRING, description='Last Name', example='Doe')
title = openapi.Schema(type=openapi.TYPE_STRING, description='Title', example='World Of Warcraft')
content = openapi.Schema(type=openapi.TYPE_STRING, description='Content', example='Abc')
comment = openapi.Schema(type=openapi.TYPE_STRING, description='Comment', example='Abc')
publication_date = openapi.Schema(type=openapi.TYPE_STRING, description='Published Date', format=openapi.FORMAT_DATE,
                                example='2023-12-31')
object_id = openapi.Schema(type=openapi.TYPE_INTEGER, description='Id', example=123)
user_id = openapi.Schema(type=openapi.TYPE_INTEGER, description='User Id', example=123)
post_id = openapi.Schema(type=openapi.TYPE_INTEGER, description='Post Id', example=123)
author_id = openapi.Schema(type=openapi.TYPE_INTEGER, description='Author Id', example=123)
comment_object = openapi.Schema(type=openapi.TYPE_OBJECT, description='Comment', properties={
    'user': openapi.Schema(type=openapi.TYPE_OBJECT, description='Author', properties={
        'firstName': fist_name,
        'lastName': last_name
    }, required=['firstName', 'lastName']),
    'title': title,
    'comment': comment
}, required=['user', 'title', 'comment'])

post = openapi.Schema(type=openapi.TYPE_OBJECT, description='Post', properties={
    'id': object_id,
    'title': title,
    'author': openapi.Schema(type=openapi.TYPE_OBJECT, description='Author', properties={
        'firstName': fist_name,
        'lastName': last_name
    }, required=['firstName', 'lastName']),
    'comment': comment_object
}, required=['id', 'title', 'author'])

create_post_request = openapi.Schema(type=openapi.TYPE_OBJECT, properties={
    'title': title,
    'content': content,
    'authorId': author_id,
    'publicationDate': publication_date
}, required=['title', 'content', 'authorId', 'publishedDate'])

create_comment_request = openapi.Schema(type=openapi.TYPE_OBJECT, properties={
    'userId': user_id,
    'postId': post_id,
    'comment': comment
}, required=['userId', 'postId', 'comment'])

posts_response = openapi.Response('Response', openapi.Schema(type=openapi.TYPE_ARRAY, items=post), examples={
    'application/json': [
        {
            "id": 1,
            "title": "Java 21",
            "author": {
                "firstName": "Andy",
                "lastName": "White"
            }
        },
        {
            "id": 2,
            "title": "Deep learning v jazyku Python",
            "author": {
                "firstName": "Andy",
                "lastName": "White"
            }
        }
    ]
})
post_response = openapi.Response('Response')

success_response = openapi.Response('Response', openapi.Schema(type=openapi.TYPE_OBJECT, properties={
    'detail': openapi.Schema(type=openapi.TYPE_STRING)
}, required=['detail']), examples={
    'application/json': {'detail': 'Success'}
})
