import requests
import json
import sys
import time
from tabulate import tabulate
import sqlite3
from validator_collection import validators
from password_validator import PasswordValidator
import re
from hashlib import sha256
from getpass_asterisk.getpass_asterisk import getpass_asterisk

# usage: python project.py
# Program that simulates the electronic transfer of money between bank accounts of different countries through cryptocurrency avoiding fee.

# Create a schema (password)
schema = PasswordValidator()
# Add properties to it
schema\
.min(8)\
.max(20)\
.has().uppercase()\
.has().lowercase()\
.has().digits()\
.has().no().spaces()\
.has().symbols()            # Password must include symbol.

start_time = 100.0          # Initialization is executed for that the first time that enters to update_rates,
end_time = 1000.0           #  executes fetch_rates.

dict = {}

rates = {
    "usd_btc": 0.0,
    "usd_eth": 0.0,
    "usd_usdt": 0.0,
    "ars_btc": 0.0,
    "ars_eth": 0.0,
    "ars_usdt": 0.0,
    "krw_btc": 0.0,
    "krw_eth": 0.0,
    "krw_usdt": 0.0,
    "eur_btc": 0.0,
    "eur_eth": 0.0,
    "eur_usdt": 0.0,
}


class Account:
    def __init__(self, row):
        id, mail, name, password, usd, ars, krw, eur = row
        self._id = id           # id is int
        self._name = name
        self._balance_dollar = float(usd)       # _ means that only this program
        self._balance_peso   = float(ars)       # can use this instance variable
        self._balance_won    = float(krw)
        self._balance_euro   = float(eur)

    @property
    def id(self):
        return self._id
    @property
    def name(self):
        return self._name
    @property
    def balance_dollar(self):
        return self._balance_dollar
    @property
    def balance_peso(self):
        return self._balance_peso
    @property
    def balance_won(self):
        return self._balance_won
    @property
    def balance_euro(self):
        return self._balance_euro

    def deposit_dollar(self, n):
        n = float(f"{n:.2f}")
        self._balance_dollar += n
        print(f"Deposit US Dollar: U${n:,.2f}")

    def withdraw_dollar(self, n):
        n = float(f"{n:.2f}")
        self._balance_dollar -= n
        print(f"Withdraw US Dollar: U${n:,.2f}")

    def deposit_peso(self, n):
        n = float(f"{n:.2f}")
        self._balance_peso += n
        print(f"Deposit Argentine Peso: ${n:,.2f}")

    def withdraw_peso(self, n):
        n = float(f"{n:.2f}")
        self._balance_peso -= n
        print(f"Withdraw Argentine Peso: ${n:,.2f}")

    def deposit_won(self, n):
        n = float(f"{n:.0f}")               # KRW without decimal numbers.
        self._balance_won += n
        print(f"Deposit Korean Won: ₩{n:,.2f}")

    def withdraw_won(self, n):
        n = float(f"{n:.0f}")               # KRW without decimal numbers.
        self._balance_won -= n
        print(f"Withdraw Korean Won: ₩{n:,.2f}")

    def deposit_euro(self, n):
        n = float(f"{n:.2f}")
        self._balance_euro += n
        print(f"Deposit Euro: €{n:,.2f}")

    def withdraw_euro(self, n):
        n = float(f"{n:.2f}")
        self._balance_euro -= n
        print(f"Withdraw Euro: €{n:,.2f}")


