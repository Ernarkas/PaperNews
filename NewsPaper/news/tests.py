from django.test import TestCase

from django.contrib.auth.models import User
from datetime import datetime
import random
from news.models import Author, Category, Post, Comment

# Получаем нужных авторов и категории
author1 = Author.objects.get(pk=1)
author2 = Author.objects.get(pk=2)
author3 = Author.objects.get(pk=3)
author4 = Author.objects.get(pk=4)
cat1 = Category.objects.get(id=1)
cat2 = Category.objects.get(id=2)
cat3 = Category.objects.get(id=3)
cat4 = Category.objects.get(id=5)

# Создаем 15 новостей и 15 статей
for i in range(30):
    # Определяем автора и категорию для текущей статьи
    if i % 4 == 0:
        author = author1
    elif i % 4 == 1:
        author = author2
    elif i % 4 == 2:
        author = author3
    else:
        author = author4

    if i % 5 == 0:
        category = cat1
    elif i % 5 == 1:
        category = cat2
    elif i % 5 == 2:
        category = cat3
    else:
        category = cat4

    # Определяем тип текущей статьи (новость или статья)
    if i < 15:
        kind = Post.news
    else:
        kind = Post.article

    # Создаем новую статью и сохраняем ее
    post = Post.objects.create(
        author=author,
        kind=kind,
        category=category,
        title=f"Заголовок статьи {i+1}",
        content=f"Небольшое содержание статьи {i+1}"
    )

    # Добавляем несколько комментариев к статье
    for j in range(random.randint(0, 10)):
        user = User.objects.create(username=f"user_{j+1}")
        comment = Comment.objects.create(
            post=post,
            user=user,
            author=author,
            comment=f"Комментарий {j+1} к статье {i+1}"
        )

    # Обновляем рейтинг автора
    author.update_rating()

# Выводим сообщение об успешном создании статей
print("Статьи успешно созданы!")
