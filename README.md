# TRANSCRIPT
### Video Demo: https://youtu.be/mAHbfoznAbk
### Description:
System that simulates the electronic transfer of money between bank accounts of different countries through cryptocurrency avoiding fee.

The idea is that:
1) you transfer from your bank account to this system,
2) you transfer from one currency to another inside the system,
3) and then, you transfer from this system to your bank account of another country.

But, as this system is only a simulation, when you register, the system gives you money as a welcome gift, so you can simulate the transfer.


### How the program project.py works:

You type the command to execute the program: python project.py

The program asks your mail. If you are already registered enter your mail, and then, password.
If not registered, register entering your mail, first name, last name, and password.
Once you are registered, you can log in with your mail and password.

The program shows your balance of the four currencies: United States Dollar, Argentine Peso, South Korean Won, and Euro.
The program fetches actual cryptocurrency rates (prices) from internet market and shows them.
They are three cryptocurrencies: Bitcoin, Ethereum, and Tether.
These 3 cryptocurrency rates are related to the 4 currencies. It means the screen shows you 12 rates (3 x 4 = 12).

Now, you have options to select:
1) View previous transfers,
2) or Transfer.

#### View previous transfers

When you select to view previous transfers (1), it shows all the transfers that you have made before.
The fields of the data are:
 - CURRENCY FROM: from what currency was the transfer.
 - AMOUNT FROM: the amount of currency from. This amount is shown with the symbol minus(-) to demonstrate that the amount was subtracted from user's balance.
 - CCR FROM: cryptocurrency chosen during the transfer, related to the currency from.
 - RATE FROM: rate (price) of the cryptocurrency related to the currency from.
 - CCR TO: cryptocurrency chosen during the transfer, related to the currency to.
 - RATE TO: rate (price) of the cryptocurrency related to the currency to.
 - CURRENCY TO: to what currency was the transfer.
 - AMOUNT TO: the amount of currency to. This is the amount added to the user's balance.
 - DATE TIME: the date and the time of the transfer, in Coordinated Universal Time (UTC).

These fields are to demonstrate the details of each of transfers.
The amount of selected currency (AMOUNT FROM) is converted into cryptocurrency using RATE FROM.
Then, it is converted into selected currency of destination (AMOUNT TO) using the correspondent RATE TO.

The formula is:
(AMOUNT FROM / RATE FROM ) x RATE TO = AMOUNT TO

Where,
 - / means division
 - x means multiplication
 - = means equals

CCR FROM and CCR TO have the same cryptocurrency but different currencies.
Date and time are important for any transaction.

#### Transfer

When you select to transfer (2), it shows a menu to choose:
1) From what currency transfer: Dollar, Peso, Won, or Euro.
2) To what currency transfer: Idem above.
Both currencies must be different.
3) Through what cryptocurrency: Bitcoin, Ethereum, or Tether.

The minimum amount to transfer is 1 for both Dollar and Euro, and 1000 for both Peso and Won.
The maximum amount to transfer (AMOUNT FROM) is the balance of the user.

Let's review the formula:
(AMOUNT FROM / RATE FROM ) x RATE TO = AMOUNT TO

For example:
(1 / 120,000) x 156,000,000 = 1300

Where,
 - AMOUNT FROM: 1 (dollar)
 - RATE FROM: 120,000 (dollar-bitcoin)
 - RATE TO: 156,000,000 (peso-bitcoin)
 - AMOUNT TO: 1300 (peso)

You can see that,
 - CURRENCY FROM: USD
 - CCR FROM: usd-btc
 - CCR TO: ars-btc
 - CURRENCY TO: ARS

If the transfer is successful, the program saves the transaction.

While you use the program, the actual rate (price) of all cryptocurrencies are fetched from internet market continuously.
As the program uses a free account, has to have fetched at least 15 seconds ago to fetch again the new data.
If it passed less than 15 seconds, it does not fetch new data, and uses the data brought before.

When you choose to Exit, the program saves the updated balance of the 4 currencies of the user and exits.



### How the program test_project.py works:

You type the command to execute the program: pytest test_project.py

Tests 3 functions of the program project.py

1. Tests verify_mail(s).
2. Tests login(typed_mail, typed_pass).
3. Tests accept_amount(text, account, opt).



### How the program sqlite3-user.py works:

You type the command to execute the program: python sqlite3-user.py

Creates the table user in the database.
 - id INTEGER PRIMARY KEY AUTOINCREMENT,
 - mail CHAR(30) UNIQUE,
 - name CHAR(30),       (is the first name and the last name of the user)
 - password BLOB(64),   (encrypted password)
 - usd FLOAT,           (dollar balance of the user)
 - ars FLOAT,           (peso balance of the user)
 - krw FLOAT,           (won balance of the user)
 - eur FLOAT            (euro balance of the user)

Inserts a register in the table created above.

I chose sqlite3 because it is lightweight and adjusts to this project.

I added user's balance in this table because every user has these 4 balances.

### How the program sqlite3-transfer.py works:

You type the command to execute the program: python sqlite3-transfer.py

Creates the table transfer in the database.
 - id INTEGER PRIMARY KEY AUTOINCREMENT,
 - currency_from CHAR(3),
 - amount_from FLOAT,
 - ccr_from CHAR(8),
 - rate_from FLOAT,
 - ccr_to CHAR(8),
 - rate_to FLOAT,
 - currency_to CHAR(3),
 - amount_to FLOAT,
 - datehour FLOAT,
 - user_id INTEGER      (is the id of the table user created above)

Inserts a register in the table created above.
