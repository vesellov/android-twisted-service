# Sample Twisted web server running on your Android

Tested on Ubuntu 18.04 Desktop


#### Install dependencies

        sudo apt-get update
        sudo apt-get upgrade

        sudo apt-get install git gcc make perl pkg-config autoconf libtool protobuf-compiler
        sudo apt-get install python3-pip openjdk-8-jdk python3-venv
        sudo apt-get install zlib1g-dev libffi-dev libusb-1.0-0-dev libudev-dev
        sudo apt-get install python-zopeinterface python-twisted

        sudo pip3 install cython


#### Install buildozer

        make install_buildozer


#### Make sure to start from clean state

        make clean


#### Build APK image

        make


#### Connect and run on Android device

Enable "Developer Mode" on your Android device: https://developer.android.com/studio/debug/dev-options

Open another terminal window and run this to be able to catch Python logs from your Android:

        adb logcat | grep python


Now connect your device with USB cable and install APK file you just created:

        adb install -r bin/twistedsample-1.0.1-armeabi-v7a-debug.apk


On your device find "TwistedSample" application and start it.
You will see a lot of output in another console window and will be able to monitor the service.


#### Test Twisted server

Twisted web server is running now on your Android on port 18000.
Normally you can just open `http://localhost:18000` on same host but on Android it is different.
You need to know the IP address which you can use to actually open `localhost`.
To do that use `ifconfig` via `adb` and find another :

        adb shell ifconfig | grep "inet addr"
        inet addr:127.0.0.1  Mask:255.0.0.0 
        inet addr:xxx.xxx.xxx.xxx  P-t-P:xxx.xxx.xxx.xxx  Mask:255.255.255.0 


Now you can open web browser on your Android and open `http://xxx.xxx.xxx.xxx:18000`.

Hello, world!
