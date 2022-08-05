from tabulate import tabulate
import datetime
import mysql.connector as mysql


def findByName(n):
    cs.execute("Select * from member_info where Member_Name='%s'" % n)
    t = cs.fetchall()
    nt = []
    for i in t:
        nt.append(i[:6])
    print(tabulate(nt, headers=['ID', 'Name', 'Age', 'Gender', 'Mobile', 'Activities']))


conn = mysql.connect(host='localhost', user='root', password='00b')
cs = conn.cursor()
cs.execute("create database if not exists horsepower")
cs.execute("use horsepower")
cs.execute(
    'create table if not exists Member_Info(id int(10) primary key not null auto_increment,Member_Name varchar(30),age int,'
    'gender char(1),mobile int,Activities varchar(40),password varchar(20))')
cs.execute(
    "create table if not exists Member_package_info(packageId int primary key auto_increment, id int(10),special_package varchar(40),total_payment int," +
    "monthly_payment int,end_of_membership date,constraint foreign key(id) references Member_Info(id) on delete " +
    "cascade)")
cs.execute("create table if not exists progress_tracker(id int, date date,weight int,height decimal(5,2), " +
           'constraint foreign key(id) references Member_Info(id) on delete cascade)')


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


print("WELCOME TO HORSEPOWER HEALTH CLUB" + bgc.BOLD + bgc.UNDERLINE)
login = input('Are you a Member or an Admin?: ')
if login == 'admin':
    password = input('Enter your password: ' + bgc.ENDC)
    if password == '123456':
        while True:
            print(bgc.BOLD + '''MENU:
            1.Add new member.
            2.Show all members.
            3.Add member package.
            4.Show all members packages.
            5.Find member.
            6.Update member package.
            7.Remove member.
            8.EXIT.''')
            ch = int(input('Enter choice 1/2/3/4/5/6/7/8:'))
            if ch == 1:
                a = input("Enter Member name: ")
                b = int(input("Enter Member age: "))
                c = input("Enter Member gender (m/f): ")
                d = int(input("Enter Member mobile number: "))
                e = input("Enter Member activities: ")
                f = input("Enter Member password: ")

                cs.execute(
                    "insert into Member_Info(Member_Name, age, gender, mobile, Activities, password) VALUES('%s',%s,'%s',%s,'%s','%s')" % (
                    a, b, c, d, e, f))
                conn.commit()
                print(bgc.OKGREEN + 'Details Inserted' + bgc.ENDC)

            elif ch == 2:
                cs.execute("Select * from Member_Info")
                t = cs.fetchall()
                nt = []
                for i in t:
                    nt.append(i[:6])
                print(tabulate(nt, headers=['ID', 'Name', 'Age', 'Gender', 'Mobile', 'Activities']))

            elif ch == 3:
                id = int(input("Enter member id: "))
                sp = input('Enter special package:')
                t = int(input('Enter total payment:'))
                mp = int(input('Enter monthly payment:'))
                e = input('Enter end of membership:')
                cs.execute(
                    "insert into member_package_info(id, special_package,total_payment,monthly_payment,end_of_membership) values(%s, '%s',%s,%s,'%s')" % (
                        id, sp, t, mp, e))
                conn.commit()
                print(bgc.OKGREEN + 'Details Inserted' + bgc.ENDC)

            elif ch == 4:
                cs.execute("Select * from member_package_info")
                t = cs.fetchall()
                nt = []
                for i in t:
                    nt.append(i)
                print(tabulate(nt, headers=['Package ID', 'ID', 'Special Package', 'Total Payment', 'Monthly Payment',
                                            'End of Membership']))

            elif ch == 5:
                n = input('Enter name to find:')
                findByName(n)

            elif ch == 6:
                n = input('Enter name to change:')
                findByName(n)

                id = int(input("Enter member ID"))
                cs.execute("select * from member_package_info where id='%s'" % id)
                fet = cs.fetchall()
                if (len(fet) != 0):
                    print(
                        tabulate(fet,
                                 headers=['package_id', 'id', 'special_package', 'total_payment', 'monthly_payment',
                                          'end_of_membership'],
                                 tablefmt='fancy_grid'))
                    packId = int(input('Enter package id to update:'))
                    sp = input('Enter special package:')
                    t = int(input('Enter total payment:'))
                    mp = int(input('Enter monthly payment:'))
                    e = input('Enter end of membership:')
                    cs.execute(
                        "update member_package_info set special_package='%s',total_payment=%s,"
                        "monthly_payment=%s,end_of_membership='%s' where packageId=%s" % (
                            sp, t, mp, e, packId))
                    conn.commit()

                    print(bgc.OKGREEN + 'Details Updated')
                else:
                    print("Members package details are empty")

            elif ch == 7:
                n = input('Enter id to remove')
                cs.execute("delete from member_info where id = %s" % n)
                conn.commit()
                print('Details Deleted' + bgc.OKGREEN)

            elif ch == 8:
                break

    else:
        print(bgc.FAIL + 'Wrong Password' + bgc.ENDC)

elif login == 'member':
    while True:
        print('''MENU:
        1.Login.
        2.Exit.'''.format(bgc.BOLD))
        a = int(input('Enter choice 1/2'))
        if a == 1:
            mobile = input("Enter your mobile: ")
            password = input("Enter your password: ")
            cs.execute(
                "SELECT id, mobile, password from member_info WHERE mobile = %s AND password = '%s'" % (
                    mobile, password))
            t = cs.fetchall()
            if len(t) > 0:
                print("Login successful")
                userId = t[0][0]
                while True:
                    print('''What would you like to do?
                                                1.Insert details in your progress tracker.
                                                2.View your progress tracker.
                                                3.View your package details.
                                                4.Log Out.'''.format(bgc.BOLD))
                    ch = int(input('Enter choice 1/2/3/4:'))
                    if ch == 1:
                        date = input('Enter date: ')
                        weight = int(input('Enter weight: '))
                        height = float(input('Enter height (metre): '))
                        cs.execute(
                            "insert into progress_tracker value (%s,'%s',%s,%s)" % (userId, date, weight, height))
                        conn.commit()
                        print(bgc.OKGREEN + 'Details Inserted')

                    elif ch == 2:
                        cs.execute(
                            'select id, date, weight, height, weight/(height*height) as bmi from progress_tracker')
                        print(tabulate(cs.fetchall(),
                                       headers=['userId', 'date', 'weight', 'height', 'bmi'],
                                       tablefmt='fancy_grid'))

                    elif ch == 3:
                        cs.execute(
                            "select * from member_package_info where id = %s" % userId)
                        print(tabulate(cs.fetchall(),
                                       headers=['package_id', 'id', 'special_package', 'total_payment', 'monthly_payment',
                                                'end_of_membership'],
                                       tablefmt='fancy_grid'))

                    elif ch == 4:
                        break

                    else:
                        print('Invalid choice')
                        continue

            else:
                print("Login Failed")
                continue
        elif a == 2:
            break
else:
    pass
