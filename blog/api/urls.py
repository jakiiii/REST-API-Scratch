from django.urls import path
from .views import BlogPostRudView


urlpatterns = [
    path('<int:pk>/', BlogPostRudView.as_view(), name='post-rud')
]