def register():
    c = False
    while(c == False):
        mail = input("Mail: ")
        check = verify_mail(mail)     # check == True when verifies that the mail is valid.
        if (check == True):
            existent = verify_mail_db(mail)         # existent == True when the mail is existent.
            if (existent):
                print("Mail already registered.")
            else:
                c = True
        else:
            print("Mail not valid.")

    c = False
    while(c == False):
        first_name = input("First name: ").strip()
        c = verify_name(first_name)
    c = False
    while(c == False):
        last_name = input("Last name: ").strip()
        c = verify_name(last_name)
    name = (first_name + " " + last_name).title()[:30]       # The first letter to be uppercase.
                                                            # Truncate until 30 characters.
    c = False
    while(c == False):
        input_password = getpass_asterisk("Password (8-20 characters, include lowercase, uppercase, number, symbol): ")
        check = verify_password(input_password)              # check == True when it verifies that the password is valid.
        if(check == True):
            input_password2 = getpass_asterisk("Type same password again: ")
            if (input_password == input_password2):
                c = True
            else:
                print("Password has to be same two times.")

    password = sha256(input_password.encode('utf-8')).hexdigest()
    usd = 100.0                     # Welcome gift United States Dollar
    ars = 100000.0                  # Welcome gift Argentine Peso
    krw = 100000.0                  # Welcome gift Korean Won
    eur = 100.0                     # Welcome gift Euro

    con = sqlite3.connect("transcript.db")
    cur = con.cursor()
    cur.execute("""
        INSERT INTO user (mail, name, password, usd, ars, krw, eur)
                VALUES(?, ?, ?, ?, ?, ?, ? )
    """, (mail, name, password, usd, ars, krw, eur))
    con.commit()
    con.close()


def verify_mail(s):
    if(len(s) > 30):        # If the length of the mail is more than 30, it is not valid.
        return False
    try:
        validators.email(s)
    except ValueError:
        return False
    return True


def verify_mail_db(s):
    new_con = sqlite3.connect("transcript.db")
    new_cur = new_con.cursor()
    new_cur.execute("""
                    SELECT mail FROM user WHERE mail = ?
                    """, (s,))
    row = new_cur.fetchone()
    #print(row)
    new_con.close()
    if (row):
        return True         # Existent mail.
    else:
        return False


def verify_name(s):
    if matches := re.search(r"^[a-zA-Z]+$", s):
        return True
    return False


def verify_password(s):
    return(schema.validate(s))


def login(typed_mail, typed_pass):
    hashed_pass = sha256(typed_pass.encode('utf-8')).hexdigest()
    new_con = sqlite3.connect("transcript.db")
    new_cur = new_con.cursor()
    new_cur.execute("""
                    SELECT id, mail, name, password, usd, ars, krw, eur FROM user WHERE mail = ? AND password = ?
                    """, (typed_mail, hashed_pass,))
    row = new_cur.fetchone()
    #print(row)
    new_con.close()
    if (row):
        account = Account(row)
        return account         # object account: Logged in.
    else:
        return False        # False: Could not log in.


def update_rates(rates):
    global start_time
    global end_time

    # Wait to pass at least 15 seconds between one fetch and another, because as it is a free account,
    # the page does not permit to do several fetches in so little time.
    end_time = time.time()
    elapsed_time = end_time - start_time
    if elapsed_time > 15:
        o = fetch_rates()
        start_time = end_time

    # format the dictionary(o) to obtain the criptocurrency rate (ccr).
        dict = o["bitcoin"]
        save_rates("btc", dict, rates)

        dict = o["ethereum"]
        save_rates("eth", dict, rates)

        dict = o["tether"]
        save_rates("usdt", dict, rates)


def fetch_rates():
    try:
        response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,tether&vs_currencies=usd,ars,krw,eur")
        o = response.json()
        #print(json.dumps(o, indent=2))

    except requests.RequestException:
        sys.exit("Request Exception to coingecko.com")

    return o


def save_rates(coin, dict, rates):
    rates["usd_" + coin] = float(dict["usd"])
    rates["ars_" + coin] = float(dict["ars"])
    rates["krw_" + coin] = float(dict["krw"])
    rates["eur_" + coin] = float(dict["eur"])


def print_menu(account, rates):
    print(f"Hello, {account.name} !  Your balance is:" )

    table = [["USD U$", account.balance_dollar],
             ["ARS  $", account.balance_peso  ],
             ["KRW  ₩", account.balance_won   ],
             ["EUR  €", account.balance_euro  ]]
    headers = ["CURRENCY", "BALANCE"]
    print(tabulate(table, headers, tablefmt="grid", floatfmt=",.2f"))

    print("Actually the price of cryptocurrency: ")
    table = [["USD U$", rates["usd_btc"], rates["usd_eth"], rates["usd_usdt"]],
             ["ARS  $", rates["ars_btc"], rates["ars_eth"], rates["ars_usdt"]],
             ["KRW  ₩", rates["krw_btc"], rates["krw_eth"], rates["krw_usdt"]],
             ["EUR  €", rates["eur_btc"], rates["eur_eth"], rates["eur_usdt"]]]
    headers = ["RATE", "Bitcoin", "Ethereum", "Tether"]
    print(tabulate(table, headers, tablefmt="grid", floatfmt=",.6f"))


