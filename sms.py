from tkinter import *
import time
import ttkthemes
from tkinter import ttk,messagebox,filedialog,simpledialog
import pymysql
import pandas
from collections import Counter
import re

#functionality part
def iexit():
    result=messagebox.askyesno('confirm','Do you want to exit')
    if result:
        root.destroy()
    else:
        pass

def export_data():
    url=filedialog.asksaveasfilename(defaultextension='.csv')
    indexing=studentTable.get_children()
    newlist=[]
    for index in indexing:
        content= studentTable.item(index)
        datalist=content['values']
        newlist.append(datalist)
    table=pandas.DataFrame(newlist,columns=['ID','NAME','MOBILE NO','EMAIL','ADDRESS','GENDER','DOB','ADDED DATE','ADDED TIME'])
    table.to_csv(url,index=False)
    messagebox.showinfo('Success','Data is saved successfully')
    print(table)

def toplevel_data(title,button_text,command):
    global idEntry,nameEntry,mobileEntry,emailEntry,addressEntry,genderEntry,dobEntry,screen
    screen=Toplevel()
    screen.title(title)
    screen.grab_set()
    screen.resizable(False, False)
    idLabel = Label(screen, text='ID', font=('times new roman', 20, 'bold'))
    idLabel.grid(row=0, column=0, padx=30, pady=15, sticky=W)
    idEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    idEntry.grid(row=0, column=1, pady=15, padx=10)

    nameLabel = Label(screen, text='NAME', font=('times new roman', 20, 'bold'))
    nameLabel.grid(row=1, column=0, padx=30, pady=15, sticky=W)
    nameEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    nameEntry.grid(row=1, column=1, pady=15, padx=10)

    mobileLabel = Label(screen, text='MOBILE NO', font=('times new roman', 20, 'bold'))
    mobileLabel.grid(row=2, column=0, padx=30, pady=15, sticky=W)
    mobileEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    mobileEntry.grid(row=2, column=1, pady=15, padx=10)

    emailLabel = Label(screen, text='EMAIL', font=('times new roman', 20, 'bold'))
    emailLabel.grid(row=3, column=0, padx=30, pady=15, sticky=W)
    emailEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    emailEntry.grid(row=3, column=1, pady=15, padx=10)

    addressLabel = Label(screen, text='ADDRESS', font=('times new roman', 20, 'bold'))
    addressLabel.grid(row=4, column=0, padx=30, pady=15, sticky=W)
    addressEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    addressEntry.grid(row=4, column=1, pady=15, padx=10)

    genderLabel = Label(screen, text='GENDER', font=('times new roman', 20, 'bold'))
    genderLabel.grid(row=5, column=0, padx=30, pady=15, sticky=W)
    genderEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    genderEntry.grid(row=5, column=1, pady=15, padx=10)

    dobLabel = Label(screen, text='D.O.B', font=('times new roman', 20, 'bold'))
    dobLabel.grid(row=6, column=0, padx=30, pady=15, sticky=W)
    dobEntry = Entry(screen, font=('roman', 15, 'bold'), width=24)
    dobEntry.grid(row=6, column=1, pady=15, padx=10)

    student_button = ttk.Button(screen, text=button_text, command=command)
    student_button.grid(row=7, columnspan=2, pady=15)
    if title=='Update Student':
       indexing = studentTable.focus()

       content = studentTable.item(indexing)
       listdata = content['values']
       idEntry.insert(0, listdata[0])
       nameEntry.insert(0, listdata[1])
       mobileEntry.insert(0, listdata[2])
       emailEntry.insert(0, listdata[3])
       addressEntry.insert(0, listdata[4])
       genderEntry.insert(0, listdata[5])
       dobEntry.insert(0, listdata[6])

def update_data():
    query ='update student set name=%s,mobile=%s,email=%s,address=%s,gender=%s,dob=%s,date=%s,time=%s where id=%s'
    mycursor.execute(query,(nameEntry.get(),mobileEntry.get(),emailEntry.get(),addressEntry.get(),
                            genderEntry.get(),dobEntry.get(),date,currenttime,idEntry.get()))
    con.commit()
    messagebox.showinfo('Success',f' ID {idEntry.get()} is modified sucessfully', parent=screen)
    screen.destroy()
    show_student()


