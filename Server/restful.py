from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import sqlite_api

app = Flask(__name__)
api = Api(app)


class AllTables(Resource):
    @staticmethod
    def get():
        return [tab[0] for tab in sqlite_api.all_tables()]

    @staticmethod
    def post():
        parser = reqparse.RequestParser()
        parser.add_argument('table_name')
        parser.add_argument('columns')
        args = parser.parse_args()
        sqlite_api.create_table(args['table_name'], args['columns'].split(','))


class AllRows(Resource):
    @staticmethod
    def get(table_name):
        return sqlite_api.query(table_name)


class EmpQuery(Resource):
    @staticmethod
    def get():
        args = request.args
        return sqlite_api.query("employees", **args)

    @staticmethod
    def post():
        parser = reqparse.RequestParser()
        parser.add_argument('id')
        parser.add_argument('employee_name')
        parser.add_argument('employee_salary')
        parser.add_argument('employee_age')
        args = parser.parse_args()
        return sqlite_api.insert("employees", **args)

    @staticmethod
    def delete():
        parser = reqparse.RequestParser()
        parser.add_argument('id')
        parser.add_argument('employee_name')
        parser.add_argument('employee_salary')
        parser.add_argument('employee_age')
        args = parser.parse_args()
        return sqlite_api.delete("employees", **args)

    @staticmethod
    def put():
        import json
        parser = reqparse.RequestParser()
        parser.add_argument('changes')
        parser.add_argument('who')
        args = parser.parse_args()
        d = dict(args)
        changes = json.loads(d['changes'].replace('\'', '\"'))
        who = json.loads(d['who'].replace('\'', '\"'))
        return sqlite_api.update("employees", changes=changes, who=who)


class TabCols(Resource):
    @staticmethod
    def get(table_name):
        return sqlite_api.table_columns(table_name)


api.add_resource(AllRows, '/<table_name>')
api.add_resource(TabCols, '/<table_name>/cols')
api.add_resource(EmpQuery, '/employees')
api.add_resource(AllTables, '/')

if __name__ == '__main__':
    app.run(debug=True)
