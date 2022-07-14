from tabulate import tabulate
import mysql.connector as mysql
conn=mysql.connect(host='localhost', user='root', password='nazeef')
cs=conn.cursor()
cs.execute("create database if not exists horsepower")
cs.execute("use horsepower")
cs.execute('create table if not exists Member_Info(id int(10) primary key not null ,name varchar(30),age int,gender varchar(6),mobile int,Activities varchar(40))')
cs.execute('create table if not exists Member_package_info(id int(10),name varchar(30),Activities varchar(40),special_package varchar(40),total_payment int,monthly_payment int,end_of_membership date,constraint foreign key(id) references Member_Info(id))')
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
              cs.execute("insert into member_info values(%s,'%s',%s,'%s',%s,'%s')"%(i,n,a,g,m,act))
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
        1.Create account.
        2.Login.
        3.Exit.'''.format(bgc.BOLD))
        ch = int(input('Enter choice 1/2/3:'))
        if ch == 1:
            print('Username should be atleast 6 characters long.')
            username = input('Enter username: ')
            if len(username) < 6:
                print('Username should be atleast 6 characters long.')
                continue
            password = input('Enter password: ')
            mobile= input('Enter mobile no.: ')
            if len(password) < 6:
                print('Password should be atleast 6 characters long.')
                continue
            print('Account created successfully.')
        elif ch==2:
            username = input('Enter username: ')
            password = input('Enter password: ')
            if username == 'admin' and password == '123456':
                print('Welcome Admin.')
                break
            else:
                print('Invalid username or password.')
                continue
else:
    pass