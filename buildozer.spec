[app]
title = Vahot App
package.name = vahotapp
package.domain = org.vahot

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 1.0
requirements = python3==3.8.5,kivy==2.1.0

orientation = portrait

presplash.filename = %(source.dir)s/presplash.png
icon.filename = %(source.dir)s/icon.png

android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

android.api = 30
android.minapi = 21
android.ndk = 23.1.7779620

android.accept_sdk_license = True
android.build_tools = 30.0.3

[buildozer]
log_level = 2
