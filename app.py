from flask import Flask, render_template, jsonify
import sqlite3
import schedule
import time
import threading
from get_data import get_gbp_rate_and_save
from email_sender import send_notification

app = Flask(__name__, static_url_path='/static')

notification_sent = False

def update_rates():
    print("Updating rates...")
    get_gbp_rate_and_save()

schedule.every(5).minutes.do(update_rates)

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

@app.route('/')
def index():
    conn = sqlite3.connect('currency_rates.db')
    c = conn.cursor()
    c.execute("SELECT * FROM rates ORDER BY selling_time DESC")
    rates = c.fetchall()
    conn.close()
    return render_template('index.html', rates=rates)

@app.route('/rates')
def get_rates():
    conn = sqlite3.connect('currency_rates.db')
    c = conn.cursor()
    c.execute("SELECT * FROM rates ORDER BY selling_time DESC LIMIT 10")
    rates = c.fetchall()
    conn.close()
    return jsonify(rates)

@app.route('/get_realtime_data')
def get_realtime_data():
    conn = sqlite3.connect('currency_rates.db')
    c = conn.cursor()
    c.execute("SELECT selling_time, selling_rate FROM rates ORDER BY selling_time DESC LIMIT 1")
    latest_data = c.fetchone() 
    conn.close()

    if latest_data:
        time, rate = latest_data
        if float(rate) < 906 and not notification_sent:
            send_notification('汇率提醒', f'汇率已经低于 906,请注意。当前汇率为 {rate}')
            notification_sent = True
        return jsonify({'time': time, 'rate': rate})
    else:
        return jsonify({'time': '', 'rate': ''})

if __name__ == '__main__':
    threading.Thread(target=run_schedule).start()
    app.run(host='0.0.0.0', port=80)



