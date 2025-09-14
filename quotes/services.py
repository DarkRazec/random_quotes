from django.db.models import F
from django.db.models.functions import Random

from quotes.models import Quote


def get_weighted_quote_id() -> int | None:
    """
    Возвращает ID случайного объекта Quote с учетом его веса
    """
    quote_id = (
        Quote.objects.annotate(weighted_random=F('weight') * Random())
        .order_by('-weighted_random')
        .values_list('id', flat=True)
        .first()
    )
    return quote_id


def get_sorted_quotes(quotes_objects, sort_method):
    """
    Сортирует переданный список объектов Quote на основе выбранного пользователем метода
    """
    match sort_method:
        case "random":
            return quotes_objects.order_by("?")
        case "viewes":
            return quotes_objects.order_by("-viewed_count", "-likes_count")
        case _:
            return quotes_objects.order_by("-likes_count", "-viewed_count")


def add_remove_relation(quote, user, value) -> None:
    """
    Добавляет/удаляет пользователя из списка quote.likes/quote.dislikes в зависимости от того, что тот нажал
    :param quote: Объект модели Quote
    :param user: Текущий пользователь
    :param value: Значение, полученное при нажатии пользователем лайка или дизлайка
    """
    actions = {
        '1': ('likes', 'dislikes'),
        '-1': ('dislikes', 'likes'),
    }

    add_field, remove_field = actions.get(value)

    add_relation = getattr(quote, add_field)
    remove_relation = getattr(quote, remove_field)

    if user in add_relation.all():
        add_relation.remove(user)
    else:
        add_relation.add(user)
        remove_relation.remove(user)
