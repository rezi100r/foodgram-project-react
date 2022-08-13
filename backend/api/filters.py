from django.core.exceptions import ValidationError
from django_filters.fields import MultipleChoiceField
from django_filters.rest_framework import FilterSet, filters
from django_filters.widgets import BooleanWidget
from recipes.models import Recipe
from rest_framework.filters import SearchFilter


class TagsMultipleChoiceField(
        MultipleChoiceField):
    def validate(self, value):
        if self.required and not value:
            raise ValidationError(
                self.error_messages['required'],
                code='required'
            )
        for val in value:
            if val in self.choices and not self.valid_value(val):
                raise ValidationError(
                    self.error_messages['invalid_choice'],
                    code='invalid_choice',
                    params={'value': val},
                )


class TagsFilter(filters.AllValuesMultipleFilter):
    field_class = TagsMultipleChoiceField


class IngredientSearchFilter(SearchFilter):
    search_param = 'name'


class RecipeFilter(FilterSet):
    author = filters.AllValuesMultipleFilter(
        field_name='author__id',
        label='Автор'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        widget=BooleanWidget(),
        label='В корзине.'
    )
    is_favorited = filters.BooleanFilter(
        widget=BooleanWidget(),
        label='В избранных.'
    )
    tags = TagsFilter(field_name='tags__slug')

    class Meta:
        model = Recipe
        fields = ['author', 'tags', 'is_in_shopping_cart', 'is_favorited']
