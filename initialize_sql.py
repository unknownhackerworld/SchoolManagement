import mysql.connector

# Connect to the MySQL server
connection = mysql.connector.connect(
    host="your_host",
    user="your_username",
    password="your_password",
    database="your_database"
)

# Create the 'students' table
students_table_query = """
CREATE TABLE students (
  ID INT(5) DEFAULT NULL,
  NAME VARCHAR(54) DEFAULT NULL,
  `ADMN NO` INT(5) DEFAULT NULL,
  CLASS VARCHAR(9) DEFAULT NULL,
  DOB VARCHAR(18) DEFAULT NULL,
  `FATHER NUMBER` VARCHAR(18) DEFAULT NULL,
  `FATHER` VARCHAR(32) DEFAULT NULL,
  `MOTHER` VARCHAR(34) DEFAULT NULL,
  `ADDRESS` VARCHAR(185) DEFAULT NULL,
  `MOTHER NUMBER` VARCHAR(22) DEFAULT NULL,
  `STUDENT ID` VARCHAR(36) DEFAULT NULL,
  `TEST_1` INT(11) NOT NULL,
  `TEST_2` INT(11) NOT NULL,
  `TEST_3` INT(11) NOT NULL,
  `TEST_4` INT(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
"""

# Create the 'user_data' table
user_data_table_query = """
CREATE TABLE user_data (
  Name VARCHAR(50) NOT NULL,
  UserName VARCHAR(100) NOT NULL,
  Password VARCHAR(100) NOT NULL,
  PhoneNumber VARCHAR(13) NOT NULL,
  acc_type VARCHAR(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
"""

user_data_insert = """
INSERT INTO `user_data` (`Name`, `UserName`, `Password`, `PhoneNumber`, `acc_type`) VALUES
('Alice Bob', 'Admin', 'Admin', '1234567890', 'Admin');
COMMIT;
"""

# Execute the queries to create the tables
cursor = connection.cursor()
cursor.execute(students_table_query)
cursor.execute(user_data_table_query)
cursor.execute(user_data_insert)

# Commit the changes and close the connection
connection.commit()
connection.close()
