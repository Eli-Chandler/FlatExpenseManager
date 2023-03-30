from datetime import datetime

import requests
from bson import ObjectId
from flask import Flask, render_template, request
from pymongo import MongoClient

notification_api_keys = {  # Populate with key = Flatmate name value = Flatmate alertzy api key
    "Eli": "myapikey1111",
    "Example_user_1": 'myapikey22222',
    "Example_user_2": "myapikey33333"
}

db_username = ''  # mongodb atlas database username
db_password = ''  # password
connection_string = ''
client = MongoClient(connection_string)
db = client['FlatExpenses']  # Either change these or make your database & collection called this
collection = db['transactions']

payment_schema = {
    'payee': str,
    'payer': str,
    'amount': float,
    'reference': str,
    'date': datetime,
    'paid': bool
}

app = Flask(__name__)


@app.route('/')
def index():
    users = notification_api_keys.keys()
    return render_template('transactions_directory.html', users=users)


def send_notification(name, title, message):
    params = {
        "accountKey": notification_api_keys[name],
        "title": title,
        "message": message,
        "priority": 2
    }
    r = requests.get("https://alertzy.app/send", params=params)


@app.route('/transactions/addnew', methods=['POST'])
def add_new_payment():
    data = request.form
    payee = data.get('payee')
    amount = round(float(data.get('amount')) / len(notification_api_keys), 2)
    reference = data.get('reference')
    date = datetime.now()
    paid = False

    print('payee:', payee)
    print('reference:', reference)
    print('amount:', amount)

    for person in notification_api_keys:
        if person == payee:
            send_notification(person, f'Payment request sent!',
                              f'We sent your request for ${amount} per person for {reference}')
        else:
            document = payment_schema.copy()
            document['payee'] = payee
            document['payer'] = person
            document['amount'] = amount
            document['reference'] = reference
            document['date'] = date
            document['paid'] = paid
            send_notification(person, f'Payment requested!',
                              f'{payee} has requested ${amount} from you for {reference}')
            collection.insert_one(document)
    return 'Success'


@app.route('/transactions/markpaid', methods=['POST'])
def mark_payment_paid():
    data = request.json
    id = ObjectId(data['id'])

    collection.update_one({'_id': id}, {'$set': {'paid': True}})
    transaction = collection.find_one({'_id': id})

    send_notification(transaction.get('payee'),
                      f'{transaction.get("payer")} has marked {transaction.get("reference")} as paid',
                      f'{transaction.get("payer")} has marked ${transaction.get("amount")} for {transaction.get("reference")} as paid! Transaction ID: {id}')
    return 'Successfully marked as paid'


@app.route('/transactions/poke', methods=['POST'])
def poke_payment():
    data = request.json
    id = ObjectId(data['id'])

    transaction = collection.find_one({'_id': id})
    print(transaction)
    send_notification(transaction.get('payer'),
                      f'{transaction.get("payee")} has poked you to pay {transaction.get("reference")}',
                      f'{transaction.get("payee")} has poked you to pay ${transaction.get("amount")} for {transaction.get("reference")} please pay promptly! Transaction ID: {id}')
    return 'Succesfully poked'


@app.route('/transactions')
def transactions_index():
    users = notification_api_keys.keys()
    return render_template('transactions_directory.html', users=users)


@app.route('/transactions/user/<user>')
def transactions_overview(user):
    transactions_to_be_paid = collection.find({'payer': user, 'paid': False})
    transactions_owed = collection.find({'payee': user, 'paid': False})

    transactions_to_be_paid_history = collection.find({'payer': user, 'paid': True})
    transactions_owed_history = collection.find({'payee': user, 'paid': True})

    return render_template('user_transactions.html', user=user, transactions_to_be_paid=transactions_to_be_paid,
                           transactions_owed=transactions_owed,
                           transactions_to_be_paid_history=transactions_to_be_paid_history,
                           transactions_owed_history=transactions_owed_history,
                           num_users=len(notification_api_keys))


if __name__ == '__main__':
    app.run()
