from rest_framework import serializers
from blog_app.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','first_name', 'last_name', 'email', 'username', 'profile', 'job', 'bio')


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


    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation['author'] = {"username":instance.author.username, "email": instance.author.email}
    #     return representation

class PostCreateSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('title', 'body', 'description', 'author', 'thumbnail', 'category',)

    def validate(self,attr):
        request = self.context.get('request')

        if request and 'author' in request.data:
            user_instance = User.objects.filter(username=request.data['author']).first()
            if request:
                return user_instance
        return None

    def get_category(self, obj):
        request = self.context.get('request')

        if request and 'category' in request.data:
            category_instance = Category.objects.filter(text=request.data['category']).first()
            if category_instance:
                return CategorySerializer(category_instance).data
        return None
