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
        self.start_service()
        self.root = Builder.load_string(KV)
        return self.root

    def on_resume(self):
        self.start_service()

    def start_service(self):
        service = autoclass(SERVICE_NAME)
        mActivity = autoclass(u'org.kivy.android.PythonActivity').mActivity
        argument = ''
        service.start(mActivity, argument)
        self.service = service

    def stop_service(self):
        if self.service:
            service = autoclass(SERVICE_NAME)
            mActivity = autoclass('org.kivy.android.PythonActivity').mActivity
            self.service.stop(mActivity)
            self.service = None


if __name__ == '__main__':
    TwistedSampleApp().run()
