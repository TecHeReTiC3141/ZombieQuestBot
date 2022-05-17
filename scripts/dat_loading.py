from bot import *
import pandas as pd

data = pd.ExcelFile('..\data.xlsx')

events = pd.read_excel(data, 'Events')

print(events.head())
cursor.execute('''DELETE FROM Event''')
for row in range(events.shape[0]):

    id, text, im, audio = events.loc[row].values.tolist()
    try:
        cursor.execute('''INSERT INTO Event
                    VALUES (?, ?, ?, ?)''', (int(id), text, im, audio))
    except Exception as e:
        print(e, events.loc[row].values.tolist())

db.commit()