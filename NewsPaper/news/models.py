from django.contrib.auth.models import User
from django.db import models
from datetime import datetime


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_rating = models.IntegerField(default=0)

    def update_rating(self):
        post_rating = sum(post.content_rating for post in self.posts.all())
        comment_rating = sum(comment.comment_rating for comment in self.comments.all())
        post_comment_rating = sum(
            comment.comment_rating for post in self.posts.all() for comment in post.comments.all())
        self.user_rating = post_rating * 3 + comment_rating + post_comment_rating
        self.save()

    def __str__(self):
        return self.user.username


class Category(models.Model):
    category_title = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, related_name='subscribed_categories')

    def __str__(self):
        return self.category_title


class Post(models.Model):
    news = "N"
    article = "A"
    KIND_OF_POST = [
        (news, 'новость'),
        (article, 'статья')
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    kind = models.CharField(max_length=1, choices=KIND_OF_POST)
    add_time = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, "PostCategory")
    temporary_categories = models.ManyToManyField(Category, related_name="temporary_posts")
    title = models.CharField(max_length=255)
    content = models.TextField()
    content_rating = models.IntegerField(default=0)
    comments = models.ManyToManyField('Comment', related_name='post_comments')

    def like(self):
        self.content_rating += 1
        self.save()

    def dislike(self):
        self.content_rating -= 1
        self.save()

    def preview(self):
        preview_length = 124
        if len(self.content) <= preview_length:
            return self.content
        else:
            return self.content[:preview_length] + "..."


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    add_comment = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()
