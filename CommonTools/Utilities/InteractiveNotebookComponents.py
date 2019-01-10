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
    def __init__( self ):
        self.output = [ ]

    def handle_submit( self, term ):
        self.output.append( term )

    def handle_reset( self ):
        self.output = [ ]

    def get_output( self ):
        return self.output


class TextPlusButtons( object ):

    def __init__( self, label, handler_object ):
        self.handler_object = handler_object
        # create widgets
        self.t = widgets.Text( description=label )
        self.submit = widgets.Button( description='Submit' )
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
        """Clear the input box"""
        self.t.value = ''

    def reset_output( self, ):
        self.out.clear_output()

    def handle_reset( self, change ):
        self.handler_object.handle_reset()  # reset_handler()
        self.reset_input()
        self.show_output()

    def handle_submit( self, change ):
        self.handler_object.handle_submit( self.t.value )
        self.reset_output()
        self.show_output()
        self.reset_input()

    def show_output( self ):
        output = self.handler_object.get_output()
        with self.out:
            clear_output()
            for item in output:
                print( item )


#
#
# def make_submission_text_input( label, submit_handler, reset_handler, output: list ):
#     """
#     Makes text input box with submit and reset buttons.
#     On submit button click, the handler is called
#     """
#     t = widgets.Text( description=label )
#     submit = widgets.Button( description='Submit' )
#     reset = widgets.Button( description='Reset' )
#     out = widgets.Output( layout={ 'border': '1px solid black' } )
#
#     def reset_input( ):
#         """Clear the input box"""
#         t.value = ''
#
#     def reset_output():
#         out.clear_output()
#
#     def handle_reset(change):
#         reset_handler()
#         reset_input()
#         show_output()
#
#     def handle_submit( change ):
#         submit_handler(t.value)
#         reset_output()
#         show_output()
#         reset_input()
#
#     def show_output():
#         # reset_output()
#         with out:
#             clear_output()
#             for item in output:
#                 print( item )
#
#     submit.on_click( handle_submit )
#     reset.on_click( handle_reset )
#     button_box = widgets.HBox( [ reset, submit ] )
#     input_box = widgets.VBox( [ t, button_box ] )
#     display( widgets.HBox( [ input_box, out ] ) )


if __name__ == '__main__':
    pass
