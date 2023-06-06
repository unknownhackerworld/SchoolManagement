from flask import Flask,render_template,request,jsonify,redirect,url_for,make_response
from werkzeug.utils import secure_filename
import mysql.connector
import uuid
import json
import os
import firebase_admin
from firebase_admin import credentials, storage
import datetime


cred = credentials.Certificate('./firebase_key.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'schoolproject-allen.appspot.com'
})



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'  # Specify the upload folder here


host = "localhost"
user = "root"
password=""
database="SchoolProject"

def check_db_connection():
    try:
        mysql.connector.connect(
            host=host,
            user=user,
            database=database,
            password=password
        )
    except mysql.connector.Error as error:
        print('Database connection error:', error)
        return False

    return True

@app.route('/')
def Home():
   return render_template("password.html")



@app.route('/AddStudents')
def AddStudents():
    if 'userType' not in request.cookies or 'userName' not in request.cookies:
        return redirect(url_for('Home'))
    else:
        return render_template("AddStudents.html")
    
    


@app.route('/StudentsDetails')
def StudentsDetails():
    if 'userType' not in request.cookies or 'userName' not in request.cookies:
        return redirect(url_for('Home'))
    
    if not check_db_connection():
        return f'''
        <script>
        alert("Database is not connected.");
        window.location.href = {url_for('StudentsDetails')};

        </script>
        '''
    
    db = mysql.connector.connect(
        host=host,
        user=user,
        database=database,
        password=password

    )
    cursor = db.cursor()
    cursor.execute("SELECT `NAME`,`FATHER`,`STUDENT ID` FROM students")
    names = [[row[0],row[1],row[2]] for row in cursor.fetchall()]
    db.close()
    return render_template('StudentsDetails.html', names=names)


@app.route('/ViewStudents', methods=['POST'])
def process():
    if 'userType' not in request.cookies or 'userName' not in request.cookies:
        return redirect(url_for('Home'))
    
    if not check_db_connection():
        return f'''
        <script>
        alert("Database is not connected.");
        window.location.href = {url_for('StudentsDetails')};

        </script>
        '''
     
    value = request.form['value']
    db = mysql.connector.connect(
    host=host,
    user=user,
    database=database,
    password=password
)

    cursor = db.cursor()

    cursor.execute(f"SELECT * FROM students WHERE `STUDENT ID` = '{value}'")
    details = cursor.fetchall()

    cursor.execute(f"SELECT UserName FROM user_data WHERE `ID` = '{value}'")
    userName = cursor.fetchone()

    
    mark = sum(details[0][-4:])

    print(details)
    return render_template('ViewStudents.html', details=details[0], mark=mark, username=userName[0])

    
@app.route('/get-names')
def get_names():
    if 'userType' not in request.cookies or 'userName' not in request.cookies:
        return redirect(url_for('Home'))
    
    if not check_db_connection():
        return '''
        <script>
        alert("Database is not connected.");
        window.location.href = window.location.href;

        </script>
        '''
     
    if request.args.get('start') or request.args.get('end'):
        start = int(request.args.get('start'))
        end = int(request.args.get('end'))
    else:
        start = ''        
        end = ''

    if request.args.get('search'):
        search = str(request.args.get('search'))
    else:
        search = ''

    try:
        # Connect to MySQL database
        db = mysql.connector.connect(
             host=host,
        user=user,
        database=database,
        password=password
        )
        cursor = db.cursor()
        query = f"SELECT NAME,`STUDENT ID` FROM students WHERE NAME LIKE '%{search}%' ORDER BY name"
        query2 = f"SELECT NAME,`STUDENT ID` FROM students ORDER BY name LIMIT {start}, {end}"

        if search:
            cursor.execute(query)
            
        else:
            cursor.execute(query2)
               
        
        result = cursor.fetchall()
        # Convert the result to a list of dictionaries
        names = [{'name': row[0], 'value': row[1]} for row in result]

        # Close the cursor and connection
        cursor.close()
        db.close()

        return jsonify(names)

    except mysql.connector.Error as error:
        print('Error retrieving names:', error)
        return jsonify([])
    
