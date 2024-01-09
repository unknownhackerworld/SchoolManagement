import mysql.connector
import uuid
from getpass import getpass
import os


try:
  from flask import Flask, render_template, request, jsonify, redirect, url_for, make_response
  from werkzeug.utils import secure_filename
  import firebase_admin
  from firebase_admin import credentials, storage

except:
  os.system('pip install -r requirements.txt')

host = "localhost"
user = "root"
password=""

def check_db_connection():
    try:
        mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
    except mysql.connector.Error as error:
        print('Database connection error:', error)
        return False

    return True

try:
  if not check_db_connection():
    print("\nDatabase Not Connected")
    quit()

  def check():
    connection_new = mysql.connector.connect(
      host=host,
      user=user,
      password=password,database="SchoolProject"
    )
  
    cur = connection_new.cursor()
  
  
    global name, UserName,Password,PhoneNumber
    name = input("Enter Admin Name: ")
    UserName = input("Enter Admin UserName: ")
    cur.execute(f"SELECT UserName FROM user_data WHERE UserName = '{UserName}'")
    data = cur.fetchall()    
    if data != []:
       print("Username Exists! Please Enter New Username\n")
       check()
    PhoneNumber = input("Enter PhoneNumber: ")
    Password = getpass("Enter Admin Password: ")
    RePassword = getpass("Enter Admin Password Again: ")



    if Password != RePassword:
      print("Passwords Doesn't Match\n")
      check()
    
  check()
  connection = mysql.connector.connect(
      host=host,
      user=user,
      password=password
  )

  create_database_query = "CREATE DATABASE IF NOT EXISTS SchoolProject"
  cursor = connection.cursor()
  cursor.execute(create_database_query)

  use_database_query = "USE SchoolProject"
  cursor.execute(use_database_query)

  students_table_query = """
  CREATE TABLE IF NOT EXISTS students (
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
  CREATE TABLE IF NOT EXISTS user_data (
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
  print(f"UserName: {UserName}, Password: {Password}")


except Exception as e:
  if "database exists" in str(e):
    print("Database Exists! Delete Existing One")
  else:  print(f"Error While Creating Database: {e}")
