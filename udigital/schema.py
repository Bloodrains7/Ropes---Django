import graphene
from graphene_django import DjangoObjectType

from udigital.models import User, Comment, Post


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number']


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        fields = ['user', 'comment', 'timestamp']


class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = '__all__'


class CreatePost(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        content = graphene.String(required=True)
        author_id = graphene.ID(required=True)
        publication_date = graphene.String(required=True)

    post = graphene.Field(PostType)

    def mutate(self, info, title, content, author_id, publication_date):
        author = User.objects.get(id=author_id)
        post = Post.objects.create(title=title, content=content, author=author, publication_date=publication_date)
        return CreatePost(post=post)


class CreateComment(graphene.Mutation):
    class Arguments:
        user_id = graphene.ID(required=True)
        post_id = graphene.ID(required=True)
        comment = graphene.String(required=True)

    comment = graphene.Field(CommentType)

    def mutate(self, info, user_id, post_id, comment):
        user = User.objects.get(id=user_id)
        post = Post.objects.get(id=post_id)
        comment = Comment.objects.create(user=user, post=post, comment=comment)
        comment.save()
        return CreateComment(comment=comment)


class Mutation(graphene.ObjectType):
    create_comment = CreateComment.Field()
    create_post = CreatePost.Field()


class Query(graphene.ObjectType):
    posts = graphene.List(PostType)
    users = graphene.List(UserType)

    def resolve_users(self, info):
        return User.objects.all()

    def resolve_posts(self, info):
        return Post.objects.all()


schema = graphene.Schema(query=Query, mutation=Mutation)
