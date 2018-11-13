from django.urls import path
from .views import BlogPostRudView, BlogPostAPIView


urlpatterns = [
    path('', BlogPostAPIView.as_view(), name='post-create'),
    path('<int:pk>/', BlogPostRudView.as_view(), name='post-rud'),
]
