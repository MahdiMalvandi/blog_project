from rest_framework import serializers
from blog_app.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'username', 'profile', 'job', 'bio')


class CategorySerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'text', 'author', 'description')


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'user', 'post', 'body', 'created', 'replies', 'point']

    def get_replies(self, obj):
        replies = Comment.objects.filter(reply=obj)
        reply_serializer = CommentSerializer(replies, many=True)

        return reply_serializer.data


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    category = CategorySerializer()
    post_comments = serializers.SerializerMethodField()
    # short_link =
    similar_posts = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('title', 'body', 'description', 'author', 'created', 'slug', 'thumbnail', 'category', 'post_comments',
                  'similar_posts')

    # def get_short_link(self, instance ):
    #     request = self.context.get('request', None)
    #     if request is not None:
    #         short_link = request.build_absolute_uri('/')[:-1] + f'?q={instance.id}'
    #         return short_link
    #     return None

    def get_similar_posts(self, instance):
        context = self.context.get('view')
        if context is not None:
            if context.action == 'retrieve':
                similar_posts = Post.objects.select_related('author', 'category').filter(
                    category=instance.category).exclude(
                    id=instance.id)
                return PostSerializer(similar_posts, many=True, context={'request': self.context['request']}).data
        return None

    def get_post_comments(self, instance):
        if 'view' in self.context:
            print('self context', self.context['view'].action)
            if self.context['view'].action == 'retrieve':
                return CommentSerializer(instance.post_comments.all(), many=True).data
        return None


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


class CommentCreateUpdateSerializer(serializers.Serializer):
    user = serializers.CharField(max_length=1000, required=False)
    post = serializers.CharField(max_length=1000, required=False)
    body = serializers.CharField(max_length=100000, required=False)
    reply = serializers.CharField(max_length=1000, required=False)
    point = serializers.CharField(max_length=100, required=False)

    def create(self, validated_data):
        reply = Comment.objects.get(pk=validated_data['reply']) if 'reply' in validated_data else None
        user = User.objects.filter(username=validated_data['user']).first()
        post_data = validated_data['post']
        if isinstance(post_data, str):
            post = Post.objects.get(slug=post_data)
        elif isinstance(post_data, int):
            post = Post.objects.get(pk=post_data)
        else:
            raise serializers.ValidationError('Invalid post data')

        comment = Comment.objects.create(
            user=user
            , post=post
            , body=validated_data['body']
            , point=validated_data['point']
            , reply=reply

        )
        comment.save()
        return comment

    def update(self, instance, validated_data):
        fields_to_update = self.validated_data

        for field, value in fields_to_update.items():
            setattr(instance, field, value)

        instance.save()
        return instance


class MessageSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['user', 'room', 'body']

    def get_user(self, obj):
        return UserSerializer(obj.user).data

    def create(self, validated_data):
        user = self.context['request'].user
        room = validated_data['room']

        message = Message.objects.create(
            user=user,
            room=room,
            body=validated_data['body']
        )
        message.save()
        return message


class RoomSerializer(serializers.ModelSerializer):
    messages = serializers.SerializerMethodField()
    pk = serializers.IntegerField(source='id', read_only=True)
    creator = UserSerializer(read_only=True)

    class Meta:
        model = Room
        fields = ('pk', 'title', 'type', 'creator', 'messages')

    def get_messages(self, obj):
        messages = Message.objects.filter(room=obj)
        return MessageSerializer(messages, many=True).data

    def create(self, validated_data):
        user = self.context['request'].user
        title = validated_data['title']
        type_of_room = validated_data['type']

        room = Room.objects.create(
            creator=user,
            title=title,
            type=type_of_room
        )

        room.save()
        return room
