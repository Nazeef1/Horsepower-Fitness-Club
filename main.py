from tabulate import tabulate
import datetime
import mysql.connector as mysql
conn=mysql.connect(host='localhost', user='root', password='nazeef')
cs=conn.cursor()
cs.execute("create database if not exists horsepower")
cs.execute("use horsepower")
cs.execute('create table if not exists Member_Info(id int(10) primary key not null,Member_Name varchar(30),age int,gender varchar(6),mobile int,Activities varchar(40),password varchar(20) invisible)')
cs.execute("create table if not exists Member_package_info(id int(10),Member_Name varchar(30),Activities varchar(40),special_package varchar(40),total_payment int,monthly_payment int,end_of_membership date,constraint foreign key(id,Member_Name,Activities) references Member_Info(id,Member_Name,Activities))")
class bgc:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    WHITE = '\033[37m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    BLACK = '\033[30m'
print("WELCOME TO HORSEPOWER HEALTH CLUB"+bgc.BOLD+bgc.UNDERLINE)
login=input('Are you a Member or an Admin?: ')
if login == 'admin':
    password=input('Enter your password: '+bgc.ENDC)
    if password=='123456':
        while True:
           print(bgc.BOLD+'''MENU:
            1.Add new member.
            2.Show all members.
            3.Show all members packages.
            4.Find member.
            5.Update member package.
            6.Remove member.
            .EXIT.''')
           ch=int(input('Enter choice 1/2/3/4/5/6/7:'))
           if ch==1:
              i=int(input('Enter id no.:'))
              n=input('Enter Name:')
              a=int(input('Enter Age:'))
              g=input('Enter Gender:')
              m=int(input('Enter mobile no.:'))
              act=input('Enter Activities:')
              pw=input('Enter password:')
              cs.execute("insert into member_info values(%s,'%s',%s,'%s',%s,'%s','%s')"%(i,n,a,g,m,act,pw))
              conn.commit()
              print(bgc.OKGREEN + 'Details Inserted')
              sp=input('Enter special package:')
              t=int(input('Enter total payment:'))
              mp=int(input('Enter monthly payment:'))
              e=input('Enter end of membership:')
              cs.execute("insert into member_package_info values(%s,'%s','%s','%s',%s,%s,%s)"%(i,n,act,sp,t,mp,e))
              conn.commit()
           elif ch==2:
                cs.execute('select * from member_info')
                print(tabulate(cs.fetchall(), headers=['id','name','age','gender','mobile','Activities'], tablefmt='fancy_grid'))
           elif ch==3:
                cs.execute('select * from member_package_info')
                print(tabulate(cs.fetchall(), headers=['id','name','Activities','special_package','total_payment','monthly_payment','end_of_membership'], tablefmt='fancy_grid'))
           elif ch==4:
                n=input('Enter name to find:')
                cs.execute("select * from member_info where name='%s'"%n)
                print(tabulate(cs.fetchall(), headers=['id','name','age','gender','mobile','Activities'], tablefmt='fancy_grid'))
           elif ch==5:
                n=input('Enter name to change:')
                cs.execute('select * from member_package_info where name="%s"'%n)
                print(tabulate(cs.fetchall(), headers=['id','name','Activities','special_package','total_payment','monthly_payment','end_of_membership'], tablefmt='fancy_grid'))
                act=input('Enter new activities:')
                sp=input('Enter special package:')
                t=int(input('Enter total payment:'))
                mp=int(input('Enter monthly payment:'))
                e=input('Enter end of membership:')
                cs.execute("update member_package_info set Activities='%s',special_package='%s',total_payment=%s,monthly_payment=%s,end_of_membership='%s' where name='%s'"%(act,sp,t,mp,e,n))
                conn.commit()
                print(bgc.OKGREEN + 'Details Updated')
           elif ch==6:
                n=input('Enter name to delete:')
                cs.execute("delete from member_info where name='%s'"%n)
                conn.commit()
                print('Details Deleted' + bgc.OKGREEN)
           else:
                conn.close()
                break
elif login == 'member':
    while True:
        print('''MENU:
        1.Login.
        2.Exit.'''.format(bgc.BOLD))
        ch = int(input('Enter choice 1/2/3:'))
        if ch == 1:
            mobile = input('Enter mobile no.: ')
            password = input('Enter password: ')
            if mobile and password in cs.execute("select * from member_info where mobile=%s and password='%s'"%(mobile,password)):
                print('Welcome' + cs.execute("select member_name from member_info where mobile=%s and password='%s'"%(mobile,password)).fetchone()[1])
                break
            else:
                print('Invalid mobile number or password.')
                continue
            print('''What would you like to do?
            1.Insert details in your progress tracker.
            2.View your progress tracker.
            3.View your package details.
            4.EXIT.'''.format(bgc.BOLD))
            ch = int(input('Enter choice 1/2/3/4:'))
            if ch == 1:
                cs.execute('create table if not exists progress_tracker(date text,weight int,height int,weight*height**2 as bmi int, workouts varchar(20),weight_loss int,weight_gain int)')
                date = input('Enter date: ')
                weight = int(input('Enter weight: '))
                height = int(input('Enter height: '))
                workouts = input('Enter workouts: ')
                weight_loss = int(input('Enter weight loss: '))
                weight_gain = int(input('Enter weight gain: '))
                bmi = weight * height ** 2
                cs.execute("insert into progress_tracker values('%s',%s,%s,%s,'%s',%s,%s)"%(date,weight,height,bmi,workouts,weight_loss,weight_gain))
                conn.commit()
                print(bgc.OKGREEN + 'Details Inserted')
            elif ch == 2:
                cs.execute('select * from progress_tracker')
                print(tabulate(cs.fetchall(), headers=['date','weight','height','bmi','workouts','weight_loss','weight_gain'], tablefmt='fancy_grid'))
            elif ch == 3:
                cs.execute('select * from member_package_info where name="%s"'%cs.execute("select member_name from member_info where mobile=%s and password='%s'"%(mobile,password)).fetchone()[1])
                print(tabulate(cs.fetchall(), headers=['id','name','Activities','special_package','total_payment','monthly_payment','end_of_membership'], tablefmt='fancy_grid'))
                today = datetime.datetime.now()
                end_date = datetime.datetime(int(cs.execute("select end_of_membership from member_package_info where name='%s'"%cs.execute("select member_name from member_info where mobile=%s and password='%s'"%(mobile,password)).fetchone()[1]).fetchone()[0][0:4]),int(cs.execute("select end_of_membership from member_package_info where name='%s'"%cs.execute("select member_name from member_info where mobile=%s and password='%s'"%(mobile,password)).fetchone()[1]).fetchone()[0][5:7]),int(cs.execute("select end_of_membership from member_package_info where name='%s'"%cs.execute("select member_name from member_info where mobile=%s and password='%s'"%(mobile,password)).fetchone()[1]).fetchone()[0][8:10]))
                difference = end_date.date() - today.date()
                print(difference.days, 'days remaining for your membership.')
                if difference.days <7:
                    print('Your membership is about to expire.'
                          'Please renew your membership at the fitness club counter.')
                elif difference.days <= 0:
                    print('Your membership has expired.')
            else:
                conn.close()
                break
else:
    pass