def show_student():
    query = 'select * from student'
    mycursor.execute(query)
    fetched_data = mycursor.fetchall()
    studentTable.delete(*studentTable.get_children())
    for data in fetched_data:
        studentTable.insert('', END, values=data)



def delete_student():
    indexing=studentTable.focus()
    print(indexing)
    content= studentTable.item(indexing)
    content_id=content['values'][0]
    query='delete from student where id=%s'
    mycursor.execute(query,content_id)
    con.commit()
    messagebox.showinfo('Delete',f'This {content_id} is deleted successfully')
    query='select * from student'
    mycursor.execute(query)
    fetched_data = mycursor.fetchall()
    studentTable.delete(*studentTable.get_children())
    for data in fetched_data:
        studentTable.insert('', END, values=data)


def search_data():
    query='select * from student where id=%s or name=%s or mobile=%s or email=%s or address=%s or gender=%s or dob=%s'
    mycursor.execute(query,(idEntry.get(),nameEntry.get(),mobileEntry.get(),emailEntry.get(), addressEntry.get(),genderEntry.get(),dobEntry.get()))
    studentTable.delete(*studentTable.get_children())
    fetched_data=mycursor.fetchall()
    for data in fetched_data:
        studentTable.insert('',END,values=data)
def is_valid_email(email):

    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)
def add_data():
    if idEntry.get()==''or nameEntry.get()==''or mobileEntry.get()==''or emailEntry.get()==''or addressEntry.get()==''or genderEntry.get()==''or dobEntry.get()=='':
       messagebox.showerror('Error','All fields are required',parent=screen)
    elif not is_valid_email(emailEntry.get()):
        messagebox.showerror('Error', 'Invalid email format', parent=screen)
    else:
        try:
           query='insert into student values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
           mycursor.execute(query,(idEntry.get(),nameEntry.get(),mobileEntry.get(),emailEntry.get(), addressEntry.get(),genderEntry.get(),dobEntry.get(),date,currenttime))
           con.commit()
           result=messagebox.askyesno('Confirm','Data added successfully.Do you want to clean the form?',parent=screen)
           if result:
               idEntry.delete(0,END)
               nameEntry.delete(0,END)
               mobileEntry.delete(0,END)
               emailEntry.delete(0,END)
               addressEntry.delete(0,END)
               genderEntry.delete(0,END)
               dobEntry.delete(0,END)
           else:
               pass
        except:
              messagebox.showerror('Error','Id cannot be repeated',parent=screen)
              return
        query='select *from student'
        mycursor.execute(query)
        fetched_data=mycursor.fetchall()
        studentTable.delete(*studentTable.get_children())
        for data in fetched_data:
            studentTable.insert('',END,values=data)


def count_admissions_by_city():
    city = simpledialog.askstring("Input", "Enter the city to count admissions from:", parent=root)
    if city:
        query = 'select address from student'
        mycursor.execute(query)
        fetched_data = mycursor.fetchall()


        cities = [data[0].split(',')[-2].strip() for data in fetched_data if data[0] and len(data[0].split(',')) >= 2]


        city_counts = Counter(cities)


        admission_count = city_counts.get(city, 0)


        messagebox.showinfo('Admission Count', f'Number of admissions from {city}: {admission_count}')
    else:
        messagebox.showwarning('Warning', 'Please enter a city.')

def count_admissions_by_state():
    state = simpledialog.askstring("Input", "Enter the state to count admissions from:", parent=root)
    if state:
        query = 'select address from student'
        mycursor.execute(query)
        fetched_data = mycursor.fetchall()

        # Extract states assuming the address is like 'Street, City, State'
        states = [data[0].split(',')[-1].strip() for data in fetched_data if data[0] and len(data[0].split(',')) >= 2]

        state_counts = Counter(states)

        admission_count = state_counts.get(state, 0)

        messagebox.showinfo('Admission Count', f'Number of admissions from {state}: {admission_count}')
    else:
        messagebox.showwarning('Warning', 'Please enter a state.')



