import sqlite3   #enable control of an sqlite database
import csv       #facilitates CSV I/O


f="discobandit.db"

db = sqlite3.connect(f) #open if f exists, otherwise create
c = db.cursor()    #facilitate db ops

#==========================================================
#INSERT YOUR POPULATE CODE IN THIS ZONE

#Create two tables
c.execute('CREATE TABLE courses(code TEXT, mark INTEGER, id INTEGER)' )
c.execute('CREATE TABLE peeps(name TEXT, age INTEGER, id INTEGER)' )

#Insert data
course_file = csv.DictReader(open('courses.csv'))
for row in course_file:
    c.execute('INSERT INTO courses VALUES (?, ?, ?)', (row['code'], row['mark'], row['id']))

peep_file = csv.DictReader(open('peeps.csv'))
for row in peep_file:
    c.execute('INSERT INTO peeps VALUES (?, ?, ?)', (row['name'], row['age'], row['id']))

#Get the data of specific student with their name
def get_data(name):
    c.execute("SELECT name, code, mark FROM peeps, courses WHERE courses.id = peeps.id AND '%s'=name;" %(name))
    data = c.fetchall()
    return data

#Get the grade of specific student with their name
def get_grade(name):
    data = get_data(name)
    grades = []
    for grade in data:
        grades.append(grade[2])
    return grades

#Get the average of specific student with their name
def get_avg(name):
    sum = 0.0
    grades = get_grade(name)
    for grade in grades:
        sum += int(grade)
    return sum / len(grades)

#Create table for student's average
c.execute('CREATE TABLE peeps_avg(name TEXT, id INTEGER, avg NUMERICAL)')

#Insert data
c.execute('SELECT name, id FROM peeps;')
data = c.fetchall()
for each in data:
    c.execute('INSERT INTO peeps_avg VALUES (?, ?, ?)', ( each[0], each[1], get_avg(each[0]) ))

#Display each student's name, id, and average
def display():
    c.execute('SELECT name, id, avg FROM peeps_avg;')
    data = c.fetchall()
    for each in data:
        s = str(each[0])
        x = len(s)
        while x <= 12:
            s = s + " "
            x = x + 1
        x = len(str(each[1]))
        while x < 5:
            s = s + " "
            x = x + 1
        s = s + str(each[1]) + "   " + str(each[2])
        print s

print display()
    
#Update method
def update():
    c.execute('SELECT * FROM peeps_avg;')
    data = c.fetchall()
    for each in data:
        c.execute("UPDATE peeps_avg SET avg = %d WHERE name='%s';" % (get_avg(each[0]), each[0]))
    print display()

#Test Case of update
c.execute("INSERT INTO courses VALUES('math', 85, 3)")
c.execute("INSERT INTO courses VALUES('math', 90, 4)")
c.execute("INSERT INTO courses VALUES('math', 100, 5)")
c.execute("INSERT INTO courses VALUES('gym', 87, 5)")

update()
#==========================================================
db.commit() #save changes
db.close()  #close database


