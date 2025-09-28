[app]
title = Vahot App
package.name = vahotapp
package.domain = org.vahot

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 1.0
requirements = python3,kivy

orientation = portrait

presplash.filename = %(source.dir)s/presplash.png
icon.filename = %(source.dir)s/icon.png

android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

android.api = 34
android.minapi = 21

# ДОБАВЬТЕ ЭТИ СТРОКИ ДЛЯ РЕШЕНИЯ ПРОБЛЕМЫ С ЛИЦЕНЗИЯМИ
android.accept_sdk_license = True
android.sdk_manager_licenses = android-sdk-license, android-sdk-preview-license

# Используйте более новую версию build-tools
android.build_tools = 34.0.0

# Дополнительные рекомендуемые настройки
android.allow_backup = True
android.enable_androidx = True

[buildozer]
log_level = 2
