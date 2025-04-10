
DROP DATABASE IF EXISTS expenses_vs_budget;

CREATE DATABASE expenses_vs_budget
WITH ENCODING = 'UTF8';


CREATE USER ${PG_USER}  WITH ENCRYPTED PASSWORD '${PG_PASSWORD}';
GRANT ALL PRIVILEGES ON DATABASE expenses_vs_budget TO budget_user;


\c expenses_vs_budget




CREATE TABLE expenses(
    expense_id SERIAL PRIMARY KEY,
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