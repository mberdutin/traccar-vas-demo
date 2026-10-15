# issue 1259: OpenID issue with push notifications

Источник: https://github.com/traccar/traccar-web/issues/1259
Срез: 2026-10-15T14:25:03.251249+00:00
Статус: closed; причина закрытия: completed.
Обновлено в GitHub: 2026-06-20T21:00:40Z.
Тематические слова: уведомления события оповещения

## Текст обращения

**Describe the bug**
I've run into a problem with the push notifications on my custom app. When the user logs in with his google account the push notifications don't work.

**To Reproduce**
Steps to reproduce the behavior:
1. Login with OpenID
2. Test Firebase Push notifications
3. Notifications don't work
1. Login with normal login
4. Test Firebase Push notifications
5. Works normally

**Expected behavior**
Push notifications working with both methods


**Smartphone (please complete the following information):**
 - Device: Pixel 5 emulator, Samsung Galaxy S20 FE, Samsung Galaxy M32
 - OS: Android
 - Browser : Chrome
 - Version ; Android 13-14

**Additional context**
I also noticed that in the app code there is " base-config cleartextTrafficPermitted="true" ". If that is turned to false notifications also stop working. Maybe that is useful to know, as OpenID also doesn't like http


## Комментарий Swell61

Источник: https://github.com/traccar/traccar-web/issues/1259#issuecomment-2317127666

I'm hitting this too with the stock Traccar Management app with a Traccar API key. If I login with OpenID (hooked into Keycloak), no notification token is given to the device and push notifications don't work. If I logout and login with a normal Traccar account, the notification token is sent and push notifications work.

## Комментарий tananaev

Источник: https://github.com/traccar/traccar-web/issues/1259#issuecomment-4759974593

I believe this is already fixed.

Полный собранный срез комментариев сохранён в локальном source-snapshot.
Содержимое обращения и предложения автора требуют проверки; не считать их ТЗ.
