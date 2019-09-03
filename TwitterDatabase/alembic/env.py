from __future__ import with_statement
from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig

from os import sys, path


# Can't use environment or anything which imports it since the command
# line variables won't be set
# import environment

from CommonTools.Credentialing.CredentialTools import CredentialLoader


x = path.dirname( path.dirname( path.dirname( path.abspath( __file__ ) ) ) )
sys.path.append( x )


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
from Models import TweetORM
target_metadata = TweetORM.Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

# Workaround not being able to get creds via environment (command line options
# make alembic fail)
# Make sure that the appropriate credential file name is defined in the alembic.ini
cred_folder = "{}/private_credentials".format(path.dirname(path.dirname( path.dirname( path.dirname( path.abspath( __file__ ) ) ) )))
cred_file = '{}/{}'.format(cred_folder, config.get_main_option("credentials_file"))
print("Reading credentials from : {}".format(cred_file))
credentials = CredentialLoader( cred_file )
driver = config.get_main_option("driver")
dsn = credentials.make_dsn(driver)
print(dsn)

# Overwrite the url value from config (NB, the
# url value in the config is non-functional
config.set_main_option( 'sqlalchemy.url', dsn )


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
