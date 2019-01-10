"""
Containts functions for displaying notebook inputs

Created by adam on 1/10/19
"""
__author__ = 'adam'

"""
Created by adam on 1/7/19
"""
__author__ = 'adam'

from ipywidgets import widgets
from IPython.display import display


# -------- General
def make_text_input( label, handler ):
    """Creates a text input field.
    Note that the handler callback is called on every keystroke in the field
    :type handler: function
    :param handler: Function to call when the input changes
    :type label: str
    :param label: The text to display
    """
    text = widgets.Text( description=label )
    display( text )
    text.observe( handler )


def make_submission_text_input( label, handler, output: list ):
    """
    Makes text input box with submit and reset buttons.
    On submit button click, the handler is called
    """
    t = widgets.Text( description='Class id' )
    submit = widgets.Button( description='Submit' )
    reset = widgets.Button( description='Reset' )
    out = widgets.Output( layout={ 'border': '1px solid black' } )

    def reset_input( ):
        """Clear the input box"""
        t.value = ''

    def reset_output():
        out.clear_output()

    def handle_reset():
        reset_input()
        reset_output()

    def handle_submit( change ):
        handler(t.value)
        reset_output()
        show_output()

    def show_output():
        reset_output()
        with out:
            for item in output:
                print( item )

    submit.on_click( handle_submit() )
    reset.on_click( reset_output() )
    button_box = widgets.HBox( [ reset, submit ] )
    input_box = widgets.VBox( [ t, button_box ] )
    display( widgets.HBox( [ input_box, out ] ) )


def make_general_reset_button():
    rb = widgets.Button( description='Clear canvas token and class ids' )

    def reset_all( change ):
        InteractiveConfiguration.reset_config()

    display( rb.on_click( reset_all ) )


if __name__ == '__main__':
    pass
