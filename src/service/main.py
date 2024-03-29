import sys

from twisted.internet import reactor
from twisted.internet import protocol
from twisted.web import server, resource

import logging
logging.basicConfig(level=logging.DEBUG)

from twisted.internet.defer import setDebugging
setDebugging(True)

from twisted.python.log import startLogging
startLogging(sys.stdout)


class Simple(resource.Resource):
    isLeaf = True

    def render_GET(self, request):
        logging.info('Hello, world!')
        return b"<html>Hello, world!</html>"


def set_auto_restart_service(restart=True):
    logging.info('set_auto_restart_service restart=%r', restart)
    from jnius import autoclass
    Service = autoclass('org.kivy.android.PythonService').mService
    Service.setAutoRestartService(restart)


def set_foreground():
    logging.info('set_foreground')
    from jnius import autoclass
    channel_id = 'org.twisted_sample.twistedsample.Twistedsample'
    Context = autoclass(u'android.content.Context')
    Intent = autoclass(u'android.content.Intent')
    PendingIntent = autoclass(u'android.app.PendingIntent')
    AndroidString = autoclass(u'java.lang.String')
    NotificationBuilder = autoclass(u'android.app.Notification$Builder')
    NotificationManager = autoclass(u'android.app.NotificationManager')
    NotificationChannel = autoclass(u'android.app.NotificationChannel')
    notification_channel = NotificationChannel(
        channel_id, AndroidString('TwistedSample Channel'.encode('utf-8')), NotificationManager.IMPORTANCE_HIGH)
    Notification = autoclass(u'android.app.Notification')
    service = autoclass('org.kivy.android.PythonService').mService
    PythonActivity = autoclass(u'org.kivy.android.PythonActivity')
    notification_service = service.getSystemService(
        Context.NOTIFICATION_SERVICE)
    notification_service.createNotificationChannel(notification_channel)
    app_context = service.getApplication().getApplicationContext()
    notification_builder = NotificationBuilder(app_context, channel_id)
    title = AndroidString("TwistedSample".encode('utf-8'))
    message = AndroidString("Application is running in background".encode('utf-8'))
    app_class = service.getApplication().getClass()
    notification_intent = Intent(app_context, PythonActivity)
    notification_intent.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP |
        Intent.FLAG_ACTIVITY_SINGLE_TOP | Intent.FLAG_ACTIVITY_NEW_TASK)
    notification_intent.setAction(Intent.ACTION_MAIN)
    notification_intent.addCategory(Intent.CATEGORY_LAUNCHER)
    intent = PendingIntent.getActivity(service, 0, notification_intent, 0)
    notification_builder.setContentTitle(title)
    notification_builder.setContentText(message)
    notification_builder.setContentIntent(intent)
    Drawable = autoclass(u"{}.R$drawable".format(service.getPackageName()))
    icon = getattr(Drawable, 'icon')
    notification_builder.setSmallIcon(icon)
    notification_builder.setAutoCancel(True)
    new_notification = notification_builder.getNotification()
    service.startForeground(1, new_notification)
    logging.info('set_foreground DONE : %r' % service)


def main():
    argument = os.environ.get('PYTHON_SERVICE_ARGUMENT', 'null')
    argument = json.loads(argument) if argument else None
    argument = {} if argument is None else argument
    logging.info('argument=%r', argument)
    if argument.get('stop_service'):
        logging.info('service to be stopped')
        return
    try:
        set_foreground()
        set_auto_restart_service()
        site = server.Site(Simple())
        srv = reactor.listenTCP(18000, site)
        logging.info('starting reactor with %r at %r' % (site, srv.getHost(), ))
        reactor.run()
        logging.info('twisted reactor stopped')
        set_auto_restart_service(False)
    except Exception:
        logging.exception('Exception in main()')
        # avoid auto-restart loop
        set_auto_restart_service(False)


if __name__ == '__main__':
    main()
    logging.info('EXIT')
