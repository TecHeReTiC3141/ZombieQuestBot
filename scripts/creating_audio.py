import subprocess
from bot import *
import gtts

cursor.execute('''SELECT event_id, text
            FROM Event''')

events = cursor.fetchall()

print(*events, sep='\n')
for id, text in events:
    path = f'../audio/wavs/{id}.wav'

    tts = gtts.gTTS(text, lang='ru', )
    tts.save(path)

    path_conv = f'../audio/voices/{id}.ogg'

    subprocess.run(['../ffmpeg/bin/ffmpeg.exe', '-i', path, path_conv])



