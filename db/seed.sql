INSERT INTO books (isbn, title, author, price, stock) VALUES
('9780132350884', 'Clean Code', 'Robert C. Martin', 40.00, 5),
('9780201616224', 'The Pragmatic Programmer', 'Andrew Hunt', 45.00, 3),
('9780134685991', 'Effective Java', 'Joshua Bloch', 50.00, 7),
('9781491950357', 'Designing Data-Intensive Applications', 'Martin Kleppmann', 60.00, 4),
('9780596007126', 'Head First Design Patterns', 'Eric Freeman', 35.00, 6),
('9780134494166', 'Clean Architecture', 'Robert C. Martin', 42.00, 2),
('9780131177055', 'Refactoring', 'Martin Fowler', 48.00, 3),
('9781617294945', 'Spring in Action', 'Craig Walls', 38.00, 8),
('9780131103627', 'The C Programming Language', 'Brian W. Kernighan', 30.00, 5),
('9780262033848', 'Introduction to Algorithms', 'Thomas H. Cormen', 80.00, 2);


INSERT INTO customers (name, email) VALUES
('Alice Johnson', 'alice@example.com'),
('Bob Smith', 'bob@example.com'),
('Charlie Brown', 'charlie@example.com'),
('Diana Prince', 'diana@example.com'),
('Evan Davis', 'evan@example.com'),
('Fiona Adams', 'fiona@example.com');


INSERT INTO orders (customer_id) VALUES
(1), 
(2), 
(3),
(4); 