def connect_database():
    def connect():
        global mycursor,con
        try:
           con=pymysql.connect(host='localhost',user='root',password='260804')
           mycursor=con.cursor()
        except:
           messagebox.showerror('Error','Invalid Details',parent= connectWindow)
           return
        try:
           query='create database StudentManagementSystem'
           mycursor.execute(query)
           query='use StudentManagementSystem'
           mycursor.execute(query)
           query='create table student(id varchar(30) not null primary key,name varchar(30),mobile varchar(10),email varchar(30)'\
                'address varchar(50),gender varchar(30),dob varchar(20),date varchar(50),time varchar(50))'
           mycursor.execute(query)
        except:
           query='use StudentManagementSystem'
           mycursor.execute(query)
        messagebox.showinfo('Success','Database Connection is successful', parent=connectWindow)
        connectWindow.destroy()
        addstudentButton.config(state=NORMAL)
        searchstudentButton.config(state=NORMAL)
        updatestudentButton.config(state=NORMAL)
        showstudentButton.config(state=NORMAL)
        exportstudentButton.config(state=NORMAL)
        deletestudentButton.config(state=NORMAL)
        countByCityButton.config(state=NORMAL)
        countByStateButton.config(state=NORMAL)

    connectWindow=Toplevel()
    connectWindow.grab_set()
    connectWindow.geometry('470x250+730+230')
    connectWindow.title('Database Connection')
    root.resizable(0,0)

    hostnameLabel=Label(connectWindow,text='Host Name',font=('arial',20,'bold'))
    hostnameLabel.grid(row=0,column=0,padx=20)

    hostEntry=Entry(connectWindow,font=('roman',15,'bold'),bd=2)
    hostEntry.grid(row=0,column=1,padx=40,pady=20)

    usernameLabel = Label(connectWindow, text='User Name', font=('arial', 20, 'bold'))
    usernameLabel.grid(row=1, column=0, padx=20)

    userEntry=Entry(connectWindow,font=('roman',15,'bold'),bd=2)
    userEntry.grid(row=1,column=1,padx=40,pady=20)

    passwordLabel = Label(connectWindow, text='Password', font=('arial', 20, 'bold'))
    passwordLabel.grid(row=2, column=0, padx=20)

    passwordEntry = Entry(connectWindow, font=('roman', 15, 'bold'), bd=2)
    passwordEntry.grid(row=2, column=1, padx=40, pady=20)

    connectButton=ttk.Button(connectWindow,text='CONNECT',command=connect)
    connectButton.grid(row=3,columnspan=2)

count=0
text=''
def slider():
    global text,count
    if count==len(s):
        count=0
        text=''
    text=text+s[count]#S
    sliderLabel.config(text=text)
    count+=1
    sliderLabel.after(300,slider)
def clock():
    global date,currenttime
    date=time.strftime('%d/%m/%Y')
    currenttime=time.strftime('%H:%M:%S')
    datetimeLabel.config(text=f' Date:{date}\nTime: {currenttime}')
    datetimeLabel.after(1000,clock)

#GUI Part
root=ttkthemes.ThemedTk()
root.get_themes()
root.set_theme('breeze')
root.geometry('1174x680+0+0')
root.resizable(0,0)
root.title('Student Information System')

datetimeLabel=Label(root,font=('times new roman',18,'bold'))
datetimeLabel.place(x=5,y=5)
clock()
s='STUDENT INFORMATION SYSTEM'#s[count]=t when count is 1
sliderLabel=Label(root,text=s,font=('arial',28,'italic bold'),width=30)
sliderLabel.place(x=350,y=0)
slider()

connectButton=ttk.Button(root,text='Connect to database',command=connect_database)
connectButton.place(x=1000,y=10)

leftFrame=Frame(root)
leftFrame.place(x=50,y=80,width=300,height=600)

logo_image=PhotoImage(file='student.png')
logo_Label=Label(leftFrame,image=logo_image)
logo_Label.grid(row=0,column=0)

