import mysql.connector
import uuid

try:
  connection = mysql.connector.connect(
      host="localhost",
      user="root",
      password=""
  )

  create_database_query = "CREATE DATABASE SchoolProject"
  cursor = connection.cursor()
  cursor.execute(create_database_query)

  use_database_query = "USE SchoolProject"
  cursor.execute(use_database_query)

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

  user_data_table_query = """
  CREATE TABLE user_data (
    Name VARCHAR(50) NOT NULL,
    UserName VARCHAR(100) NOT NULL,
    Password VARCHAR(100) NOT NULL,
    PhoneNumber VARCHAR(13) NOT NULL,
    acc_type VARCHAR(10) NOT NULL,
    `ID` VARCHAR(100) NOT NULL
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
  """
  random_uuid = uuid.uuid4()
  random_string = str(random_uuid)
  def check():
    global name, UserName,Password,PhoneNumber
    name = input("Enter Admin Name: ")
    UserName = input("Enter Admin UserName: ")
    PhoneNumber = input("Enter PhoneNumber: ")
    Password = input("Enter Admin Password: ")
    RePassword = input("Enter Admin Password Again: ")

    if Password != RePassword:
      print("Passwords Doesn't Match")
      check()
    else:
      pass
  check()
  user_data_insert = f"""
  INSERT INTO `user_data` (`Name`, `UserName`, `Password`, `PhoneNumber`, `acc_type`, `ID`) VALUES
  ('{name}', '{UserName}', '{Password}', '{PhoneNumber}', 'Admin','{random_string}');
  """

  cursor.execute(students_table_query)
  cursor.execute(user_data_table_query)
  cursor.execute(user_data_insert)

  connection.commit()
  connection.close()
  print("Database Created Successfully!!!")
except Exception as e:
  if "database exists" in str(e):
    print("Database Exists! Delete Existing One")
  else:  print(f"Error While Creating Database: {e}")
