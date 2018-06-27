"""
Created by adam on 6/26/18
"""
__author__ = 'adam'

from faker import Faker

fake = Faker()

from twitter.models import User, Status

def generate_data(field):
    final = field.split('_')[-1]

    numericVals = [ 'id', 'id_str' ]
    longText = [ 'description' ]
    d = None

    if field == 'email':
        d = fake.email()
    
    # numeric fields
    elif field in numericVals or final == 'count':
        d = fake.pyint()

    # likely date fields
    elif final == 'at':
        d = fake.date( pattern="%Y-%m-%d", end_datetime=None )

    # multiple sentences
    elif field in longText:
        d = fake.paragraph( nb_sentences=3, variable_nb_sentences=True, ext_word_list=None )

    # links
    elif final == 'url' or final == 'https':
        d = fake.url()

    # styling
    elif final == 'color':
        d = fake.hex_color()

    else:
        d = fake.word()

    return d


class UserSearchResultFactory( User ):
    """Creates the object we receive from a search
    for a user with fake data
    """
    def __init__( self ):
        super().__init__()
        for k in self.__dict__:
            d = generate_data(k)
            setattr( self, k, d )



class TweetSearchResultFactory( Status ):
    """Returns a result object from a Status searc, full of fake data"""
    def __init__( self ):
        super().__init__()
        for k in self.__dict__:
            d = generate_data(k)
            setattr( self, k, d )



if __name__ == '__main__':
    u = TweetSearchResultFactory()

    print( u.__dict__ )
