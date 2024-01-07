from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import permissions


# region APIVIEW CBV
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

    def get_post(self, request, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({'status': status.HTTP_404_NOT_FOUND})

    def get(self, request, pk):

        post = self.get_post(request, pk)

        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        post = self.get_post(request, pk)

        serializer = PostSerializer(data=request.data, instance=post)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        post = self.get_post(request, pk)
        post.delete()
        return Response({'message': 'deleting post successfully'}, status=status.HTTP_200_OK)


# endregion

# region MIXINS
class PostListViewGenerics(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDetailApiViewGenerics(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


# endregion

# region VIEWSETS

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
# endregion
