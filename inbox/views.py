from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Message

@login_required
def inbox(request):
    messages = Message.objects.filter(user=request.user).order_by("-created_at")
    unread_count = messages.filter(is_read=False).count()

    return render(request, "inbox/inbox.html", {
        "messages": messages,
        "unread_count": unread_count
    })
