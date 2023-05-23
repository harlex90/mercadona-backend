CREATE TABLE promotions (
  id serial PRIMARY KEY,
  product_id integer NOT NULL,
  start_date integer NOT NULL,
  end_date integer NOT NULL,
  discount real NOT NULL
);
