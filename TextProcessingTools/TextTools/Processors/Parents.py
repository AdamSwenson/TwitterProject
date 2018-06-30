"""
These bind together a set of filters, modifiers, and tokenizers into an
object which handles the actual processing tasks.

They may be run in succession to each other:
paragraph processor -> sentence processor
sentence processor -> single word

However, these processors do not provide any other handling or control.
Those are the responsibility of the consumer of these objects.

The main consumers of these objects are in:
TextProcessingTools/StatisticalTools
DataAnalysis/ProcessingTools/ProcessingControllers


Created by adam on 5/20/18
"""
import TextProcessingTools.TextTools.Replacement.Interfaces
from TextProcessingTools.TextTools.Filtration import Filters
from TextProcessingTools.TextTools.Replacement import Modifiers

__author__ = 'adam'

if __name__ == '__main__':
    pass


class IProcessor(object):
    """
    This is the base class for the single operation modules
    which are used to process text
    """

    def __init__(self):
        self._modifiers = []
        self._listmodifiers = []
        self._filters = []
        self._ngram_filters = []

        # Defaults
        # Format of what process returns
        self.return_indexed = False

    def add_modifiers( self, imodifier: TextProcessingTools.TextTools.Replacement.Interfaces.IModifier ):
        """
        Adds an object or list of objexts which does modification
        to the que of modifiers which get called by _check_unwanted()
        Example:
            bagmaker.add_to_cleaners(URLFilter())
            bagmaker.add_to_cleaners(UsernameFilter())
            bagmaker.add_to_cleaners(NumeralFilter())

        Args:
            imodifier:  list | IModifier or IModifierList inheriting object
        """
        if isinstance(imodifier, list):
            [ self._modifiers.append(f) for f in imodifier]
        else:
            self._modifiers.append(imodifier)


    def add_filters( self, ifilter: Filters.IFilter ):
        """
        Adds an object or list of objects which does filtration to the stack of filters
        Example:
            bagmaker.add_to_cleaners(URLFilter())
            bagmaker.add_to_cleaners(UsernameFilter())
            bagmaker.add_to_cleaners(NumeralFilter())

        Args:
            ifilter: IFilter inheriting object
            :type ifilter: list | Filters.IFilter
        """
        if isinstance(ifilter, list):
            [ self._filters.append(f) for f in ifilter]
        else:
            self._filters.append(ifilter)

        # todo Fix this !!!!!!!!!!!!!!!!
        # # print(type(ifilter))
        # if isinstance(ifilter, Filters.IFilter):
        #     # if PRINT_STEPS is True: print("Adding filter %s to filters stack" % ifilter.__name__)
        #     self._filters.append(ifilter)
        #
        # elif inspect.isclass(ifilter) and issubclass(ifilter, Filters.IFilter):
        #     self._filters.append(ifilter)
        #
        # elif isinstance(ifilter, INgramFilter):
        #     self._ngram_filters.append(ifilter)
        # else:
        #     print("Error attempting to add filter %s to filters stack" % ifilter.__name__)
        #     # raise ValueError

    def set_initial_transforms(self, listOfModifiers, **kwargs):
        """
        Sets some modifiers to run before any other operations happen.
        """
        raise NotImplementedError

    def process(self, to_process, **kwargs):
        """
        The main interface
        Args:
            to_process: Something which will be processed
        """
        raise NotImplementedError

    def _process_kwargs(self, kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)