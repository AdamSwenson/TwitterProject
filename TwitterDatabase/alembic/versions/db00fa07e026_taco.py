"""taco

Revision ID: db00fa07e026
Revises: 
Create Date: 2018-08-10 17:44:52.755750

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'db00fa07e026'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('hashtags',
    sa.Column('tagID', sa.Integer(), nullable=False),
    sa.Column('hashtag', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('tagID')
    )
    op.create_table('users',
    sa.Column('userID', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('screen_name', sa.String(length=225), nullable=True),
    sa.Column('id_str', sa.String(length=225), nullable=True),
    sa.Column('name', sa.String(length=225), nullable=True),
    sa.Column('description', sa.String(length=250), nullable=True),
    sa.Column('lang', sa.String(length=100), nullable=True),
    sa.Column('utc_offset', sa.String(length=100), nullable=True),
    sa.Column('verified', sa.String(length=100), nullable=True),
    sa.Column('followers_count', sa.Integer(), nullable=True),
    sa.Column('friends_count', sa.Integer(), nullable=True),
    sa.Column('url', sa.String(length=100), nullable=True),
    sa.Column('time_zone', sa.String(length=100), nullable=True),
    sa.Column('created_at', sa.String(length=100), nullable=True),
    sa.Column('entities', sa.String(length=225), nullable=True),
    sa.Column('favourites_count', sa.Integer(), nullable=True),
    sa.Column('statuses_count', sa.Integer(), nullable=True),
    sa.Column('id', sa.String(length=225), nullable=True),
    sa.Column('location', sa.String(length=225), nullable=True),
    sa.Column('is_translation_enabled', sa.String(length=10), nullable=True),
    sa.Column('other_data', sa.JSON(), nullable=True),
    sa.PrimaryKeyConstraint('userID')
    )
    op.create_table('tweets',
    sa.Column('tweetID', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('userID', sa.Integer(), nullable=True),
    sa.Column('tweetText', sa.String(length=250), nullable=True),
    sa.Column('favorite_count', sa.Integer(), nullable=True),
    sa.Column('source', sa.String(length=250), nullable=False),
    sa.Column('retweeted', sa.String(length=10), nullable=True),
    sa.Column('retweet_count', sa.Integer(), nullable=True),
    sa.Column('in_reply_to_screen_name', sa.String(length=100), nullable=True),
    sa.Column('favorited', sa.String(length=10), nullable=True),
    sa.Column('lang', sa.String(length=100), nullable=True),
    sa.Column('created_at', sa.String(length=100), nullable=True),
    sa.Column('profile_background_tile', sa.String(length=100), nullable=True),
    sa.Column('is_translation_enabled', sa.String(length=100), nullable=True),
    sa.Column('profile_location', sa.String(length=100), nullable=True),
    sa.Column('other_data', sa.JSON(), nullable=True),
    # sa.ForeignKeyConstraint(['userID'], ['users.userID'], ),
    sa.PrimaryKeyConstraint('tweetID')
    )
    op.create_table('tweetsXtags',
    sa.Column('tweetID', sa.Integer(), nullable=True),
    sa.Column('tagID', sa.Integer(), nullable=True),
    # sa.ForeignKeyConstraint(['tagID'], ['hashtags.tagID'], ),
    # sa.ForeignKeyConstraint(['tweetID'], ['tweets.tweetID'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # pass
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tweetsXtags')
    op.drop_table('tweets')
    op.drop_table('users')
    op.drop_table('hashtags')
    ### end Alembic commands ###
