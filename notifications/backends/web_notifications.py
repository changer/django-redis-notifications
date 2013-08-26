from redis_cache import get_redis_connection
from time import time
from operator import itemgetter
import json

def get_user_key(user):
    return '%s:%s' % ('unread_notifications', user.id)

def get_notification_key(user, obj):
    return '%s:%s' % (obj.__class__, obj.id)

def add_notification(user, obj, message, url):
    r = get_redis_connection() 
    user_key = get_user_key(user)
    notification_key = get_notification_key(user, obj)
    r.hset(user_key, notification_key, json.dumps({
        'id': notification_key,
        'timestamp': time(),
        'message': message,
        'url': url
        }))

def send(recepients, obj, message, url):
    for recepient in recepients:
        add_notification(recepient, obj, message, url)

def get_notifications(user):
    r = get_redis_connection() 
    user_key = get_user_key(user)
    notifications = r.hgetall(user_key).values()
    notifications = [json.loads(notification) for notification in notifications]
    notifications.sort(key=itemgetter('timestamp'))
    return notifications

def remove_notification(user, notification_id):
    r = get_redis_connection() 
    user_key = get_user_key(user)
    r.hdel(user_key, notification_id)
