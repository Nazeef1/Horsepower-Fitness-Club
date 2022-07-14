from tabulate import tabulate
import mysql.connector as mysql
conn=mysql.connect(host='localhost',user='root',password='nazeef')
cs=conn.cursor()
cs.execute("create database if not exists horsepower")
cs.execute("use horsepower")
cs.execute('create table if not exists Member_Info(id int(10) primary key not null auto_increment,name varchar(30),age int,mobile int,Activities varchar(40),Monthly_Fee int)')
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
print(bgc.BOLD+bgc.UNDERLINE+"WELCOME TO HORSEPOWER HEALTH CLUB")
login=input('Are you a Member or an Admin?: ')
if login == 'admin':
    password=input('Enter your password: ')
    if password=='123456':
        while True:
           print(bgc.BOLD+ bgc.WHITE+'''MENU:
            1.Add new member.
            2.Show all members.
            3.Find member.
            4.Change member package.
            5.Delete member.
            6.EXIT.''')
           ch=int(input('Enter choice 1/2/3/4/5/6/7:'))
           if ch==1:
              i=int(input('Enter id no.:'))
              n=input('Enter Name:')
              a=int(input('Enter Age:'))
              m=int(input('Enter mobile no.:'))
              act=input('Enter Activities:')
              fee=int(input('Enter Monthly Fee:'))
              cs.execute("insert into member_info values(%s,'%s',%s,%s,'%s',%s)"%(i,n,a,m,act,fee))
              conn.commit()
              print(bgc.OKGREEN + 'Details Inserted')
           elif ch==2:
                cs.execute('select * from member_info')
                print(tabulate(cs.fetchall(), headers=['id','name','age','mobile','Activities','Monthly Fee'], tablefmt='fancy_grid'))
           elif ch==3:
                n=input('Enter name to find:')
                cs.execute("select * from member_info where name='%s'"%n)
                print(tabulate(cs.fetchall(), headers=['id','name','age','mobile','Activities','Monthly Fee'], tablefmt='fancy_grid'))
           elif ch==4:
                n=input('Enter name to change:')
                cs.execute("select * from member_info where name='%s'"%n)
                print(tabulate(cs.fetchall(), headers=['id','name','age','mobile','Activities','Monthly Fee'], tablefmt='fancy_grid'))
                act=input('Enter new Activities:')
                fee=int(input('Enter new Monthly Fee:'))
                cs.execute("update member_info set Activities='%s',Monthly_Fee=%s where name='%s'"%(act,fee,n))
                conn.commit()
                print('Details Updated' + bgc.OKGREEN)
           elif ch==5:
                n=input('Enter name to delete:')
                cs.execute("delete from member_info where name='%s'"%n)
                conn.commit()
                print('Details Deleted' + bgc.OKGREEN)
           else:
                conn.close()
                break
else:
    pass