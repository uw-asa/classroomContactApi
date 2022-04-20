#! python3
import sqlite3
import pyodbc
import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_dbs():
    if 'db_local' not in g:
        g.db_local = sqlite3.connect(
            current_app.config['SQLITE_DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        def make_dicts(cursor, row):
            return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))
        g.db_local.row_factory = make_dicts

    if 'db_edw' not in g:
        g.db_edw = pyodbc.connect('Driver={SQL Server};'
							'Server=edwpub.s.uw.edu;'
							'Database=EDWPresentation;'
							'TrustedConnection=True;'
							)

    return {'local': g.db_local, 'edw': g.db_edw}


def close_dbs(e=None):
    db_local = g.pop('db_local', None)
    db_edw = g.pop('db_edw', None)

    if db_local is not None:
        db_local.close()
    if db_edw is not None:
        db_edw.close()


def init_local_db():
    dbs = get_dbs()

    with current_app.open_resource('schema.sql') as f:
        dbs['local'].executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    '''Clear the existing data and create new tables.'''
    init_local_db()
    click.echo('Initialized the local database.')

def query_local(query, args=(), one=False):
    cursor = get_dbs()['local'].execute(query, args)
    rv = cursor.fetchall()
    cursor.close()
    return (rv[0] if rv else None) if one else rv

def update_local(query, args={}):
    con = get_dbs()['local']
    con.execute(query, args)
    con.commit()

def query_edw(query, args=(), one=False):
    cursor = get_dbs()['edw'].cursor()
    cursor.execute(query, args)
    rv = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    results = []
    for row in rv:
        results.append(dict(zip(columns, row)))
    cursor.close()
    return (results[0] if results else None) if one else results

def init_app(app):
    # Hook app lifecycle events
    app.teardown_appcontext(close_dbs)
    app.cli.add_command(init_db_command)
