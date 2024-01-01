from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class PostListView(APIView):
    def get(self, request):
        serializer = PostSerializer(Post.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'status': serializer.errors})


class PostDetailView(APIView):
    def get(self, request, id):

        try:
            post = Post.objects.get(pk=id)
        except Post.DoesNotExist:
            return Response({'status': status.HTTP_404_NOT_FOUND})

        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)
