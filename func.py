from telebot import types
import sqlite3
import key
import datetime
import os
from google.cloud import speech_v1p1beta1 as speech



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
    client = speech.SpeechClient(credentials=key.google_api)
    with open(file_name, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.OGG_OPUS,
        sample_rate_hertz=16000,
        language_code="ru-RU",  # Замените на нужный язык, если это не русский
    )

    response = client.recognize(config=config, audio=audio)

    # Извлечение текста из ответа и отправка его в чат
    for result in response.results:
        recognized_text = result.alternatives[0].transcript
        return recognized_text




