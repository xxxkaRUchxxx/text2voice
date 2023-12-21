from telebot import types
import sqlite3
import key
import datetime
import os
import json
from vosk import Model, KaldiRecognizer
import soundfile as sf
import wave
import shutil


'''
users: id, count_v, balance, username, reg_time
orders: order, id, count, pay_id, order_time
'''

time_now = lambda: datetime.datetime.now().strftime('%Y.%M.%d %H:%M')


def first_join(message):
    user_id = message.chat.id
    conn = sqlite3.connect(key.db)
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM users WHERE id=?', (user_id,))
        exist = cursor.fetchone()
        if not exist:
            cursor.execute('INSERT INTO users (id, count_v, balance, username, reg_time) VALUES (?, ?, ?, ?, ?)',
                            (user_id, 0, key.new_balance, message.from_user.username, time_now()))
            conn.commit()

        cursor.execute('SELECT * FROM users WHERE id=?', (user_id,))
        answer = cursor.fetchone()
        return answer[1], answer[2]
    except Exception as e:
        print("first_join", e)
    finally:
        conn.close()

def voice_rec(file_name):
    data, samplerate = sf.read(f'voices/{file_name}.ogg')
    sf.write(f'voices/{file_name}.ogg', data, samplerate)
    os.system(f'whisper {file_name}.ogg -o voices -f txt')
    with open(f'voices/{file_name}.txt', 'r') as file:
        text = file.read()
        print(text)
