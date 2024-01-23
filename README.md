# finance_app
## Finance app for stock portfolio management

## Table of Contents
1. [Setup](#setup)
1. [Usage](#usage)
1. [Contribution](#contribution)
    1. [Backend](#backend)
    1. [API End Points](#api-end-points)


## Setup
- Prerequisites

    Prerequisite | Installation
    ---- | ----
    python3 | Install python3 depending on your OS
    pip3 | `wget https://bootstrap.pypi.io/get-pip.py; python3 get-pip.py; rm get-pip.py`
    virtualenv | `pip3 install virtualenv`


- Clone [the repo](https://github.com/LeafieSolutions/finance_app): `git clone https://github.com/LeafieSolutions/finance_app`

- Create a virtual environment: `virtualenv ".env_$(basename $PWD)"`

- Activate it: `source ".env_$(basename $PWD)/bin/activate"`

- Install dependencies: `pip3 install -r requirements.txt`

- Create an **Individual Account** with a **free plan** at https://iexcloud.io/cloud-login#/register/

- Confirm your account via confirmation email

- Visit https://iexcloud.io/console/token and copy the key that appears under the Token column (it should begin with pk_).

- In your terminal window, execute:
`export API_KEY=value`
where value is that (pasted) value, without any space immediately before or after the =.

    (*You also may wish to paste that value in a text document somewhere, in case you need it again later*).

## Production
- Setup the project as indicated [the setup section](#setup) of this README

- Run Flask's server using gunicorn: `gunicorn -b 127.0.0.1:5000 app`

- You can now trade stocks !!!

## Contribution

- Setup the project as indicated [the setup section](#setup) of this README

- To run the server in development mode run: `flask --app app --debug run`

- Make you contribution

- Create a pull request and wait for confirmation


## API End Points

### Login

- #### /login
    - GET
        ```
        login.html
        ```

- #### /api/login/authenticate?username=<string:username>&password=<string:password>
    - GET
        - successful
        ```json
        {
            "flag": "success",
        }
        ```

        - username not passed in url query
        ```json
        {
            "flag": "error",
            "reason": "null username",
        }
        ```

        - password not passed in url query
        ```json
        {
            "flag": "error",
            "reason": "null password",
        }
        ```

        - invalid username or password
        ```json
        {
            "flag": "error",
            "reason": "invalid",
        }
        ```


### Register

- #### /register
    - GET
        ```
        register.html
        ```

- #### /api/register/username_exists?username=<string:username>
    - GET
        - null username
        ```json
        {
            "flag": "error",
            "reason": "null username",
        }
        ```
        - username exists
        ```json
        {
            "flag": "success",
            "reason": "exist",
        }
        ```
        - username does not exist
        ```json
        {
            "flag": "success",
            "reason": "not exist",
        }
        ```


- ####  /api/register?username=<string:username>&password=<string:password>
    - GET
        - successful
        ```json
        {
            "flag": "success",
        }
        ```

        - username not passed in url query
        ```json
        {
            "flag": "error",
            "reason": "null username",
        }
        ```

        - password not passed in url query
        ```json
        {
            "flag": "error",
            "reason": "null password",
        }
        ```

        - invalid username
        ```json
        {
            "flag": "error",
            "reason": "invalid username",
        }
        ```

        - username already exists
        ```json
        {
            "flag": "error",
            "reason": "username exists"
        }
        ```


### Homepage

- #### /home or /
    - GET
        ```
        homepage.html
        ```

- #### /logout
    - GET
        ```
        redirect to "/login"
        ```

- #### /api/user/summary
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

- #### /api/company_names
    - GET
        ```jsonc
        [
            "Apple Inc",
            "Tesla Inc",
            "Microsoft Corporation",
            "Amazon Inc",
            "Facebook Inc",
            "Alphabet Inc",
        //  ...
        ]
        ```


### Quote

- #### /quote
    - GET
        ```
        quote.html
        ```

- #### /api/quote?company_name=<string:company_name>
    - GET
        - successful
        ```json
        {
            "flag": "success",
            "ticker": "AAPL",
            "name": "Apple Inc",
            "price": 203.43
        }
        ```
        - company name not passed in url query
        ```json
        {
            "flag": "error",
            "reason": "null company_name",
        }
        ```
        - company name does not exist
        ```json
        {
            "flag": "error",
            "reason": "invalid company_name",
        }
        ```


### Buy

- #### /buy
    - GET
        ```
        buy.html
        ```
    

- #### /api/buy?company_name=<string:company_name>&shares=<int:shares>
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

        - company name not passed in url query
        ```json
        {
            "flag": "error",
            "reason": "null company_name",
        }
        ```

        - shares not passed in url query
        ```json
        {
            "flag": "error",
            "reason": "null shares",
        }
        ```

        - company name does not exist
        ```json
        {
            "flag": "error",
            "reason": "invalid company_name",
        }
        ```

        - shares is not a positive integer
        ```json
        {
            "flag": "error",
            "reason": "invalid shares",
        }
        ```

        - user does not have enough cash
        ```json
        {
            "flag": "error",
            "reason": "insufficient cash",
            "cash": 2000
        }
        ```


### Sell

- #### /sell
    - GET
        ```
        sell.html
        ```

- #### /api/user/company_shares
    - GET
        ```json
        {
            "Apple Inc": 2,
            "Goldman Sachs Physical Gold ETF Trust - Goldman Sachs Physical Gold ETF": 2,
            "Microsoft Corporation": 3,
            "Tesla Inc": 4
        }
        ```


- #### /api/sell?company_name=<string:company_name>&shares=<int:shares>
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

        - company name not passed in url query
        ```json
        {
            "flag": "error",
            "reason": "null company_name",
        }
        ```

        - shares not passed in url query
        ```json
        {
            "flag": "error",
            "reason": "null shares",
        }
        ```

        - shares is not a positive integer
        ```json
        {
            "flag": "error",
            "reason": "invalid shares",
        }
        ```

        - user does not have shares in company
        ```json
        {
            "flag": "error",
            "reason": "invalid company_name",
        }
        ```

        - user does not have enough shares
        ```json
        {
            "flag": "error",
            "reason": "insufficient shares",
        }
        ```



### History

- #### /history
    - GET
        ```
        history.html
        ```

- #### /api/user/history
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



### Profile


- #### /profile
    - GET
        ```
        profile.html
        ```


- #### /api/user/profile/username
    - GET
        ```
        "testuser"
        ```

- #### /api/register/username_exists?username=<string:username>
    - GET
        - null username
        ```json
        {
            "flag": "error",
            "reason": "null username",
        }
        ```
        - username exists
        ```json
        {
            "flag": "success",
            "reason": "exist",
        }
        ```
        - username does not exist
        ```json
        {
            "flag": "success",
            "reason": "not exist",
        }
        ```


- #### /api/user/profile/change/username?username=<string:new_username>
    - GET
        - successful
        ```json
        {
            "flag": "success",
            "username": "test_user"
        }
        ```
        - username not passed in url query
        ```json
        {
            "flag": "error",
            "reason": "null username",
        }
        ```
        - invalid username
        ```json
        {
            "flag": "error",
            "reason": "invalid username",
        }
        ```
        - username already exists
        ```json
        {
            "flag": "error",
            "reason": "already taken"
        }
        ```

        - username not changed
        ```json
        {
            "flag": "error",
            "reason": "not changed"
        }
        ```
        


- #### /api/user/profile/change/password?old_password=<string:old_password>&new_password=<string:new_password>
    - GET
        - successful
        ```json
        {
            "flag": "success",
        }
        ```
        - old password not passed in url query
        ```json
        {
            "flag": "error",
            "reason": "null old_password",
        }
        ```
        - new password not passed in url query
        ```json
        {
            "flag": "error",
            "reason": "null new_password",
        }
        ```

        - old password is incorrect
        ```json
        {
            "flag": "error",
            "reason": "incorrect password"
        }
        ```
    
