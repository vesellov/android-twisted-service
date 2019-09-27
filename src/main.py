# coding: utf8
__version__ = '0.2'

import kivy
kivy.require('1.9.1')  # replace with your current kivy version !

from kivy.app import App
from kivy.lang import Builder
from kivy.utils import platform

from jnius import autoclass


SERVICE_NAME = u'{packagename}.Service{servicename}'.format(
    packagename=u'org.twisted_sample.twistedsample',
    servicename=u'Twistedsample'
)


KV = '''
BoxLayout:
    orientation: 'vertical'
    BoxLayout:
        size_hint_y: None
        height: '50sp'
        Button:
            text: 'start service'
            on_press: app.start_service()
        Button:
            text: 'stop service'
            on_press: app.stop_service()
'''



class TwistedSampleApp(App):

    def build(self):
        self.service = None
        self.root = Builder.load_string(KV)
        return self.root

    def on_resume(self):
        if self.service:
            self.start_service()

    def start_service(self, finishing=False):
        service = autoclass(SERVICE_NAME)
        mActivity = autoclass(u'org.kivy.android.PythonActivity').mActivity
        argument = ''
        if finishing:
            argument = '{"stop_service": 1}'
        service.start(mActivity, argument)
        if finishing:
            self.service = None
        else:
            self.service = service

    def stop_service(self):
        service = autoclass(SERVICE_NAME)
        mActivity = autoclass('org.kivy.android.PythonActivity').mActivity
        service.stop(mActivity)
        self.start_service(finishing=True)


if __name__ == '__main__':
    TwistedSampleApp().run()
