"""
Containts functions for displaying notebook inputs

Created by adam on 1/10/19
"""
__author__ = 'adam'

"""
Created by adam on 1/7/19
"""
__author__ = 'adam'

from IPython.display import clear_output
from IPython.display import display
from ipywidgets import widgets


# -------- General
class EventHandler( object ):
    def __init__( self, callback ):
        self.callback = callback

    def parse_event( self, event ):
        if event[ 'type' ] == 'change' and event[ 'name' ] == 'value':
            newVal = event[ 'new' ]
            self.callback( newVal )


def make_text_input( label, handler ):
    """Creates a text input field.
    Note that the handler callback is called on every keystroke in the field
    Example:
        def handle_search(term):
            print(term)
        make_text_input('Term to search', handle_search)
    :type handler: function
    :param handler: Function to call with the input value when the input changes
    :type label: str
    :param label: The text to display
    """
    eh = EventHandler( handler )
    text = widgets.Text( description=label )
    display( text )
    text.observe( eh.parse_event )


class Handler( object ):
    """Base class for using the TextPlusButtons input"""
    def __init__( self ):
        self.output = [ ]

    def handle_submit( self, term ):
        self.output.append( term )

    def handle_reset( self ):
        self.output = [ ]

    def get_output( self ):
        return self.output


class TextPlusButtons( object ):
    """
    Makes text input box with submit and reset buttons.
    On submit and reset button clicks, the handler is called
    The appropriate output is displayed in an adjacent box
    """

    def __init__( self, label, handler_object ):
        """
        :param label: The text to display
        :param handler_object: The object which handles clicks etc
        :type handler_object: Handler
        """
        self.handler_object = handler_object
        # create widgets
        self.t = widgets.Text( description=label )
        self.submit = widgets.Button( description='Submit', button_style='success')
        self.reset = widgets.Button( description='Reset' )
        self.out = widgets.Output( layout={ 'border': '1px solid black' } )
        # attach handlers
        self.submit.on_click( self.handle_submit )
        self.reset.on_click( self.handle_reset )
        # display
        button_box = widgets.HBox( [ self.reset, self.submit ] )
        input_box = widgets.VBox( [ self.t, button_box ] )
        display( widgets.HBox( [ input_box, self.out ] ) )

    def reset_input( self ):
        """Clears the input box"""
        self.t.value = ''

    def reset_output( self, ):
        self.out.clear_output()

    def handle_reset( self, change ):
        self.handler_object.handle_reset()  # reset_handler()
        self.reset_input()
        self.show_output()

    def handle_submit( self, change ):
        self.submit.button_style = 'info'
        self.handler_object.handle_submit( self.t.value )
        self.reset_output()
        self.show_output()
        self.reset_input()
        self.submit.button_style = 'success'

    def show_output( self ):
        output = self.handler_object.get_output()
        with self.out:
            clear_output()
            for item in output:
                print( item )


def log_progress(sequence, every=None, size=None, name='Items'):
    """
    Displays a progress indicator
    Example
        def dothing(v):
            time.sleep(1)
            s = [1, 2, 3,4]
            for r in log_progress(s, every=1):
                dothing(r)
    From https://github.com/alexanderkuk/log-progress
    """
    from ipywidgets import IntProgress, HTML, VBox
    from IPython.display import display

    is_iterator = False
    if size is None:
        try:
            size = len(sequence)
        except TypeError:
            is_iterator = True
    if size is not None:
        if every is None:
            if size <= 200:
                every = 1
            else:
                every = int(size / 200)     # every 0.5%
    else:
        assert every is not None, 'sequence is iterator, set every'

    if is_iterator:
        progress = IntProgress(min=0, max=1, value=1)
        progress.bar_style = 'info'
    else:
        progress = IntProgress(min=0, max=size, value=0)
    label = HTML()
    box = VBox(children=[label, progress])
    display(box)

    index = 0
    try:
        for index, record in enumerate(sequence, 1):
            if index == 1 or index % every == 0:
                if is_iterator:
                    label.value = '{name}: {index} / ?'.format(
                        name=name,
                        index=index
                    )
                else:
                    progress.value = index
                    label.value = u'{name}: {index} / {size}'.format(
                        name=name,
                        index=index,
                        size=size
                    )
            yield record
    except:
        progress.bar_style = 'danger'
        raise
    else:
        progress.bar_style = 'success'
        progress.value = index
        label.value = "{name}: {index}".format(
            name=name,
            index=str(index or '?')
        )



if __name__ == '__main__':
    pass
