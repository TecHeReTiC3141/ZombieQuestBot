import subprocess
from bot import *
import gtts

cursor.execute('''SELECT event_id, text
            FROM Event''')

events = cursor.fetchall()

print(*events, sep='\n')
for id, text in events:
    path = f'../audio/voices/{id}.ogg'

    cursor.execute('''UPDATE Event
                    SET audio = (?)
                    WHERE event_id = (?)''', (path, id))


db.commit()



