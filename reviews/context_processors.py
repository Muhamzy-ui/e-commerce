try:
    from inbox.models import Message
except Exception:
    Message = None

from reviews.models import Review

try:
    from orders.models import OrderItem
except Exception:
    OrderItem = None

def user_sidebar_counts(request):
    if not request.user.is_authenticated:
        return {}

    if Message is not None:
        unread_messages = Message.objects.filter(
            user=request.user, is_read=False
        ).count()
    else:
        unread_messages = 0

    if OrderItem is not None:
        purchased_products = OrderItem.objects.filter(
            order__email=request.user.email
        ).values_list("product", flat=True)
    else:
        purchased_products = []

    reviewed_products = Review.objects.filter(
        user=request.user
    ).values_list("product", flat=True)

    pending_reviews = len(
        set(purchased_products) - set(reviewed_products)
    )

    return {
        "unread_messages_count": unread_messages,
        "pending_reviews_count": pending_reviews,
    }