def view_previous_transfers(account):
    transfers = []
    new_con = sqlite3.connect("transcript.db")
    new_cur = new_con.cursor()
    for row in new_cur.execute("""
           SELECT id, currency_from, amount_from, ccr_from, rate_from, ccr_to, rate_to, currency_to, amount_to, datehour, user_id FROM transfer
           WHERE user_id = ?
           """, (account.id,)):
        #print(row)
        transfers.append(row)
    new_con.close()

    table = []
    for transfer in transfers:
        id, currency_from, amount_from, ccr_from, rate_from, ccr_to, rate_to, currency_to, amount_to, datehour, user_id = transfer
        formatted_time3 = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(datehour))
        table.append([currency_from, amount_from, ccr_from, rate_from, ccr_to, rate_to, currency_to, amount_to, formatted_time3 ])
    headers = ["FROM", "AMOUNT FROM", "CCR FROM", "RATE FROM", "CCR TO", "RATE TO", "TO", "AMOUNT TO", "DATE       TIME"]
    print(tabulate(table, headers, tablefmt="grid", floatfmt=",.2f"))


def accept_transfer_option():
    print("Transfer from: (1)Dollar (2)Peso (3)Won (4)Euro (5)Exit ", end="")
    option_from = input("Your option: ")
    if (option_from not in "1234") or (option_from == ""):            # option_from == "" means that the input option is enter.
        return False
    if len(option_from) > 1:                    # option_from maybe "123" for example. It is not valid.
        return False

    print("Transfer to: (1)Dollar (2)Peso (3)Won (4)Euro (5)Exit ", end="")
    option_to = input("Your option: ")
    if (option_to not in "1234") or (option_to == ""):
        return False
    if len(option_to) > 1:                      # option_to maybe "234" for example. It is not valid.
        return False

    print("Through: (1)Bitcoin (2)Ethereum (3)Tether (4)Exit ", end="")
    option_through = input("Your option: ")
    if (option_through not in "123") or (option_through == ""):
        return False
    if len(option_through) > 1:                 # option_through maybe "123" for example. It is not valid.
        return False

    if option_from == option_to:
        print("Currency_from and currency_to must be different.")
        return False

    return (option_from + option_to + option_through)


def accept_amount(text, account, opt):
    try:
        amount = float(text)
    except:
        return False        # text is not valid. Has to be float.

    if amount <= 0:
        return False        # amount to transfer must be positive.

    opt_from = opt
    match opt_from:
        case "1": execute = available_dollar(account, amount)
        case "2": execute = available_peso(account, amount)
        case "3": execute = available_won(account, amount)
        case "4": execute = available_euro(account, amount)
        case _: execute = False
    if execute:
        return amount
    return False


def available_dollar(account, amount_dollar):
    if amount_dollar < 1:       # minimum amount dollar
        return False
    if account.balance_dollar < amount_dollar:
        return False
    return True

def available_peso(account, amount_peso):
    if amount_peso < 1000:       # minimum amount peso
        return False
    if account.balance_peso < amount_peso:
        return False
    return True

def available_won(account, amount_won):
    if amount_won < 1000:       # minimum amount won
        return False
    if account.balance_won < amount_won:
        return False
    return True

def available_euro(account, amount_euro):
    if amount_euro < 1:       # minimum amount euro
        return False
    if account.balance_euro < amount_euro:
        return False
    return True


