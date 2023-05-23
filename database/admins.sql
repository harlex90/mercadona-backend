CREATE TABLE admins (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT NOT NULL,
  password TEXT NOT NULL
);

INSERT INTO admins (id, name, email, password) VALUES
(1, 'Soraya', 'soraya.gaillard@hotmail.fr', 'abcdef');