@app.route('/AddData', methods=['POST'])
def AddData():
    if 'userType' not in request.cookies or 'userName' not in request.cookies:
        return redirect(url_for('Home'))
    
    if not check_db_connection():
        return f'''
        <script>
        alert("Database is not connected.");
        window.location.href = {url_for('AddStudents')};

        </script>
        '''
     
    random_uuid = uuid.uuid4()
    random_string = str(random_uuid)

    name = request.form['name']
    class_name = request.form['class']
    date_of_birth = request.form['dateOfBirth']
    father_number = request.form['fatherNumber']
    father = request.form['father']
    mother = request.form['mother']
    address = request.form['address']
    mother_number = request.form['motherNumber']

    db = mysql.connector.connect(
        host=host,
        user=user,
        database=database,
        password=password
    )
    cursor = db.cursor()
    cursor.execute("SELECT ID, `ADMN NO` FROM students ORDER BY ID DESC LIMIT 1")
    a = cursor.fetchall()
    if a != []:
        id = int(a[0][0]) + 1
        admn = int(a[0][1]) + 1
    else:
        id = 1
        admn = 1

    try:
        cursor.execute(f"INSERT INTO `students` (`ID`, `NAME`, `ADMN NO`, `CLASS`, `DOB`, `FATHER NUMBER`, `FATHER`, `MOTHER`, `ADDRESS`, `MOTHER NUMBER`, `STUDENT ID`,`TEST_1`,`TEST_2`,`TEST_3`,`TEST_4`) VALUES ('{id}','{name}','{admn}','{class_name}','{date_of_birth}','{father_number}','{father}','{mother}','{address}','{mother_number}','{random_string}','0','0','0','0')")

        cursor.execute(f"INSERT INTO `user_data` (`Name`, `UserName`, `Password`, `PhoneNumber`, `acc_type`,`ID`) VALUES ('{name}', '{f'XYZCPT{admn}'}', 'XYZStud@2023', '{father_number}', 'Student','{random_string}'); ")
        db.commit()
        return redirect(url_for('StudentsDetails'))
    except Exception as e:
        return f'''
        <script>
            alert("There Is Some Error: {e}");
            window.location.href = "{url_for('StudentsDetails')}";
        </script>
        '''
    finally:
        return redirect(url_for('StudentsDetails'))

@app.route('/EditStudents')
def EditStudents():
    if 'userType' not in request.cookies or 'userName' not in request.cookies:
        return redirect(url_for('Home'))
    
    if not check_db_connection():
        return '''
        <script>
        alert("Database is not connected.");
        window.location.href = window.location.href;

        </script>
        '''
     
    db = mysql.connector.connect(
        host=host,
        user=user,
        database=database,
        password=password
    )
    cursor = db.cursor()
    cursor.execute("SELECT * FROM students")
    columns = [column[0] for column in cursor.description]
    students = [dict(zip(columns, student)) for student in cursor.fetchall()]
    form_data = json.dumps(students)  # Convert students data to JSON format
    return render_template('EditStudents.html', form_data=form_data, students=students)

@app.route('/Edit',methods=['POST'])
def Edit():
    if 'userType' not in request.cookies or 'userName' not in request.cookies:
        return redirect(url_for('Home'))
    
    if not check_db_connection():
        return f'''
        <script>
        alert("Database is not connected.");
        window.location.href = {url_for('EditStudents')};

        </script>
        '''
     
    admn = request.form['admn']
    id = request.form['id']
    student_id = request.form['studentId']
    name = request.form['name']
    class_name = request.form['class']
    date_of_birth = request.form['dateOfBirth']
    father_number = request.form['fatherNumber']
    father = request.form['father']
    mother = request.form['mother']
    address = request.form['address']
    mother_number = request.form['motherNumber']

    db = mysql.connector.connect(
        host=host,
        user=user,
        database=database,
        password=password
    )
    cursor = db.cursor()

    try:
        cursor.execute(f"UPDATE students SET ID = '{id}', NAME = '{name}', `ADMN NO` = '{admn}', CLASS = '{class_name}', DOB = '{date_of_birth}', `FATHER NUMBER` = '{father_number}', FATHER = '{father}', MOTHER = '{mother}', ADDRESS = '{address}', `MOTHER NUMBER` = '{mother_number}', `STUDENT ID` = '{student_id}' WHERE `STUDENT ID` = '{student_id}'")
        db.commit()
        return redirect(url_for('StudentsDetails'))
    except Exception as e:
        return f'''
        <script>
            alert("There Is Some Error: {e}");
            window.location.href = "{url_for('StudentsDetails')}";
        </script>
        '''
