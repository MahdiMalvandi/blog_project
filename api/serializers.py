from rest_framework import serializers
from blog_app.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'username', 'profile', 'job', 'bio')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    category = CategorySerializer()

    class Meta:
        model = Post
        fields = ('title', 'body', 'description', 'author', 'created', 'slug', 'thumbnail', 'category')


class PostCreateUpdateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100, required=False)
    author = serializers.CharField(max_length=100, required=False)
    body = serializers.CharField(max_length=100, required=False)
    description = serializers.CharField(max_length=100, required=False)
    thumbnail = serializers.ImageField(required=False)
    category = serializers.CharField(max_length=100, required=False)




    def create(self, validated_data):
        image = validated_data['thumbnail'] if validated_data['thumbnail'] else None

        author = User.objects.filter(username=validated_data['author']).first()
        category = Category.objects.filter(text=validated_data['category']).first()
        post = Post.objects.create(
            title=validated_data['title'], author=author,
            body=validated_data['body'], description=validated_data['description'],
            category=category,
            thumbnail=image
        )
        post.save()
        return post


    def update(self, instance, validated_data):
        fields_to_update = self.validated_data

        for field, value in fields_to_update.items():
             setattr(instance, field, value)

        instance.save()
        return instance

