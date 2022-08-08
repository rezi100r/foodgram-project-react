from django.db.models import F
from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_base64.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import (Ingredient, IngredientInRecipe, Recipe, Tag)
from users.models import Follow, User


class GetIsSubscribedMixin:
    """Миксина отображения подписки на пользователя"""
    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.follower.filter(author=obj.id).exists()


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор создания пользователя"""
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'password',)


class CustomUserListSerializer(GetIsSubscribedMixin, UserSerializer):
    """Сериализатор просмотра пользователя"""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed')
        read_only_fields = ('is_subscribed', )


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для тегов"""
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиентов"""
    class Meta:
        model = Ingredient
        fields = '__all__'


class GetIngredientsMixin:
    """Миксина для рецептов, получение ингредиентов"""

    def get_ingredients(self, obj):
        return obj.ingredients.values(
            'id', 'name', 'measurement_unit',
            amount=F('ingredients_amount__amount')
        )


class RecipeReadSerializer(GetIngredientsMixin, serializers.ModelSerializer):
    """Сериализатор для чтения рецепта"""
    tags = TagSerializer(many=True)
    author = CustomUserListSerializer
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.BooleanField(default=False)
    is_in_shopping_cart = serializers.BooleanField(default=False)

    class Meta:
        model = Recipe
        fields = '__all__'


class RecipeWriteSerializer(GetIngredientsMixin, serializers.ModelSerializer):
    """Сериализатор для записи рецепта"""
    tags = TagSerializer(many=True, read_only=True)
    ingredients = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = '__all__'
        read_only_fields = ('author',)

    def validate(self, data):
        ingredients = self.initial_data['ingredients']
        ingredient_list = []
        if not ingredients:
            raise serializers.ValidationError(
                'Минимально должен быть 1 ингредиент.'
            )
        for item in ingredients:
            ingredient = get_object_or_404(
                Ingredient, id=item['id']
            )
            if ingredient in ingredient_list:
                raise serializers.ValidationError(
                    'Ингредиент не должен повторяться.'
                )
            if int(item.get('amount')) < 1:
                raise serializers.ValidationError(
                    'Минимальное количество = 1'
                )
            ingredient_list.append(ingredient)
        data['ingredients'] = ingredients
        return data

    def validate_cooking_time(self, time):
        if int(time) < 1:
            raise serializers.ValidationError(
                'Минимальное время = 1'
            )
        return time

    def add_ingredients_and_tags(self, instance, **validate_data):
        ingredients = validate_data['ingredients']
        tags = validate_data['tags']
        for tag in tags:
            instance.tags.add(tag)

        for ingredient in ingredients:
            IngredientInRecipe.objects.create(
                recipe=instance,
                ingredient_id=ingredient.get('id'),
                amount=ingredient.get('amount'),
            )
        return instance

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = self.initial_data.get('tags')
        recipe = super().create(validated_data)
        return self.add_ingredients_and_tags(
            recipe, ingredients=ingredients, tags=tags
        )

    def update(self, instance, validated_data):
        instance.ingredients.clear()
        instance.tags.clear()
        ingredients = validated_data.pop('ingredients')
        tags = self.initial_data.get('tags')
        instance = self.add_ingredients_and_tags(
            instance, ingredients=ingredients, tags=tags)
        return super().update(instance, validated_data)


class RecipeAddingSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления рецепта в подписки и корзины"""
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')


class FollowSerializer(GetIsSubscribedMixin, serializers.ModelSerializer):
    """Сериализатор подписки"""
    id = serializers.ReadOnlyField(source='author.id')
    email = serializers.ReadOnlyField(source='author.email')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        queryset = obj.author.recipes.all()
        if limit:
            queryset = queryset[:int(limit)]
        return RecipeAddingSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        return obj.author.recipes.all().count()
