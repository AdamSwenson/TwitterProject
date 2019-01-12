"""
Created by adam on 6/30/18
"""
__author__ = 'adam'

import environment as env
from TwitterDatabase.DatabaseAccessObjects.DataConnections import MySqlConnection
from TwitterDatabase.Models.TweetORM import create_db_tables

if __name__ == '__main__':
    credential_file = env.CREDENTIAL_FILE
    # credential_file = '%s/private_credentials/sql_miner_laptop_credentials.xml' % env.BASE

    conn = MySqlConnection( credential_file )
    print( 'connected to %s' % conn._dsn )

    create_db_tables( conn.engine )
