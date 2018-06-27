"""
Created by adam on 6/25/18
"""
import environment
from DatabaseAccessObjects.Errors import DataError
from Models.DataStructures import is_result

__author__ = 'adam'

if __name__ == '__main__':
    pass


class IRepository( object ):
    def save( self, listOfResults ):
        raise NotImplementedError

    def _fire_save_notification( self, item=None ):
        pass

    # print( "TODO: Replace this with a successful save event firing" )

    def _fire_error_saving_notification( self, item=None ):
        pass
        # print( "TODO Replace this with an error saving event firing" )

    def _is_valid( self, result ):
        if is_result( result ):
            return True
        else:
            raise DataError


class ISessionHaver( object ):
    """Common class for objects which have access to the sqalchemy session.
    Loads and initalizes on object construction. """

    def __init__( self ):
        self.session = None
        self.session_factory = None
        # self.start_session()

    # def start_session( self ):
    #     """Loads the sqlalchemy Session object in as self.session"""
    #
    #     try:
    #         if type( Session ) is not None:
    #             self.session = session
    #     except:
    #         pass
    #         # create_global_session()

    def handle_flush( self ):
        # increment the queue count
        self.queue_count += 1
        if self.queue_count > environment.DB_QUEUE_SIZE:
            self.session.commit()
            # reset the queue
            self.queue_count = 0

    def rollback_transaction( self ):
        """
        Rolls back the Session's transaction when there's been a problem.
        """
        self.session.rollback()