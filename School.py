from flask import Flask,render_template,request,jsonify,redirect,url_for
import mysql.connector
import uuid


app = Flask(__name__)

host = "localhost"
user = "root"
password=""
database="SchoolProject"


@app.route('/')
def hello_world():
   return render_template("index.html")

@app.route('/AddStudents')
def AddStudents():
   return render_template("AddStudents.html")

@app.route('/StudentsDetails')
def StudentsDetails():
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
    return render_template('ViewStudents.html',details=details[0])
    
@app.route('/get-names')
def get_names():
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
        cursor.execute(f"INSERT INTO `students`(`ID`, `NAME`, `ADMN NO`, `CLASS`, `DOB`, `FATHER NUMBER`, `FATHER`, `MOTHER`, `ADDRESS`, `MOTHER NUMBER`, `STUDENT ID`) VALUES ('{id}','{name}','{admn}','{class_name}','{date_of_birth}','{father_number}','{father}','{mother}','{address}','{mother_number}','{random_string}')")
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


if __name__ == '__main__':
   app.run()