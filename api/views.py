from rest_framework.generics import get_object_or_404
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, mixins
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import permissions

from rest_framework import generics


class PostListView(APIView):
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PostCreateUpdateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            thumbnail = request.data.get('thumbnail')
            if thumbnail:
                serializer.validated_data['thumbnail'] = thumbnail

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'status': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'

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
        # 1. ایجاد اتاق
        room_data = {
            "title": request.data.get("title"),
            "type": request.data.get("type"),
            "body": request.data.get("body"),
        }
        room_serializer = RoomSerializer(data=room_data, context={"request": request})
        if room_serializer.is_valid():
            room = room_serializer.save()

            # 2. ایجاد اولین پیام برای اتاق
            message_data = {"body": request.data.get("body"), "user": request.user, "room": room}

            message_serializer = MessageSerializer(data=message_data)
            if message_serializer.is_valid():
                message_serializer.save()
                return Response(room_serializer.data)
            else:
                # در صورت ناکامی بودن ایجاد پیام، اتاق را نیز حذف کنید.
                room.delete()
                return Response(message_serializer.errors)

        return Response(room_serializer.errors)