def transfer_coin(account, opt, amount_from, rate):
    opt_from = opt[0]
    opt_to = opt[1]
    opt_through = opt[2]
    print("----- Starting transfer -----")

    match opt_from:

        case "1":       # from USD
            currency_from = "USD"
            account.withdraw_dollar(amount_from)
            match opt_through:
                case "1":
                    ccr_from = "usd_btc"
                    rate_from = rate["usd_btc"]
                    temp_ccr = amount_from / rate["usd_btc"]
                    ccr_to, rate_to, currency_to, amount_to = transfer_currency_to(account, opt_to, "btc", temp_ccr, rate)
                case "2":
                    ccr_from = "usd_eth"
                    rate_from = rate["usd_eth"]
                    temp_ccr = amount_from / rate["usd_eth"]
                    ccr_to, rate_to, currency_to, amount_to = transfer_currency_to(account, opt_to, "eth", temp_ccr, rate)
                case "3":
                    ccr_from = "usd_usdt"
                    rate_from = rate["usd_usdt"]
                    temp_ccr = amount_from / rate["usd_usdt"]
                    ccr_to, rate_to, currency_to, amount_to = transfer_currency_to(account, opt_to, "usdt", temp_ccr, rate)

        case "2":       # from ARS
            currency_from = "ARS"
            account.withdraw_peso(amount_from)
            match opt_through:
                case "1":
                    ccr_from = "ars_btc"
                    rate_from = rate["ars_btc"]
                    temp_ccr = amount_from / rate["ars_btc"]
                    ccr_to, rate_to, currency_to, amount_to = transfer_currency_to(account, opt_to, "btc", temp_ccr, rate)
                case "2":
                    ccr_from = "ars_eth"
                    rate_from = rate["ars_eth"]
                    temp_ccr = amount_from / rate["ars_eth"]
                    ccr_to, rate_to, currency_to, amount_to = transfer_currency_to(account, opt_to, "eth", temp_ccr, rate)
                case "3":
                    ccr_from = "ars_usdt"
                    rate_from = rate["ars_usdt"]
                    temp_ccr = amount_from / rate["ars_usdt"]
                    ccr_to, rate_to, currency_to, amount_to = transfer_currency_to(account, opt_to, "usdt", temp_ccr, rate)

        case "3":       # from KRW
            currency_from = "KRW"
            account.withdraw_won(amount_from)
            match opt_through:
                case "1":
                    ccr_from = "krw_btc"
                    rate_from = rate["krw_btc"]
                    temp_ccr = amount_from / rate["krw_btc"]
                    ccr_to, rate_to, currency_to, amount_to = transfer_currency_to(account, opt_to, "btc", temp_ccr, rate)
                case "2":
                    ccr_from = "krw_eth"
                    rate_from = rate["krw_eth"]
                    temp_ccr = amount_from / rate["krw_eth"]
                    ccr_to, rate_to, currency_to, amount_to = transfer_currency_to(account, opt_to, "eth", temp_ccr, rate)
                case "3":
                    ccr_from = "krw_usdt"
                    rate_from = rate["krw_usdt"]
                    temp_ccr = amount_from / rate["krw_usdt"]
                    ccr_to, rate_to, currency_to, amount_to = transfer_currency_to(account, opt_to, "usdt", temp_ccr, rate)

        case "4":       # from EUR
            currency_from = "EUR"
            account.withdraw_euro(amount_from)
            match opt_through:
                case "1":
                    ccr_from = "eur_btc"
                    rate_from = rate["eur_btc"]
                    temp_ccr = amount_from / rate["eur_btc"]
                    ccr_to, rate_to, currency_to, amount_to = transfer_currency_to(account, opt_to, "btc", temp_ccr, rate)
                case "2":
                    ccr_from = "eur_eth"
                    rate_from = rate["eur_eth"]
                    temp_ccr = amount_from / rate["eur_eth"]
                    ccr_to, rate_to, currency_to, amount_to = transfer_currency_to(account, opt_to, "eth", temp_ccr, rate)
                case "3":
                    ccr_from = "eur_usdt"
                    rate_from = rate["eur_usdt"]
                    temp_ccr = amount_from / rate["eur_usdt"]
                    ccr_to, rate_to, currency_to, amount_to = transfer_currency_to(account, opt_to, "usdt", temp_ccr, rate)

        case _: return False

    print("----- Transfer finished -----")
    amount_from_negative = amount_from * -1         # amount_from is subtracted from user's balance. So, register as negative value.
    datehour = time.time()

    # Save the log with the data generated in this function.
    con = sqlite3.connect("transcript.db")
    cur = con.cursor()
    cur.execute("""
        INSERT INTO transfer (currency_from, amount_from, ccr_from, rate_from, ccr_to, rate_to, currency_to, amount_to, datehour, user_id)
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ? )
    """, (currency_from, amount_from_negative, ccr_from, rate_from, ccr_to, rate_to, currency_to, amount_to, datehour, account.id))
    con.commit()
    con.close()
    return True


