from blog_app.models import Room


def get_last_messages(request):
    messages = Room.opens.all().order_by('-created')[:5]
    return {'last_rooms': messages}