@app.route('/MarkEdit',methods=['POST'])
def MarkEdit():
    if 'userType' not in request.cookies or 'userName' not in request.cookies:
        return redirect(url_for('Home'))
    
    if not check_db_connection():
        return f'''
        <script>
        alert("Database is not connected.");
        window.location.href = {url_for('StudentsReport')};

        </script>
        '''
     
    test1 = request.form['TEST1']
    test2 = request.form['TEST2']
    test3 = request.form['TEST3']
    test4 = request.form['TEST4']
    student_id = request.form['studentId']

    db = mysql.connector.connect(
        host=host,
        user=user,
        database=database,
        password=password
    )
    cursor = db.cursor()
   

    try:
        cursor.execute(f"UPDATE students SET `TEST_1` = '{test1}', `TEST_2` = '{test2}', `TEST_3` = '{test3}',`TEST_4` = '{test4}' WHERE `STUDENT ID` = '{student_id}'")
        db.commit()
        return redirect(url_for('StudentsReport'))
    except Exception as e:
        return f'''
        <script>
            alert("There Is Some Error: {e}");
            window.location.href = "{url_for('StudentsReport')}";
        </script>
        '''    
    

@app.route('/StudentsReport')
def StudentsReport():
    if 'userType' not in request.cookies or 'userName' not in request.cookies:
        return redirect(url_for('Home'))
    
    if not check_db_connection():
        return '''
        <script>
        alert("Database is not connected.");
        window.location.href = window.location.href;

        </script>
        '''
     
    db = mysql.connector.connect(
        host=host,
        user=user,
        database=database,
        password=password
    )
    cursor = db.cursor()
    cursor.execute("SELECT NAME,TEST_1,TEST_2,TEST_3,TEST_4,`STUDENT ID` FROM students")
    columns = [column[0] for column in cursor.description]
    students = [dict(zip(columns, student)) for student in cursor.fetchall()]
    form_data = json.dumps(students)  
    return render_template('StudentsReport.html',form_data=form_data, students=students)

@app.route('/Admin')
def Admin():
    if 'userType' not in request.cookies or 'userName' not in request.cookies:
        return redirect(url_for('Home'))
     
    return render_template('Admin.html')

@app.route('/Students')
def Student():
    if 'userType' not in request.cookies or 'userName' not in request.cookies:
        return redirect(url_for('Home'))
     
    return render_template('Student.html')

@app.route('/login')
def EnterPassword():
    
     
    return render_template('password.html')

@app.route('/CheckData',methods=['POST'])
def CheckData():
    userType = request.form['user']
    UserName = request.form['username']
    PassWord = request.form['password']

    if not check_db_connection():
        return f'''
        <script>
        alert("Database is not connected.");
        window.location.href = "{url_for('EnterPassword')}";

        </script>
        '''

    db = mysql.connector.connect(
        host=host,
        user=user,
        database=database,
        password=password
    )
    cursor = db.cursor()
    cursor.execute(f"SELECT Password,acc_type,UserName,ID FROM user_data WHERE UserName = '{UserName}'")
    data = cursor.fetchall()
    if data == []:
        return f'''
        <script>
            alert("No UserName Found");
            window.location.href = "{url_for('EnterPassword')}";
        </script>'''
    elif (PassWord != data[0][0]) and (UserName == data[0][2]):
        return f'''
        <script>
            alert("Incorrect Password");
            window.location.href = "{url_for('EnterPassword')}";
        </script>
        '''
    elif (PassWord == data[0][0]) and (userType == data[0][1]):
        response = make_response(redirect(url_for(userType)))

        # Set the 'UserName' and 'userType' cookies
        response.set_cookie('userName', UserName)
        response.set_cookie('userType', userType)
        response.set_cookie('ID', data[0][3])

        return response

