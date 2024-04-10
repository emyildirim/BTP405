use db;

CREATE TABLE user_types (
    type_id INT AUTO_INCREMENT PRIMARY KEY,
    type_name VARCHAR(20)
);

-- Users Table
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    type_id INT,
    fullname VARCHAR(50) NOT NULL,
    phone VARCHAR(15) NOT NULL,
    email VARCHAR(50) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    FOREIGN KEY (type_id) REFERENCES user_types(type_id)
);

-- Reservation Table
CREATE TABLE reservations (
    reservation_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    reservation_date DATE NOT NULL,
    reservation_time TIME NOT NULL,
    number_of_guests INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);


-- DEMO DATA

INSERT INTO user_types (type_name) VALUES
('Customer'),
('Staff');

/* EDIT THE HASHED PASSWORDS */
INSERT INTO users (type_id, fullname, phone, email, password_hash) VALUES
(1, 'John Doe', '1234567890', 'johndoe@yahoo.com', '$2b$12$kEt.z3GlbBI8Yrejgzuzz.TSDlPu2NTd04jv81RRUPQjhzV16dBsK'),
(1, 'Jane Smith', '9987654321', 'janesmith@outlook.com', '$2b$12$deBQcdMCLzdkc2H07DFPIOYVzwJVjFhY/MxTM4Q.hQ7FmiMPVnZzC'),
(2, 'Mitchel Rock', '5555555555', 'mitchel91@gmail.com', '$2b$12$B8N9Gu6yVH7sG1zHWTVMoOKwVk3Ehb8tcybOky0njjRRzUTRRC16O');


INSERT INTO reservations (user_id, reservation_date, reservation_time, number_of_guests) VALUES
(1, '2024-04-20', '20:00', 2),
(2, '2024-04-11', '15:00', 3),
(1, '2024-04-12', '13:00', 1),
(3, '2024-04-15', '13:00', 5),
(3, '2024-04-17', '13:00', 5);