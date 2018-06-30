"""initial database structure

Revision ID: 3de348837e56
Revises: 
Create Date: 2018-06-30 13:16:53.658459

"""
from alembic import op
from sqlalchemy import Column, ForeignKey, Integer, String, JSON

# revision identifiers, used by Alembic.
revision = '3de348837e56'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    pass
    # op.create_table( 'tweets',
    #                  Column( 'tweetID', Integer, primary_key=True, autoincrement=False ),
    #                  Column( 'userID', Integer, ForeignKey( 'users.userID' ) ),
    #                  Column( 'tweetText', String( 250 ) ),
    #                  Column( 'favorite_count', Integer ),
    #                  Column( 'source', String( 250 ), nullable=False ),
    #                  Column( 'retweeted', String( 10 ) ),
    #                  Column( 'retweet_count', Integer ),
    #                  Column( 'in_reply_to_screen_name', String( 100 ) ),
    #                  Column( 'favorited', String( 10 ) ),
    #                  Column( 'lang', String( 100 ) ),
    #                  Column( 'created_at', String( 100 ) ),
    #                  Column( 'profile_background_tile', String( 100 ) ),
    #                  Column( 'is_translation_enabled', String( 100 ) ),
    #                  Column( 'profile_location', String( 100 ) ),
    #                  Column( 'other_data', JSON() )
    #                  )
    #
    # op.create_table( 'users',
    #                  Column( 'userID', Integer, primary_key=True, autoincrement=False ),
    #                  Column( 'id', String( 225 ) ),
    #                  Column( 'screen_name', String( 225 ) ),
    #                  Column( 'id_str', String( 225 ) ),
    #                  Column( 'name', String( 225 ) ),
    #                  Column( 'description', String( 250 ) ),
    #                  Column( 'lang', String( 100 ) ),
    #                  Column( 'utc_offset', String( 100 ) ),
    #                  Column( 'verified', String( 100 ) ),
    #                  Column( 'followers_count', Integer ),
    #                  Column( 'friends_count', Integer ),
    #                  Column( 'url', String( 100 ) ),
    #                  Column( 'time_zone', String( 100 ) ),
    #                  Column( 'created_at', String( 100 ) ),
    #                  Column( 'entities', String( 225 ) ),
    #                  Column( 'favourites_count', Integer ),
    #                  Column( 'statuses_count', Integer ),
    #                  Column( 'location', String( 225 ) ),
    #                  Column( 'is_translation_enabled', String( 10 ) ),
    #                  Column( 'other_data', JSON() )
    #                  )
    #
    # op.create_table( 'hashtags',
    #                  Column( 'tagID', Integer, primary_key=True ),
    #                  Column( 'hashtag', String( 100 ), nullable=False )
    #                  )
    #
    # op.create_table( 'tweetsXtags',
    #                  Column( 'tweetID', Integer, ForeignKey( 'tweets.tweetID' ) ),
    #                  Column( 'tagID', Integer, ForeignKey( 'hashtags.tagID' ) )
    #                  )
    #

def downgrade():
    pass
