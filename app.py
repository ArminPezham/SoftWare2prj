from flask import Flask,render_template,request#1
from uuid import uuid4
import pymysql
conn=pymysql.connect(host='localhost',user='root',password='armin1379',db='swprj')
curr=conn.cursor()
app=Flask(__name__,template_folder='D:\programming\SW2prj')
def generate():
    return uuid4().int & (1<<16)-1
@app.route('/')
def home():
    return render_template('Base.html')
@app.route('/teachers',methods=['POST','GET'])
def teachers():
    if request.method=='POST':
        if request.form['submit']=='add':
            id=request.form['id']
            fname=request.form['fname']
            lname=request.form['lname']
            curr.execute('insert into teacher(tid,fname,lname) values ({},"{}","{}")'.format(id,fname,lname))
            conn.commit()
        else:
            id=request.form['id']
            curr.execute('delete from teacher where tid={}'.format(id))
    curr.execute('select tid,fname,lname from teacher')
    teachers=curr.fetchall()
    return render_template('teachers.html',teachers=teachers)
@app.route('/students',methods=['POST','GET'])
def students():
    if request.method=='POST':
        if request.form['submit']=='add':
            id=request.form['id']
            fname=request.form['fname']
            lname=request.form['lname']
            curr.execute('insert into student(sid,fname,lname) values ({},"{}","{}")'.format(id,fname,lname))
            conn.commit()
        else:
            id=request.form['id']
            curr.execute('delete from student where sid={}'.format(id))
            conn.commit()
    curr.execute('select sid,fname,lname from student')
    students=curr.fetchall()
    return render_template('students.html',students=students)
@app.route('/lessons',methods=['POST','GET'])
def lessons():
    if request.method=='POST':
        if request.form['submit']=='add':
            id=generate()
            weight=request.form['weight']
            name=request.form['name']
            curr.execute('insert into lesson(lid,weight,title) values ({},{},"{}")'.format(id,weight,name))
            conn.commit()
        else:
            id=request.form['id']
            curr.execute('delete from lesson where lid={}'.format(id))
            conn.commit()
    curr.execute('select lid,weight,title from lesson')
    lessons=curr.fetchall()
    return render_template('lessons.html',lessons=lessons)
@app.route('/classes',methods=['POST','GET'])
def classes():
    if request.method=='POST':
        if request.form['submit']=='add':
            lid=request.form['lid']
            tid=request.form['tid']
            cday=request.form['day']
            chour=request.form['hour']
            cminute=request.form['minute']
            curr.execute('insert into class(lid,tid,cday,chour,cminute) values ({},{},"{}",{},{})'.format(lid,tid,cday,chour,cminute))
            conn.commit()
        else:
            lid=request.form['lid']
            cday=request.form['day']
            chour=request.form['hour']
            cminute=request.form['minute']
            curr.execute('delete from class where lid={} and cday="{}" and chour={} and cminute={}'.format(lid,cday,chour,cminute))
            conn.commit()
    sql='select lesson.lid,title,cday,chour,cminute,teacher.tid,fname,lname from class,lesson,teacher where class.lid=lesson.lid and teacher.tid=class.tid'
    curr.execute(sql)
    classes=curr.fetchall()
    return render_template('classes.html',classes=classes)
@app.route('/schedules',methods=['POST','GET'])
def scheduals():
    if request.method=='POST':
        tid=request.form['id']
        curr.execute('select fname,lname from teacher where tid={}'.format(tid))
        name=curr.fetchall()
        name='{} {}'.format(name[0][0],name[0][1])
        curr.execute('select lesson.lid,title,cday,chour,cminute from lesson,class where class.lid=lesson.lid and tid={}'.format(tid))
        classes=curr.fetchall()
        return render_template('schedules.html',classes=classes,name=name)
    return render_template('schedules.html')
@app.route('/reports',methods=['POST','GET'])
def reports():
    if request.method=='POST':
        if request.form['submit']=='add':
            sid=request.form['sid']
            lid=request.form['lid']
            mark1=request.form['term1']
            mark2=request.form['term2']
            mark3=request.form['final1']
            mark4=request.form['final2']
            curr.execute('insert into section(lid,sid,term1,fianl1,term2,final2) values ({},{},{},{},{},{})'.format(lid,sid,mark1,mark3,mark2,mark4))
            conn.commit()
        else:
            sid=request.form['sid']
            lid=request.form['lid']
            curr.execute('delete from section where lid={} and sid={}'.format(lid,sid))
            conn.commit()
    curr.execute('select lid,sid,term1,fianl1,term2,final2 from section')
    sections=curr.fetchall()
    return render_template('reports.html',sections=sections)
@app.route('/studentreport',methods=['POST','GET'])
def student_report():
    if request.method=='POST':
        sid=request.form['id']
        curr.execute('select fname,lname from student where sid={}'.format(sid))
        temp=curr.fetchall()
        name='{} {}'.format(temp[0][0],temp[0][1])
        curr.execute('select sid,section.lid,title,term1,fianl1,term2,final2 from section,lesson where lesson.lid=section.lid and sid={}'.format(sid))
        datas=curr.fetchall()
        return render_template('student_report.html',name=name,datas=datas)
    return render_template('student_report.html')
if __name__=="__main__":
    app.run(debug=True)