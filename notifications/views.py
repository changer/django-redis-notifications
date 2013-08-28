from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.conf import settings
from .backends.web_notifications import remove_notification, get_notification

def read_notification(request, notification_id):
    notification = get_notification(request.user, notification_id)
    remove_notification(request.user, notification_id)
    if notification:
        return redirect(notification['url'])
    return redirect(reverse(settings.NOTIFICATION_READ_DEFAULT_REDIRECT))
