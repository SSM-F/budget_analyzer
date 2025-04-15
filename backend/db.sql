
DROP DATABASE IF EXISTS expenses_vs_budget;

CREATE DATABASE expenses_vs_budget
WITH ENCODING = 'UTF8';


CREATE USER %{PGUSER}  WITH ENCRYPTED PASSWORD '%{PGPASSWORD}';
GRANT ALL PRIVILEGES ON DATABASE expenses_vs_budget TO %{PGUSER};


\c expenses_vs_budget

CREATE TABLE expenses(
    expense_id SERIAL PRIMARY KEY,
    id INTEGER,
    date DATE NOT NULL,
    description TEXT,
    amount NUMERIC(10,2) NOT NULL,
    category TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
GRANT ALL PRIVILEGES ON SCHEMA public TO budget_user;
GRANT ALL PRIVILEGES ON TABLE expenses TO budget_user;

GRANT USAGE, SELECT ON SEQUENCE expenses_expense_id_seq TO budget_user;
GRANT UPDATE ON SEQUENCE expenses_expense_id_seq TO budget_user;
ALTER SEQUENCE expenses_expense_id_seq OWNED BY budget_user;
ALTER TABLE expenses ADD CONSTARINT unique_expenses UNIQUE (date,description,amount,category);



