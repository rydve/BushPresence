Для запуска программы используйте ярлык на рабочем столе или BushPresence.exe
Если вы хотите использовать собственные данные в программе, вы можете изменить конфиг,
открыв его через трей правой кнопкой мыши или напрямую из корневой папки программы.
ЕСЛИ ВЫ НЕ ХОТИТЕ ИСПОЛЬЗОВАТЬ КАКИЕ-ТО ПАРАМЕТРЫ, ОСТАВЬТЕ В ИХ ЗНАЧЕНИИ ТРИ ПРОБЕЛА.
Если вы перезапустили дискорд и программа перестала работать, или она не работает по каким-то иным причинам,
попробуйте нажать в трее кнопку refresh и подождать пару секунд (иногда ожидание может доходить до 15 секунд).
Если проблемы продолжаются, напишите мне в дискорд, мой URL: rydve.
Если вы хотите добавить какие-то параметры для конфига, ниже будут указаны возможные параметры:
Parameters:
pid (int) – the process id of your game

state (str) – the user’s current status

details (str) – what the player is currently doing

start (int) – epoch time for game start

end (int) – epoch time for game end

large_image (str) – name of the uploaded image for the large profile artwork

large_text (str) – tooltip for the large image

small_image (str) – name of the uploaded image for the small profile artwork

small_text (str) – tootltip for the small image

party_id (str) – id of the player’s party, lobby, or group

party_size (list) – current size of the player’s party, lobby, or group, and the max in this format: [1,4]

join (str) – unique hashed string for chat invitations and ask to join

spectate (str) – unique hashed string for spectate button

match (str) – unique hashed string for spectate and join

instance (bool) – marks the match as a game session with a specific beginning and end

Чтобы добавить своё название активности и свои картинки, вам нужно использовать собственный Discord Application, вы можете создать его тут:
https://discord.com/developers/applications/
Далее в разделе General Information вам необходимо будет скопировать APPLICATION ID И вставить его в config.json
в строку client_id вместо имеющегося.
Для добавления своих картинок перейдите в раздел Rich Presence и добавьте Rich Presence Assets.
Далее впишите выбранное вами имя картинки в config.json в строку large_image.
