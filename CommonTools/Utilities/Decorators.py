"""
Created by adam on 6/25/18
"""
import warnings
from functools import wraps

__author__ = 'adam'

if __name__ == '__main__':
    pass


def deprecated( deprecated_function, *args, **kwargs ):
    """
    Wrapper for deprecated functions which ensures that
    the user gets a warning that the function is deprecated
    when they call it.

    Use:
        @deprecated
        def fun(j):
            print(j)

    Output:
        DataTools/Cursors.py:14: DeprecationWarning: deprecated class threadsafe_iter:

    """

    @wraps( deprecated_function )
    def wrapper( *args, **kwargs ):
        warnings.filterwarnings( 'always' )
        warnings.warn( "deprecated", DeprecationWarning )
        deprecated_function( *args, **kwargs )

    return wrapper