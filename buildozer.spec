[app]
title = Vahot App
package.name = vahotapp
package.domain = org.vahot

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 1.0
requirements = python3,kivy

orientation = portrait

[buildozer]
log_level = 2

[app]
presplash.filename = %(source.dir)s/presplash.png
icon.filename = %(source.dir)s/icon.png

android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

android.api = 30
android.minapi = 21
