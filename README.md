# finance_app
## Finance app for stock portfolio management

## Table of Contents
1. [Setup](#setup)
1. [Usage](#usage)
1. [Contribution](#contribution)

## Setup
- Prerequisites

    Prerequisite | Installation
    ---- | ----
    python3 | Install python depending on your OS
    pip3 | `wget https://bootstrap.pypi.io/get-pip.py; python3 get-pip.py; rm get-pip.py`
    virtualenv | `pip3 install virtualenv`


- Clone [the repo](https://github.com/LeafieSolutions/finance_app): `git clone https://github.com/LeafieSolutions/finance_app`

- Create a virtual environment: `virtualenv ".env_$(basename $PWD)"`

- Activate it: `source ".env_$(basename $PWD)/bin/activate"`

- Install dependencies: `pip3 install -r requirements.txt`

## Usage
- Setup the project as indicated [the setup section](#setup) of this README

- Run the following in the terminal

- Create an **Individual Account** with a **free plan** at https://iexcloud.io/cloud-login#/register/

- Confirm your account via confirmation email


- Visit https://iexcloud.io/console/token and copy the key that appears under the Token column (it should begin with pk_).

- In your terminal window, execute:
`export API_KEY=value`
where value is that (pasted) value, without any space immediately before or after the =.

    (*You also may wish to paste that value in a text document somewhere, in case you need it again later*).

- Run Flask's server: `python -m app`

- You can now trade stocks !!!

## Contribution

- Setup the project as indicated [the setup section](#setup) of this README

- To run the server in development mode run: `flask --app app --debug run`

### Backend

- Make you contribution

- Create a pull request and wait for confirmation


## Frontend

- Here are the definition of routes

- ### /login/<string:username>/<string:password>
```
redirect to /
```

- ### /login
```
login.html
```

- ### /register/<string:username>/<string:password>/<string:confirmation>
```
redirect to /
```

- ### /logout
```
redirect("/login")
```

- ### /api/user/summary
    - GET 
        ```json
        {
            "state": [
                {
                    "name": "Apple Inc",
                    "ticker": "AAPL",
                    "price": 201,
                    "shares": 2,
                    "total": 402
                },
                {
                    "name": "Tesla Inc",
                    "ticker": "TSLA",
                    "price": 230,
                    "shares": 3,
                    "total": 690
                },
            ],
            "cash" : 2000,
            "stocks_total": 1902,
            "portfolio_total": 3902
        }
        ```

- ### /home or /
    - GET
        ```
        homepage.html
        ```

- ### /api/quote/<string:company_name>
    - GET
        ```json
        {
            "price": 203.43
        }
        ```


- ### /buy
    - GET
        ```
        buy.html
        ```
    

- ### /buy/<string:company_name>/<int:shares>
    - GET
        - successful
        ```json
        {
            "flag": "success",
            "shares": 2,
            "price": 203.43,
            "total_share_cost": 406.86,
            
        }
        ```

        - user does not have enough shares
        ```json
        {
            "flag": "error",
            "reason": "insufficient cash",
            "cash": 2000
        }
        ```

- ### /api/user/company_names
    - GET
        ```json
        [
            "Apple Inc",
            "Tesla Inc"
        ]
        ```

- ### /sell/<string:company_name>/<int:shares>
    - GET
        - successful
        ```json
        {
            "flag": "success",
            "shares": 4,
            "price": 34.11,
            "total_share_cost": 136.44,
        }
        ```

        - user does not have enough shares
        ```json
        {
            "flag": "error",
            "reason": "non-existent shares",
        }
        ```


- ### sell
    - GET
        ```
        sell.html
        ```


- ### /api/user/history
    - GET
        ```json
        [
            {
                "timestamp": "2024-08-15 12:00:00",
                "name": "Apple Inc",
                "ticker": "AAPL",
                "price": 201,
                "shares": 2,
                "total": 402,
            },
            {
                "timestamp": "2024-08-15 12:00:00",
                "name": "Tesla Inc",
                "ticker": "TSLA",
                "price": 230,
                "shares": 3,
                "total": 690,
            },
        ]
        ```


- ### /history
    - GET
        ```
        history.html
        ```

- ### /api/user/username
    - GET
        ```json
        {
            "username": "username"
        }
        ```

- ### /profile/username/<string:username>
    - GET
        - successful
        ```json
        {
            "flag": "success",
            "username": "test_user"
        }
        ```
        - username already exists
        ```json
        {
            "flag": "error",
            "reason": "username already exists"
        }
        ```

        - username not changed
        ```json
        {
            "flag": "error",
            "reason": "not changed"
        }
        ```
        


- ### /profile/password/<string:old_password>/<string:password>
    - GET
        - successful
        ```json
        {
            "flag": "success",
        }
        ```

        - old password is incorrect
        ```json
        {
            "flag": "error",
            "reason": "incorrect password"
        }
        ```
    

- ### /profile
    - GET
        ```
        profile.html
        ```
