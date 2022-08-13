from django.core.management import BaseCommand
from recipes.models import Tag


class Command(BaseCommand):
    help = 'Создание шаблонных тегов в базе данных.'

    def handle(self, *args, **kwargs):
        data = [
            {'name': 'Завтрак', 'color': '#3DD25A', 'slug': 'breakfast'},
            {'name': 'Обед', 'color': '#10B7FF', 'slug': 'lunch'},
            {'name': 'Ужин', 'color': '#F61930', 'slug': 'dinner'},
            {'name': 'Первое', 'color': '#B840CF', 'slug': 'first'},
            {'name': 'Второе', 'color': '#003153', 'slug': 'second'},
            {'name': 'Салат', 'color': '#D8FF10', 'slug': 'salad'},
        ]
        try:
            Tag.objects.bulk_create(Tag(**tag) for tag in data)
        except ValueError:
            print('Неопределенное значение.')
        except Exception:
            print('Что-то пошло не так!')
        else:
            print('Создание тегов окончено.')
