from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DATABASE = 'student.db'

# Create table
def create_table():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT NOT NULL,
            dob TEXT NOT NULL,
            course TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

create_table()

# Home page / list students
@app.route('/')
def form():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students')
    students = cursor.fetchall()
    conn.close()
    return render_template('form.html', students=students)

# Add student
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    dob = request.form['dob']
    course = request.form['course']

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO students (name,email,phone,dob,course) VALUES (?,?,?,?,?)",
        (name, email, phone, dob, course)
    )
    conn.commit()
    conn.close()
    return redirect(url_for('form'))

# Delete student
@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('form'))

# Update student
@app.route('/update/<int:id>', methods=['GET','POST'])
def update_student(id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        dob = request.form['dob']
        course = request.form['course']

        cursor.execute(
            "UPDATE students SET name=?, email=?, phone=?, dob=?, course=? WHERE id=?",
            (name, email, phone, dob, course, id)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('form'))

    # For GET request, fetch student data
    cursor.execute("SELECT * FROM students WHERE id=?", (id,))
    student = cursor.fetchone()
    conn.close()
    return render_template('update.html', student=student)

if __name__ == "__main__":
    app.run(debug=True)
