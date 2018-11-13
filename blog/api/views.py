from rest_framework import generics

from blog.models import Blog
from .serializer import BlogSerializers


# Create your api views here.
class BlogPostAPIView(generics.CreateAPIView):
    lookup_field = 'pk'
    serializer_class = BlogSerializers

    def get_queryset(self):
        return Blog.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BlogPostRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = BlogSerializers

    def get_queryset(self):
        return Blog.objects.all()
