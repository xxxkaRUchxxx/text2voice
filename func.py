import sqlite3
import key
import datetime
import whisper
import os

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
    model = whisper.load_model("base")
    audio = whisper.load_audio(f'voices/{file_name}.ogg')
    audio = whisper.pad_or_trim(audio)
    mel = whisper.log_mel_spectrogram(audio).to(model.device)
    options = whisper.DecodingOptions(language='ru')
    result = whisper.decode(model, mel, options)
    os.remove(f'voices/{file_name}.ogg')
    return result.text