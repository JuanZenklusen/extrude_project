from courses.models import Notifications

def global_consult(request):
    viewed_notifications = Notifications.objects.filter(read = True)
    not_viewed_notifications = Notifications.objects.filter(read = False)
    count_notif = not_viewed_notifications.count()

    return {'viewed_notifications': viewed_notifications, 'not_viewed_notifications': not_viewed_notifications, 'count_notif': count_notif}