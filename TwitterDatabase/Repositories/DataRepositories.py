"""
Created by adam on 11/6/16
"""
from Repositories.Interfaces import IRepository, ISessionHaver

__author__ = 'adam'

from Models.DataStructures import *
from DatabaseAccessObjects.Errors import DataError
from Models.WordORM import *


class WordRepository( IRepository, ISessionHaver ):
    """Allows asynchronously updating the database with the items.
    todo If going to eventually use in multithreaded actions, there could be race conditions w/r/t creating and retrieving words
    """

    def __init__( self, session=None ):
        if session is not None:
            self.session = session
        else:
            super().__init__()

    def get_word( self, result ):
        """
        Look up whether word exists already
        If not, create a new entry and return the object
        Should not save yet so that the map can be flushed too
        """
        text = result.text if is_result( result ) else result
        # print("get_word: %s" % text)
        # Get if already exists
        word = self.session.query( Word ).filter( Word.word == text ).first()

        # Create a new word if doesn't yet exist
        if not isinstance( word, Word ):
            word = Word()
            word.word = text

        return word

    def get_map( self, result, word ):
        """
        Creates a mapping object from the result. Tries loading a preexisting
        mapping first, if one exists, it returns the object
        """
        self._is_valid( result )
        assert (type( word ) is Word)
        # try loading in case already recorded
        # wordMap = self.session.word_map_table_creation_query(WordMapping).filter(
        #     WordMapping.tweet_id == result.tweet_id and
        #     WordMapping.sentence_index == result.sentence_index and
        #     WordMapping.word_index == result.word_index
        # ).first()
        #
        # if not isinstance(wordMap, WordMapping):
        wordMap = WordMapping()
        wordMap.sentence_index = result.sentence_index
        wordMap.word_index = result.word_index
        wordMap.word = word
        if result.type == 'tweet' and result.id is not None:
            wordMap.tweet_id = result.id
        if result.type == 'user' and result.id is not None:
            wordMap.user_id = result.id

        return wordMap

    def save( self, resultOrResults ):
        """
        For each word contained in the list, this retreives
        the object if it already exists or creates a new word object.
         It then writes the word and mapping to the db.
          Finally, it fires various notifications
        """

        # make a list if only one passed in
        resultOrResults = [ resultOrResults ] if not isinstance( resultOrResults, list ) else resultOrResults

        for result in resultOrResults:
            try:
                # self._is_valid(result)

                # get a Word object for the result
                word = self.get_word( result )
                # create a mapping object and attach word
                wordMap = self.get_map( result, word )
                # print( "save: %s" % wordMap.sentence_index )

                if self.write_to_db( word, wordMap ) is True:
                    # fire a save complete event
                    self._fire_save_notification( wordMap )
                else:
                    self._fire_error_saving_notification( wordMap )
            except DataError:
                self._fire_error_saving_notification( wordMap )
                print( 'uh oh' )

    def write_to_db( self, *args ):
        """Takes a list of objects and flushes them to the database"""
        try:
            toSave = [ a for a in args ]
            # save them
            self.session.add_all( toSave )
            self.session.commit()
            self._fire_save_notification()
            return True
        except Exception as e:
            print( "Error : %s" % e )
            self._fire_error_saving_notification( e )
            return False


class MapRepository( IRepository, ISessionHaver ):
    """Allows asynchronously updating the database with the items.
    """

    def __init__( self, session=None ):
        self.queue_count = 0
        if session is not None:
            self.session = session
        else:
            super().__init__()

    def save( self, result ):
        """
        Creates a mapping object from the result.
        """
        # try:
        # self._is_valid(result)
        wordMap = WordMappingDeux()
        wordMap.word = result.text if is_result( result ) else result
        wordMap.sentence_index = result.sentence_index
        wordMap.word_index = result.word_index
        if result.type == 'tweet' and result.id is not None:
            wordMap.tweet_id = result.id
        if result.type == 'user' and result.id is not None:
            wordMap.user_id = result.id
        # stage for saving
        self.session.add( wordMap )
        # self.handle_flush()
