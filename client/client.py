import requests


URL = "http://localhost:8080"

def print_response(obj):
    if obj.status_code != 200:
        print(obj.text)
    else:
        print(obj.json())


def create_user():
    response = requests.post(
        URL + "/user",
        json={"email": "salmansyyd12@gmail.com", "password": "secure_password"},
    )

    print_response(response)


def create_loan():
    loan_request = {
        "customer_id": 1,
        "loan_amount": 2000.0,
        "rate_of_interest": 20.0,
        "tennure_in_years": 1,
    }

    response = requests.post(URL + "/loan/request", json=loan_request)
    print_response(response)

def make_payment():
    pay = {
        "amount": 2000,
        "loan_id": 1,
        "payment_type": "sdf",
    }

    response = requests.post(
        URL+"/loan/pay",
        json=pay
    )
    print_response(response)


def get_ledger():
    loan_id = 1
    response = requests.get(
        URL+f"/loan/ledger/{loan_id}"
    )

    print_response(response)

def account_overview(customer_id):
    response = requests.get(
        URL+f"/loan/overview/{customer_id}"
    )
    print_response(response)


if __name__ == "__main__":
    # create_user()
    # create_loan()
    # make_payment()
    # get_ledger()
    account_overview(1)
