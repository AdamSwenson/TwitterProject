import unittest
from faker import Faker

fake = Faker()

import sqlalchemy

from Models.WordORM import create_db_tables
from DatabaseAccessObjects.EngineMakers import create_sqlite_engine, _create_sqlite_file_engine


class SqliteMemoryTests( unittest.TestCase ):
    def test_that_tables_are_created( self ):
        text = fake.word()
        ENGINE = 'sqlite'
        engine = create_sqlite_engine()
        create_db_tables( engine )

        self.assertIsInstance( engine, sqlalchemy.engine.base.Engine, 'created engine' )

        engine.execute( "insert into words (word) values('%s')" % text )

        result = engine.execute( "select word from words where word = '%s'" % text )
        for r in result:
            self.assertEqual( r[ 'word' ], text )


class SqliteFileTests( unittest.TestCase ):
    def test_that_tables_are_created( self ):
        text = fake.word()
        ENGINE = 'sqlite-file'
        SQLITE_FILE_CONNECTION_STRING = 'sqlite:///test.db'

        engine = _create_sqlite_file_engine( SQLITE_FILE_CONNECTION_STRING )
        create_db_tables( engine )

        self.assertIsInstance( engine, sqlalchemy.engine.base.Engine, 'created engine' )

        engine.execute( "insert into words (word) values('%s')" % text )

        result = engine.execute( "select word from words where word = '%s'" % text )
        for r in result:
            self.assertEqual( r[ 'word' ], text )


if __name__ == '__main__':
    unittest.main()
