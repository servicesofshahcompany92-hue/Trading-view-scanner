[app]
title = Trading Scanner
package.name = tradingscanner
package.domain = org.scanner
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 0.1
requirements = python3,kivy==2.3.0,pandas,numpy,ta,requests,urllib3

orientation = portrait
fullscreen = 0

android.permissions = INTERNET, SYSTEM_ALERT_WINDOW, VIBRATE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True
