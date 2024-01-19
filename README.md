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

### Backend
- Setup the project as indicated [the setup section](#setup) of this README

- Make you contribution

- Create a pull request and wait for confirmation
