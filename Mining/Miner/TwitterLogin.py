import twitter

from CommonTools.Credentialing.CredentialTools import CredentialLoader


def login( credentials_file ):
    """
    Reads the credentials file for the necessary credentials, creates a twitter.Twitter connection and returns it

    Normally, we will use the TwitterConnection object. But we are leaving this
    separate so it can

    Args:
        credentials_file: xml file containing login credentials

    Returns:
        A twitter.Twitter connection object
    """
    credentials = CredentialLoader( credentials_file )
    APP_NAME = credentials.find( 'app_name' )
    CONSUMER_KEY = credentials.find( 'consumer_key' )
    CONSUMER_SECRET = credentials.find( 'consumer_secret' )
    TOKEN_FILE = 'out/twitter.oauth'
    ACCESS_TOKEN = credentials.find( 'access_token' )
    ACCESS_TOKEN_SECRET = credentials.find( 'access_token_secret' )
    return twitter.Api( domain='api.twitter.com', api_version='1.1',
                        auth=twitter.oauth.OAuth( ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET ) )


class TwitterConnection( object ):
    """
    Connection using python-twitter
    NB, set to automatically sleep on rate limit
    """

    def __init__( self, credentials_file ):
        self.credentials = CredentialLoader( credentials_file )
        self.APP_NAME = self.credentials.find( 'app_name' )
        self.CONSUMER_KEY = self.credentials.find( 'consumer_key' )
        self.CONSUMER_SECRET = self.credentials.find( 'consumer_secret' )
        self.TOKEN_FILE = 'out/twitter.oauth'
        self.ACCESS_TOKEN = self.credentials.find( 'access_token' )
        self.ACCESS_TOKEN_SECRET = self.credentials.find( 'access_token_secret' )

        self.connection = twitter.api.Api(
            consumer_key=self.CONSUMER_KEY,
            consumer_secret=self.CONSUMER_SECRET,
            access_token_key=self.ACCESS_TOKEN,
            access_token_secret=self.ACCESS_TOKEN_SECRET,
            sleep_on_rate_limit=True
        )

        # self.connection = login(credentials_file)
        # alias for older stuff
        self.conn = self.connection
