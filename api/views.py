from django.contrib.postgres.search import TrigramSimilarity
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, mixins
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.decorators import action, permission_classes, api_view
from rest_framework import permissions

from rest_framework import generics


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return PostCreateUpdateSerializer
        return super().get_serializer_class()


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateUpdateSerializer
    http_method_names = ['post', 'delete', 'get', 'put']

    # def get_permissions(self):
    #     if self.action == 'create':
    #         permission_classes = [permissions.IsAuthenticated]
    #     elif self.action in ['destroy']:
    #         permission_classes = [permissions.IsAdminUser]
    #     else:
    #         permission_classes = [permissions.AllowAny]
    #     return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        return Response({'detail': 'You Can Get All of the Comments'}, status=405)


class RoomView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            rooms = Room.opens.all()
        else:
            rooms = Room.objects.filter(creator=request.user)
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        room_data = {
            "title": request.data.get("title"),
            "type": request.data.get("type"),
            "body": request.data.get("body"),
            "creator": request.user
        }
        room_serializer = RoomSerializer(data=room_data, context={"request": request})
        if room_serializer.is_valid():
            room = room_serializer.save()
            message_data = {"body": request.data.get("body"), "user": request.user, "room": room.pk}

            message_serializer = MessageSerializer(data=message_data, context={"request": request})

            if message_serializer.is_valid():
                message_serializer.save()
                return Response(room_serializer.data)
            else:
                room.delete()
                return Response(message_serializer.errors)

        return Response(room_serializer.errors)


class AddMessage(APIView):
    permission_classes([IsAuthenticated])

    def post(self, request, pk):
        room = get_object_or_404(Room, pk=pk)
        data = {
            'user': request.user,
            'room': room.pk,
            'body': request.data.get("body")
        }
        message = MessageSerializer(data=data, context={"request": request})
        if message.is_valid():
            message.save()
            room = RoomSerializer(room).data
            return Response(room)
        return Response(message.errors)


class GetPostComments(APIView):
    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        comments = CommentSerializer(post.post_comments.all(), many=True)
        return Response(comments.data)


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryPostsView(APIView):
    def get(self, request, category_text):
        category = get_object_or_404(Category, text=category_text)
        serializer = PostSerializer(category.posts.all(), many=True)
        return Response({"category": CategorySerializer(category).data, 'posts': serializer.data})


class SearchView(APIView):
    def get(self, request):
        if 'q' in request.GET:

            query = request.GET.get('q')

            # Search
            results_by_title = Post.objects.annotate(similarity=TrigramSimilarity('title', query)).filter(
                similarity__gt=0.1)
            results_by_body = Post.objects.annotate(similarity=TrigramSimilarity('body', query)).filter(
                similarity__gt=0.1)

            results = (results_by_title | results_by_body).order_by("-similarity")
            return Response(PostSerializer(results, many=True).data)
        else:
            return Response({'error': 'Invalid query'}, status=status.HTTP_404_NOT_FOUND)


class UserProfileView(APIView):
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        user_posts = user.user_posts.all()
        user_serializer = UserSerializer(user)
        user_posts_serializer = PostSerializer(user_posts, many=True)
        response = {
            'user': user_serializer.data,
            'user_posts': user_posts_serializer.data
        }
        return Response(response)
