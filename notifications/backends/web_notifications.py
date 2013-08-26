from redis_cache import get_redis_connection

def get_user_key(user):
    return '%s:%s' % ('unread_notifications', user.id)

def get_notification_key(user, obj):
    return '%s:%s' % (obj.__class__, obj.id)

def add_notification(user, obj, message, url):
    r = get_redis_connection() 
    user_key = get_user_key(user)
    notification_key = get_notification_key(user, obj)
    r.hset(user_key, notification_key, message)
    set_notification_url(notification_key, url)

def get_notification_url(notification_id):
    r = get_redis_connection() 
    return r.hget('notification_urls', notification_id)

def set_notification_url(notification_id, url):
    r = get_redis_connection() 
    r.hset('notification_urls', notification_id, url)

def send(recepients, obj, message, url):
    for recepient in recepients:
        add_notification(recepient, obj, message, url)

def get_notifications(user):
    r = get_redis_connection() 
    user_key = get_user_key(user)
    notifications = r.hgetall(user_key)
    notifications = [ {'id': key, 'message': val, 'url': get_notification_url(key)} for key, val in notifications.items()]
    return notifications

def remove_notification(user, notification_id):
    r = get_redis_connection() 
    user_key = get_user_key(user)
    r.hdel(user_key, notification_id)