addstudentButton=ttk.Button(leftFrame,text='ADD STUDENT',width=25,state=DISABLED,command=lambda :toplevel_data('Add Student','ADD STUDENT',add_data))
addstudentButton.grid(row=1,column=0,pady=20)

searchstudentButton=ttk.Button(leftFrame,text='SEARCH STUDENT',width=25,state=DISABLED,command=lambda :toplevel_data('Search Student','SEARCH STUDENT',search_data))
searchstudentButton.grid(row=2,column=0,pady=20)

deletestudentButton=ttk.Button(leftFrame,text='DELETE STUDENT',width=25,state=DISABLED,command=delete_student)
deletestudentButton.grid(row=3,column=0,pady=20)

updatestudentButton=ttk.Button(leftFrame,text='UPDATE STUDENT',width=25,state=DISABLED,command=lambda :toplevel_data('Update Student','UPDATE STUDENT',update_data))
updatestudentButton.grid(row=4,column=0,pady=20)

showstudentButton=ttk.Button(leftFrame,text='SHOW STUDENT',width=25,state=DISABLED,command=show_student)
showstudentButton.grid(row=5,column=0,pady=20)

exportstudentButton=ttk.Button(leftFrame,text='EXPORT DATA',width=25,state=DISABLED,command=export_data)
exportstudentButton.grid(row=6,column=0,pady=20)

countByCityButton = ttk.Button(leftFrame, text='COUNT ADMISSIONS BY CITY', width=25, state=DISABLED, command=count_admissions_by_city)
countByCityButton.grid(row=7, column=0, pady=20)

countByStateButton = ttk.Button(leftFrame, text='COUNT ADMISSIONS BY STATE', width=25, state=DISABLED, command=count_admissions_by_state)
countByStateButton.grid(row=8, column=0, pady=20)

exitstudentButton=ttk.Button(leftFrame,text='EXIT',width=25,command=iexit)
exitstudentButton.grid(row=9,column=0,pady=20)

rightFrame=Frame(root)
rightFrame.place(x=250,y=80,width=820,height=600)

scrollBarX=Scrollbar(rightFrame,orient=HORIZONTAL)
scrollBarY=Scrollbar(rightFrame,orient=VERTICAL)

studentTable=ttk.Treeview(rightFrame,columns=('ID','NAME','MOBILE NO','EMAIL','ADDRESS','GENDER','D.O.B','ADDED DATE','ADDED TIME'),xscrollcommand=scrollBarX.set,yscrollcommand=scrollBarY.set)

scrollBarX.config(command=studentTable.xview)
scrollBarY.config(command=studentTable.yview)

scrollBarX.pack(side=BOTTOM,fill=X)
scrollBarY.pack(side=RIGHT,fill=Y)

studentTable.pack(fill=BOTH,expand=1)


studentTable.heading('ID',text='ID')
studentTable.heading('NAME',text='NAME')
studentTable.heading('MOBILE NO',text='MOBILE NO')
studentTable.heading('EMAIL',text='EMAIL')
studentTable.heading('ADDRESS',text='ADDRESS')
studentTable.heading('GENDER',text='GENDER')
studentTable.heading('D.O.B',text='D.O.B')
studentTable.heading('ADDED DATE',text='ADDED DATE')
studentTable.heading('ADDED TIME',text='ADDED TIME')

studentTable.column('ID',width=300,anchor=CENTER)
studentTable.column('NAME',width=300,anchor=CENTER)
studentTable.column('MOBILE NO',width=300,anchor=CENTER)
studentTable.column('EMAIL',width=300,anchor=CENTER)
studentTable.column('ADDRESS',width=300,anchor=CENTER)
studentTable.column('GENDER',width=150,anchor=CENTER)
studentTable.column('D.O.B',width=150,anchor=CENTER)
studentTable.column('ADDED DATE',width=300,anchor=CENTER)
studentTable.column('ADDED TIME',width=300,anchor=CENTER)

style=ttk.Style()

style.configure('Treeview',rowheight=40,font=('arial',15,'bold'),background='white',fieldbackground='white')
style.configure('Treeview.Heading',font=('arial',14,'bold'),foreground='royalblue')


studentTable.config(show='headings')


root.mainloop()