def transfer_currency_to(account, currency_to, ccr, temp_ccr, rate):
    match currency_to:
        case "1":
            ccr_to = "usd_" + ccr
            rate_to = rate["usd_" + ccr]
            currency_to = "USD"
            amount_to = temp_ccr * rate["usd_" + ccr]
            amount_to = float(f"{amount_to:.2f}")
            account.deposit_dollar(amount_to)
        case "2":
            ccr_to = "ars_" + ccr
            rate_to = rate["ars_" + ccr]
            currency_to = "ARS"
            amount_to = temp_ccr * rate["ars_" + ccr]
            amount_to = float(f"{amount_to:.2f}")
            account.deposit_peso(amount_to)
        case "3":
            ccr_to = "krw_" + ccr
            rate_to = rate["krw_" + ccr]
            currency_to = "KRW"
            amount_to = temp_ccr * rate["krw_" + ccr]
            amount_to = float(f"{amount_to:.0f}")       # KRW with no decimal numbers.
            account.deposit_won(amount_to)
        case "4":
            ccr_to = "eur_" + ccr
            rate_to = rate["eur_" + ccr]
            currency_to = "EUR"
            amount_to = temp_ccr * rate["eur_" + ccr]
            amount_to = float(f"{amount_to:.2f}")
            account.deposit_euro(amount_to)

    print(f"Chosen cryptocurrency: {ccr}")         # Infomation for the user.
    return ccr_to, rate_to, currency_to, amount_to


def save_status(account):
    save_con = sqlite3.connect("transcript.db")
    save_cur = save_con.cursor()
    save_cur.execute("""
                     UPDATE user SET usd=?, ars=?, krw=?, eur=? WHERE id = ?
        """, (account.balance_dollar, account.balance_peso, account.balance_won, account.balance_euro, account.id))
    save_con.commit()
    save_con.close()


def main():
    global rates
    print("Welcome to TRANSCRIPT")
# Identification of the user.
    c = False
    while(c == False):
        option = input("Enter your mail, or (1)Register (2)Exit: ")
        if (option == "2") or (option == ""):            # option == "" means that the input option is enter.
            sys.exit("Exit")
        if (option == "1"):
            register()
            print("Congratulations!!! Successful registration. You received a Welcome gift!!!")
        else:
            check = verify_mail(option)             # verifies that the mail is valid.
            if (check):
                typed_pass = getpass_asterisk("Enter your password: ")
                c = login(option, typed_pass)           # c == True if could log in. c is account(object).
                if (c):
                    print("Logged in.")
                else:
                    print("Invalid user.")
            else:
                print("Mail is invalid.")
    account = c

# Initialize rates. Print menu.
    c = True
    while(c == True):
        update_rates(rates)
        print_menu(account, rates)
# Main menu.
        option = input("Enter your option. (1)View previous transfers (2)Transfer (3)Exit: ")
        if (option not in "12") or (option == ""):                      # option == "" means option is enter.
            c = False
# Show previous transfers.
        if (option == "1"):
            view_previous_transfers(account)
# Transfer.
        if (option == "2"):
            transfer_option = accept_transfer_option()
            if(transfer_option):
                text = input("Type amount currency from: ")
                amount_from = accept_amount(text, account, transfer_option[0])
                if (amount_from):
                    transfer_coin(account, transfer_option, amount_from, rates)
                else:
                    print("Amount greater than your balance or smaller than the minimum." )
            else:
                c = False
# Finalize.
    save_status(account)


if __name__ == "__main__":
    main()
