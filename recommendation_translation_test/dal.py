import psycopg2
from psycopg2 import sql

_connection = None


def _get_connection():
    global _connection
    if _connection is None or _connection.closed != 0:
        _connection = psycopg2.connect(dbname='test', user='testing', password='testing', host='localhost')
    return _connection


def get_items(target):
    target_name = sql.Identifier('{}wiki'.format(target))
    query = 'select id, {0} as prediction from predictions where {0} is not null order by {0} desc;'

    with _get_connection().cursor() as cursor:
        try:
            cursor.execute(sql.SQL(query).format(target_name))
            results = cursor.fetchall()
        except psycopg2.Error:
            return []

    return [{'id': result[0], 'prediction': result[1]} for result in results]
