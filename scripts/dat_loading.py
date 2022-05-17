from bot import *
import pandas as pd

data = pd.ExcelFile('data.xlsx')

events = pd.read_excel(data, 'Events')

print(events.head())

for row in range(events.shape[0]):
    print(events.loc[row].values.tolist())
    cursor.execute('''INSERT INTO Event (event_id, text)
                    VALUES (?, ?)''', events.loc[row].values.tolist()[:2])

db.commit()