@app.route('/Grades')
def StudentGrades():

    if 'userType' not in request.cookies or 'userName' not in request.cookies:
        return redirect(url_for('Home'))
    
    if not check_db_connection():
        return '''
        <script>
        alert("Database is not connected.");
        window.location.href = window.location.href;

        </script>
        '''
     
    db = mysql.connector.connect(
        host=host,
        user=user,
        database=database,
        password=password
    )
    cursor = db.cursor()
    cursor.execute(f"SELECT NAME,TEST_1,TEST_2,TEST_3,TEST_4 FROM students WHERE `STUDENT ID` = '{request.cookies['ID']}'")
    Grades  = cursor.fetchall()
    if Grades == []:
        return f'''
        <script>alert("Cannot Retrieve Grades");
        window.location.href = '{url_for('Student')}'
        </script>
        '''
    
    return render_template('StudentGrades.html',grades=Grades[0])


@app.route('/UploadAssignment')
def UploadAssignment():
    if 'userType' not in request.cookies or 'userName' not in request.cookies:
        return redirect(url_for('Home'))
     
    bucket = storage.bucket()
    blobs = bucket.list_blobs()
    assignment_urls = []
    filenames = []
    for blob in blobs:
        filenames.append(blob.name)  # Extract only the filename without the "Assignments/" prefix
        assignment_urls.append(blob.generate_signed_url(expiration=datetime.timedelta(days=1)))
    return render_template('UploadAssignments.html',assignment_urls=assignment_urls, filenames=filenames)


@app.route('/upload-assignment', methods=['POST'])
def upload_assignment():
    if 'userType' not in request.cookies or 'userName' not in request.cookies:
        return redirect(url_for('Home'))
     
    file = request.files['file']
    if file:
        filename = secure_filename(file.filename)
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(temp_path)
        bucket = storage.bucket()
        blob = bucket.blob(filename)
        blob.upload_from_filename(temp_path)
        os.remove(temp_path)
        return redirect(url_for('UploadAssignment'))
    else:
        return 'No file selected.'

@app.route('/assignments')
def assignments():
    if 'userType' not in request.cookies or 'userName' not in request.cookies:
        return redirect(url_for('Home'))
     
    bucket = storage.bucket()
    blobs = bucket.list_blobs()
    assignment_urls = []
    filenames = []
    for blob in blobs:
        filenames.append(blob.name)  # Extract only the filename without the "Assignments/" prefix
        assignment_urls.append(blob.generate_signed_url(expiration=datetime.timedelta(days=1)))
    return render_template('GetAssignments.html', assignment_urls=assignment_urls, filenames=filenames)

@app.route('/profile')
def Profile():
    if 'userType' not in request.cookies or 'userName' not in request.cookies:
        return redirect(url_for('Home'))
    
    if not check_db_connection():
        return '''
        <script>
        alert("Database is not connected.");
        window.location.href = window.location.href;

        </script>
        '''
     
    UserName = request.cookies.get('userName')

    db = mysql.connector.connect(
        host=host,
        user=user,
        database=database,
        password=password
    )
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM user_data WHERE UserName = '{UserName}'")
    data = cursor.fetchall()

    return render_template('Profile_Student.html',data=data[0])

@app.route('/admin_profile')
def Profile_Admin():
    if 'userType' not in request.cookies or 'userName' not in request.cookies:
        return redirect(url_for('Home'))
    
    if not check_db_connection():
        return '''
        <script>
        alert("Database is not connected.");
        window.location.href = window.location.href;

        </script>
        '''
     
    UserName = request.cookies.get('userName')

    db = mysql.connector.connect(
        host=host,
        user=user,
        database=database,
        password=password
    )
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM user_data WHERE UserName = '{UserName}'")
    data = cursor.fetchall()
    print(data)

    return render_template('Profile_Admin.html',data=data[0])



if __name__ == '__main__':
   app.run()