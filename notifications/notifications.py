from redis_cache import get_redis_connection
from django.contrib.auth import get_user_model
from hashlib import sha1

def get_key(obj):
    key = "%s:%s" % (str(type(obj)), obj.pk)
    return sha1(key).hexdigest()

def add_follower(obj, user):
    r = get_redis_connection()
    key = get_key(obj)
    value = user.id
    r.sadd(key, value)
    return True

def get_followers(obj):
    r = get_redis_connection()
    key = get_key(obj)
    user_ids = r.smembers(key)
    users = get_user_model().objects.filter(pk__in=user_ids)
    return users

def send_notification(following_obj, notification_type_class, obj=None):
    if not obj:
        obj = following_obj
    followers = get_followers(following_obj)
    notification = notification_type_class(obj, followers)
    notification.process()
