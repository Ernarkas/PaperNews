from django import template

register = template.Library()

censored_words = ['Хуй', 'Пизда', 'Ебаться', 'Пиздец', 'Блять', 'Блядь', 'Далбаёб', 'Ебанный']


@register.filter()
def censor(value):
    if isinstance(value, str):
        for word in censored_words:
            if word.lower() in value.lower():
                value = value.replace(word, word[0] + '*' * (len(word) - 1))
        return value
    else:
        raise ValueError('Value must be a string')
