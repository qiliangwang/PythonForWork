import MySQLdb
from flask import Flask
import flask_restful as restful

app = Flask(__name__)
api = restful.Api(app)

info_data = {
    'localhost_props': {
        'host': '127.0.0.1',
        'user': 'root',
        'passwd': 'password',
        'port': 3306,
    },
    'remote1_props': {
        'host': '192.168.33.206',
        'user': 'dev',
        'passwd': 'lvyue@123456',
        'port': 3361,
    },
    'remote2_props': {
        'host': '192.168.33.206',
        'user': 'dev',
        'passwd': 'lvyue@123456',
        'port': 3362,
    },
    'remote3_props': {
        'host': '192.168.33.206',
        'user': 'dev',
        'passwd': 'lvyue@123456',
        'port': 3363,
    },
    'remote4_props': {
        'host': '192.168.33.206',
        'user': 'dev',
        'passwd': 'lvyue@123456',
        'port': 3364,
    },
    'remote5_props': {
        'host': '192.168.33.206',
        'user': 'dev',
        'passwd': 'lvyue@123456',
        'port': 3365,
    },
    'remote6_props': {
        'host': '192.168.33.206',
        'user': 'dev',
        'passwd': 'lvyue@123456',
        'port': 3366,
    },
}
data_query = 'remote6_props'
json_data = {}


class ColumnData(restful.Resource):
    def get(self):
        return {'error': 0,
                'data': json_data,
                }


api.add_resource(ColumnData, '/')


def get_connection(db_name, port_info=data_query):
    conn_props = info_data[port_info]
    conn_props['db'] = db_name
    conn = MySQLdb.connect(**conn_props)
    return conn
    pass


def get_dbs():
    conn = MySQLdb.connect(**info_data[data_query])
    cursor = conn.cursor()
    cursor.execute('SHOW DATABASES;')
    dbs = [db_name[0] for db_name in cursor.fetchall()]
    for db in dbs:
        json_data[db] = {}
    cursor.close()
    return dbs


def get_tables(db_name, port_info=data_query):
    conn_props = info_data[port_info]
    conn_props['db'] = db_name
    conn = MySQLdb.connect(**conn_props)
    cursor = conn.cursor()
    cursor.execute('SHOW TABLES;')
    tables = [table[0] for table in cursor.fetchall()]
    for table in tables:
        sql_statement = "SHOW columns FROM " + str(table)
        cursor.execute(sql_statement)
        json_data[db_name][table] = [column[0] for column in cursor.fetchall()]
        print('DateBase: ', db_name, "|| TableName: ", table, "|| ColumnInfo: ", [column[0] for column in cursor.fetchall()])
    cursor.close()


def load_data():
    dbs = get_dbs()
    # dbs = ['sell']
    for db in dbs:
        get_tables(db)


if __name__ == '__main__':
    load_data()
    app.run(debug=True)
