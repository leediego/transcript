import sqlite3
from datetime import datetime
import time

# https://docs.python.org/3/library/sqlite3.html
# usage: previously execute: python sqlite3-user.py to create the table user.
# Then,                      python sqlite3-transfer.py
# In transcript.db, creates the table transfer
#  and inserts a row.

# Instead saving date and time, saves seconds passed from 1970-01-01 00:00:00.

# https://sqlite.org/foreignkeys.html
# sqlite3  (Enter)                     # Starts sqlite commands
# sqlite> PRAGMA foreign_keys = ON;    # Enables FOREIGN KEY constraints
# sqlite> PRAGMA foreign_keys;         # Returns 0 if disabled, 1 if enabled.
# sqlite> PRAGMA foreign_keys = OFF;   # Disables FOREIGN KEY constraints

###########################
# 1st part of the program. Creates the table, inserts a row and shows.
con = sqlite3.connect("transcript.db")
cur = con.cursor()
cur.execute("CREATE TABLE transfer(id INTEGER PRIMARY KEY AUTOINCREMENT, currency_from CHAR(3), amount_from FLOAT, ccr_from CHAR(8), rate_from FLOAT," \
            "ccr_to CHAR(8), rate_to FLOAT, currency_to CHAR(3), amount_to FLOAT, datehour FLOAT, user_id INTEGER DEFAULT 0 REFERENCES user(id) ON DELETE SET DEFAULT)")


cur.execute("""
    INSERT INTO transfer (currency_from, amount_from, ccr_from, rate_from, ccr_to, rate_to, currency_to, amount_to, datehour, user_id)
                    VALUES("USD",        -1.0,        "usd_btc", 120000.0, "ars_btc", 156000000.0, "ARS",  1300.0,  1753307181.351104, 1)
""")
con.commit()


for row in cur.execute("SELECT id, currency_from, amount_from, ccr_from, rate_from, ccr_to, rate_to, currency_to, amount_to, datehour, user_id FROM transfer"):
    print(row)
    id, currency_from, amount_from, ccr_from, rate_from, ccr_to, rate_to, currency_to, amount_to, datehour, user_id = row
    formatted_time3 = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(datehour))
    print(formatted_time3)

con.close()

#########################
# 2nd part of the program. Connects, selects, and shows content of the table transfer.
new_con = sqlite3.connect("transcript.db")
new_cur = new_con.cursor()
for row in new_cur.execute("SELECT id, currency_from, amount_from, ccr_from, rate_from, ccr_to, rate_to, currency_to, amount_to, datehour, user_id FROM transfer"):
    print(row)
    id, currency_from, amount_from, ccr_from, rate_from, ccr_to, rate_to, currency_to, amount_to, datehour, user_id = row
    formatted_time3 = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(datehour))
    print(formatted_time3)

new_con.close()
