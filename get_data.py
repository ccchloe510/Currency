import requests
import sqlite3
from bs4 import BeautifulSoup
from datetime import datetime

def create_db():
    conn = sqlite3.connect('currency_rates.db')
    c = conn.cursor()
    # 创建表
    c.execute('''CREATE TABLE IF NOT EXISTS rates
                 (selling_time REAL PRIMARY KEY, currency TEXT, selling_rate REAL)''')
    conn.commit()
    conn.close()

def get_gbp_rate_and_save():
    url = 'https://www.bankofchina.com/sourcedb/whpj/enindex_1619.html'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    rows = soup.find_all('tr')
    for row in rows:
        cells = row.find_all('td')
        if cells and cells[0].get_text(strip=True) == 'GBP':
            selling_rate = cells[3].get_text(strip=True)
            selling_time = cells[6].get_text(strip=True)
            print(f"GBP Selling Rate: {selling_rate}")
            print(f"Time: {selling_time}")
            save_rate_to_db(selling_time, 'GBP', selling_rate)
            break

def save_rate_to_db(date, currency, rate):
    conn = sqlite3.connect('currency_rates.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM rates WHERE selling_time = ?", (date,))
    existing_records = c.fetchone()[0]
    if existing_records == 0:
        c.execute("INSERT INTO rates (selling_time, currency, selling_rate) VALUES (?, ?, ?)", (date, currency, rate))
        print(f"Saved {currency} rate to database.")
    print(f"Saved {currency} rate to database.")
    conn.commit()
    conn.close()


create_db()
get_gbp_rate_and_save()


