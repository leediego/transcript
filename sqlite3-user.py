import sqlite3

# https://docs.python.org/3/library/sqlite3.html
# usage: python sqlite3-user.py
# In transcript.db, creates the table user
#  and inserts the user leediego@yahoo.com

# https://sqlite.org/foreignkeys.html
# sqlite3  (Enter)                     # Starts sqlite commands
# sqlite> PRAGMA foreign_keys = ON;    # Enables FOREIGN KEY constraints
# sqlite> PRAGMA foreign_keys;         # Returns 0 if disabled, 1 if enabled.
# sqlite> PRAGMA foreign_keys = OFF;   # Disables FOREIGN KEY constraints

###########################
# 1st part of the program. Creates the table, inserts a row and shows.
con = sqlite3.connect("transcript.db")
cur = con.cursor()
cur.execute("CREATE TABLE user(id INTEGER PRIMARY KEY AUTOINCREMENT, mail CHAR(30) UNIQUE, name CHAR(30), password BLOB(64)," \
"                       usd FLOAT, ars FLOAT, krw FLOAT, eur FLOAT)")


cur.execute("""
    INSERT INTO user (mail, name, password, usd, ars, krw, eur)
            VALUES('leebeta@yahoo.com', 'Diego Lee', '27305517b9eeb1bfcfa90b2de37d177f3edf22f2bcdb7cd33d25caad2732c86c', 100.0, 100000.0, 100000.0, 100.0)
""")
con.commit()


for row in cur.execute("SELECT id, mail, name, password, usd, ars, krw, eur FROM user"):
    print(row)

con.close()

#########################
# 2nd part of the program. Connects, selects, and shows content of the table user.
new_con = sqlite3.connect("transcript.db")
new_cur = new_con.cursor()
for row in new_cur.execute("SELECT id, mail, name, password, usd, ars, krw, eur FROM user"):
    print(row)

new_con.close()
