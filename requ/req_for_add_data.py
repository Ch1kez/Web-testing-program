import json
import sqlite3

import requests

con = sqlite3.connect(r'C:\Users\123\PycharmProjects\api_on_postgre\base\ftacommander.db')
cur = con.cursor()
con.commit()

data_tuple = cur.execute('select * from tuser').fetchall()
con.commit()
# print(data_tuple)
targets = []

#
labels = ['target', 'ulogin', 'upass', 'uorg']
for data_el in data_tuple:
    q = {}
    for i, label in enumerate(labels):
        q.update({label: data_el[i]})
    targets.append(q)

for i, target in enumerate(reversed(targets)):
    response = requests.get('http://127.0.0.1:8000/api/tusers/').json()

    req_post = requests.post('http://127.0.0.1:8000/api/tusers/', json=target)

    response_after_update = requests.get('http://127.0.0.1:8000/api/tusers/').json()

    print(f'''
    ================ Поле номер: {i} ====================
    Начальные данные:
    {json.dumps(response)}

    Отправленные данные:
    {targets}

    Данные после обновления:
    {json.dumps(response_after_update)}
    ******************************************************''')
