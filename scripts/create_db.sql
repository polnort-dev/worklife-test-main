-- Create the team table
CREATE TABLE IF NOT EXISTS team (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    team_name VARCHAR(30) NOT NULL
);

-- Create the employee table
CREATE TABLE IF NOT EXISTS employee (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    first_name VARCHAR(30) NOT NULL,
    last_name VARCHAR(30) NOT NULL,
    team_id UUID,
    FOREIGN KEY (team_id) REFERENCES team(id)
);

-- Create the enum type for vacation type
CREATE TYPE vacation_type AS ENUM ('Unpaid leave', 'Paid leave');

-- Create the vacation table
CREATE TABLE IF NOT EXISTS vacation (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    type vacation_type NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    employee_id UUID,
    FOREIGN KEY (employee_id) REFERENCES employee(id)
);

-- Insert sample data into the team table
INSERT INTO team (team_name) VALUES ('Commercial');
INSERT INTO team (team_name) VALUES ('Developpement');

-- Insert sample data into the employee table
INSERT INTO employee (first_name, last_name, team_id) VALUES ('Jean', 'Dujardin', (SELECT id FROM team WHERE team_name = 'Commercial'));
INSERT INTO employee (first_name, last_name, team_id) VALUES ('Paul', 'Personne', (SELECT id FROM team WHERE team_name = 'Developpement'));

-- Insert sample data into the vacation table
INSERT INTO vacation (type, start_date, end_date, employee_id) VALUES ('Paid leave', '2024-12-21', '2025-01-05', (SELECT id FROM employee WHERE first_name = 'Jean' AND last_name = 'Dujardin'));
INSERT INTO vacation (type, start_date, end_date, employee_id) VALUES ('Unpaid leave', '2025-05-02', '2025-05-09', (SELECT id FROM employee WHERE first_name = 'Paul' AND last_name = 'Personne'));
