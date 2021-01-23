# django-sample for ATM

## Start Application
#### 1. Migrate
$ python manage.py makemigrations sample_api <br>
$ python manage.py migrate
#### 2. Run Locally
$ python manage.py runserver 0.0.0.0:8000

## Test
$ python manage.py test

## API
#### 1. Authorize
Call login API like below with inserted card number and pin number
```
url --location --request POST 'http://localhost:8000/api/login/' \
 --header 'Content-Type: application/json' \
 --data-raw '{
     "card_num": "1234",
     "pin_num": 1234
 }'
```
Then it will return user id and token like below
```
{
    "user_id": 2,
    "token": "ddf9c2f30a820dcf5bb88027dcc6e2f17821986a"
}
```

#### 2. Get accounts of the user
Call accounts API like below with user id and token like below
```
curl --location --request GET 'http://localhost:8000/api/users/2/accounts/' \
--header 'Authorization: Token ddf9c2f30a820dcf5bb88027dcc6e2f17821986a'
```
Then it will return accounts associated with the user like below
```
{
    "accounts": [
        {
            "account_num": "lllll",
            "user": 2,
            "balance": 50
        },
        {
            "account_num": "uuuuu",
            "user": 2,
            "balance": 300
        }
    ]
}
```

#### 3. Deposit
Call deposit API like below with user id, account number and the amount to deposit like below
```
curl --location --request POST 'http://localhost:8000/api/users/2/deposit' \
--header 'Authorization: Token ddf9c2f30a820dcf5bb88027dcc6e2f17821986a' \
--header 'Content-Type: application/json' \
--data-raw '{
    "account_num": "uuuuu",
    "amount": 300
}'
```
Then it will call cash bin to deposit and return deposited account like below
```
{
    "account": {
        "account_num": "uuuuu",
        "user": 2,
        "balance": 600
    }
}
```

#### 4. Withdraw
Call withdraw API like below with user id, account number and the amount to withdraw like below
```
curl --location --request POST 'http://localhost:8000/api/users/2/withdraw' \
--header 'Authorization: Token b6f1774af2ca95e69cd50534ef20dbcbd90f8b21' \
--header 'Content-Type: application/json' \
--data-raw '{
    "account_num": "uuuuu",
    "amount": 300
}'
```
Then it will call cash bin to withdraw and return withdrawn account like below
```
{
    "account": {
        "account_num": "uuuuu",
        "user": 2,
        "balance": 300
    }
}
```



