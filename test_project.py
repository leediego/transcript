from project import verify_mail, login, accept_amount
import pytest

# usage: pytest test_project.py

def test_verify_mail():
    assert verify_mail("1234567890123456789012345678901") == False
    assert verify_mail("12345678901234567890") == False

    assert verify_mail("") == False
    assert verify_mail("         ") == False
    assert verify_mail("invaliduser@invalidaddress") == False
    assert verify_mail("%$#=@*-+") == False
    assert verify_mail("admin*admin") == False
    assert verify_mail("user@domain.") == False

    assert verify_mail("lee@visa.com.ar") == True
    assert verify_mail("diego@delavega.ar") == True
    assert verify_mail("federico@lacroze.org.ar") == True
    assert verify_mail("lucas@utn.edu.ar") == True
    assert verify_mail("rich@man.com") == True
    assert verify_mail("iceman@yahoo.com") == True


def test_login():
    assert login("captain@america.com", "anyPasswordForMe") == False
    assert login("any@mail", "passwordisInvalid") == False

    account = login("leebeta@yahoo.com", "algoAlgo0+")
    assert account.name == "Diego Lee"

    account2 = login("coreargentina@hotmail.com", "algoAlgo2*")
    assert account2.name == "Diego Lee"


def test_accept_amount():
    account = login("leebeta@yahoo.com", "algoAlgo0+")
    assert accept_amount("text1", account, "1") == False
    assert accept_amount("123*456", account, "2") == False
    assert accept_amount("1", account, "3") == False
    assert accept_amount("1000", account, "3") == 1000
    assert accept_amount("1", account, "1") == 1

    account2 = login("coreargentina@hotmail.com", "algoAlgo2*")
    assert accept_amount("text22", account2, "4") == False
    assert accept_amount("654/987", account2, "1") == False
    assert accept_amount("1", account2, "2") == False
    assert accept_amount("1000", account2, "2") == 1000
    assert accept_amount("1", account2, "4") == 1
