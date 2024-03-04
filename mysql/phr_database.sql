CREATE DATABASE IF NOT EXISTS db

use db;

CREATE TABLE user_types (
    type_id INT AUTO_INCREMENT PRIMARY KEY,
    type_name VARCHAR(20)
);

CREATE TABLE resources (
    resource_id INT AUTO_INCREMENT PRIMARY KEY,
    resource_name VARCHAR(25)
);

-- Users Table
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    type_id INT,
    fullname VARCHAR(50) NOT NULL,
    contact VARCHAR(10) NOT NULL,
    email VARCHAR(50) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    FOREIGN KEY (type_id) REFERENCES user_types(type_id)
);

-- Health Records Table
CREATE TABLE health_records (
    record_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    record_date DATE NOT NULL,
    record_text TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Healthcare Providers Table
CREATE TABLE healthcare_providers (
    provider_id INT AUTO_INCREMENT PRIMARY KEY,
    provider_name VARCHAR(100) NOT NULL,
    provider_address VARCHAR(50) NOT NULL,
    provider_contact VARCHAR(255)
);

-- User-Provider Relationship Table
CREATE TABLE user_provider (
    user_id INT,
    provider_id INT,
    PRIMARY KEY (user_id, provider_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (provider_id) REFERENCES healthcare_providers(provider_id)
);

-- Reminders and Alerts Table
CREATE TABLE reminders (
    reminder_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    reminder_text TEXT NOT NULL,
    reminder_date DATETIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- User access control table
CREATE TABLE permissions (
    resource_id INT,
    type_id INT,
    can_add BOOLEAN,
    can_view BOOLEAN,
    can_edit BOOLEAN,
    PRIMARY KEY (resource_id, type_id),
    FOREIGN KEY (resource_id) REFERENCES resources(resource_id),
    FOREIGN KEY (type_id) REFERENCES user_types(type_id)
);



-- DEMO DATA

INSERT INTO user_types (type_name)
VALUES
    ('Admin'),
    ('Doctor'),
    ('Patient');

INSERT INTO resources (resource_name)
VALUES
    ('Users'),
    ('Health Records'),
    ('Healthcare Providers'),
    ('User Provider'),
    ('Permissions');

INSERT INTO users (fullname, contact, type_id, email, password_hash)
VALUES
    ('Alice Watson', '1234567890', 1, 'alice1982@yahoo.com', '...'),
    ('Charles Hicks', '9876543210', 2, 'cahrlesh4@outlook.com', '...'),
    ('Will Mitchell', '5551234567', 3, 'mitchel91@gmail.com', '...');

INSERT INTO health_records (user_id, record_date, record_text)
VALUES
    (1, '2023-01-15', 'Annual physical check-up. All vitals are normal.'),
    (1, '2023-04-20', 'Flu symptoms. Prescribed medication.'),
    (1, '2023-07-10', 'Injury treatment. X-ray performed.'),
    (2, '2023-02-20', 'Routine dental check-up. No cavities detected.'),
    (2, '2023-05-05', 'Stomach ache. Treated with antibiotics.'),
    (3, '2023-03-10', 'Blood test for cholesterol levels. Results pending.'),
    (3, '2023-06-25', 'Follow-up appointment for hypertension.');

INSERT INTO healthcare_providers (provider_name, provider_address, provider_contact)
VALUES
    ('Etobicoke General Hospital', '123 Main St, Etobicoke, ON M9C 3S8', '123-456-7890'),
    ('Lakefront Walk-In Clinic', '456 Oak Ave, Brampton, ON L6T 3W8', '987-654-3210'),
    ('Downtown Medical Center', '789 Elm St, Toronto, ON M5S 2V6', '555-123-4567');

INSERT INTO user_provider (user_id, provider_id)
VALUES
    (1, 1),
    (2, 2),
    (3, 3);

INSERT INTO reminders (user_id, reminder_text, reminder_date)
VALUES
    (1, 'Schedule MRI appointment', '2024-01-05 10:00:00'),
    (1, 'Renew prescription', '2024-02-15 09:00:00'),
    (2, 'Annual check-up due soon', '2024-03-20 14:30:00'),
    (2, 'Medication refill due next week', '2024-04-25 08:00:00'),
    (3, 'Follow-up appointment for blood test results', '2024-05-30 11:00:00');


-- Add Default credentials to the users
INSERT INTO permissions (resource_id, type_id, can_add, can_view, can_edit)
VALUES 
    (1, 1, 1, 1, 1), 
    (2, 1, 1, 1, 1), 
    (3, 1, 1, 1, 1), 
    (4, 1, 1, 1, 1), 
    (5, 1, 1, 1, 1), 

    (1, 2, 0, 1, 0), 
    (2, 2, 1, 1, 1), 
    (3, 2, 0, 1, 0),
    (4, 2, 0, 1, 0), 
    (5, 2, 0, 0, 0), 

    (1, 3, 0, 0, 0), 
    (2, 3, 1, 1, 1), 
    (3, 3, 0, 1, 0), 
    (4, 3, 0, 1, 0), 
    (5, 3, 0, 0, 0); 