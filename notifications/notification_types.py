from .backends import web_notifications
class BaseNotificationType(object):

    def __init__(self, obj, followers):
        self.followers =followers
        self.obj = obj

    def process(self):
        """
        Accepts a list of followers and sends notifications to the recepients
        """
        raise NotImplementedError
        pass

    def send_notifications(self, recepients, message, url):
        web_notifications.send(recepients, self.obj, message, url)
