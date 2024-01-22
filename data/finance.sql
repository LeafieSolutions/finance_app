CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username TEXT NOT NULL,
    hash TEXT NOT NULL,
    cash NUMERIC NOT NULL DEFAULT 10000.00
);


CREATE UNIQUE INDEX username ON users (username);


CREATE TABLE companies (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    ticker TEXT NOT NULL UNIQUE,
    name TEXT
    latest_price NUMERIC DEFAULT 0 NOT NULL,
    last_update DATETIME DEFAULT '2022-01-01 10:00:00' NOT NULL,
);


CREATE UNIQUE INDEX ticker ON companies (ticker);


CREATE TABLE transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        time_stamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
        user_id INTEGER NOT NULL,
        comp_ticker TEXT NOT NULL,
        trans_type TEXT NOT NULL,
        shares INTEGER NOT NULL,
        price NUMERIC NOT NULL,

        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(comp_ticker) REFERENCES companies(ticker)
);


CREATE TABLE states (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id INTEGER NOT NULL,
    comp_ticker TEXT NOT NULL,
    shares INTEGER NOT NULL DEFAULT 0,

    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(comp_ticker) REFERENCES companies(ticker)
);
