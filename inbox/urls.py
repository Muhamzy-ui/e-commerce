# inbox/urls.py
from django.urls import path
from .views import inbox

app_name = "inbox"

urlpatterns = [
    path("", inbox, name="inbox"),
]
