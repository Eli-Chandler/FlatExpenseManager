# FlatExpenseManager
## What is it?
This tool lets you help manage shared payments with your flatmates/roommates.

![image](https://user-images.githubusercontent.com/53414320/228875575-9c16e01e-348f-4399-ab70-304e00a32c52.png)


## Setup
You neeed to modify some values in `app.py`

```py
notification_api_keys = {  # Populate with key = Flatmate name value = Flatmate alertzy api key
    "Eli": "myapikey1111",
    "Example_user_1": 'myapikey22222',
    "Example_user_2": "myapikey33333"
}
```
Alertzy is an app for iOS and Android, this is what lets you get notifications when a transaction is added/paid
Each of your flatmates needs to sign up here and provide their API key https://alertzy.app/

```
db_username = ''  # mongodb atlas database username
db_password = ''  # password
connection_string = ''
client = MongoClient(connection_string)
db = client['FlatExpenses']  # Either change these or make your database & collection called this
collection = db['transactions']
```

Add a new mongodb atlas and use the connection string here. Either create a database called 'FlatExpenses' and a collection inside called 'transactions' or modify these values to your current database.

That's it! Now either host locally or online (:

## Room for improvement

* Allow expenses to be sent to an individual user

Asynchronous backend - currently sending an alert blocks other actions. Why I don't fix this? If I had made this project from scratch I would have, however one of my flatmates started this as a 'chore notifier' and I added the transactions feature. I didn't want to steal any of their code so I only included my parts. Flask & Requests could be replaced with Quart & AioHTTP very easily to avoid blocking. However considering this project is intended for flats, so small userbases I don't think it will be an issue.
