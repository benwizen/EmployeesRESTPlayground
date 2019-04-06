import csv
import sqlite_api


def csv_to_db():
    with open(r'C:\Users\User\PycharmProjects\REST_emp\emps_info2.csv', 'r') as csv_info:
        csv_file = csv.reader(csv_info)
        next(csv_file)
        for row in csv_file:
            sqlite_api.insert("employees",
                              id=row[0],
                              employee_name=row[1],
                              employee_age=row[2],
                              employee_salary=row[3])


if __name__ == "__main__":
    csv_to_db()
