from inbox.models import Message
from reviews.models import Review

def dashboard_counts(request):
    if request.user.is_authenticated:
        return {
            "unread_messages_count": Message.objects.filter(user=request.user, is_read=False).count(),
            "pending_reviews_count": Review.objects.filter(user=request.user, rating__isnull=True).count(),
        }
    return {}
