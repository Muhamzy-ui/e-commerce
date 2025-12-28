from django.urls import path
from .views import pending_reviews

app_name = "reviews"

urlpatterns = [
    path("pending/", pending_reviews, name="pending"),
]
