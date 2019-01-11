"""
Functions for plotting temporal and other properties of tweets
Created by adam on 1/11/19
"""
__author__ = 'adam'

from bokeh.io import show
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure, output_notebook
# from bokeh.sampledata.commits import data
from bokeh.transform import jitter

# from bokeh.plotting import *
from bokeh.models import FuncTickFormatter
from bokeh.models.tickers import FixedTicker

from bokeh.palettes import Spectral6, Category20, magma, inferno, viridis


def color_generator(num_colors, palette_function=viridis):
    """Returns a color from the relevant palette each time it is called"""
    colorlist = palette_function(num_colors)
    for c in colorlist:
        yield c


def plot_tweet_distributions( frame, terms: list, title='tweet frequencies', **kwargs ):
    """
    Uses bokeh to make a jittered plot of tweet timestamps
    :param frame: Dataframe with columns tweetTime (datetime), tweet (int), term (str)
    :param terms: List of terms appearing in the frame
    :param title: Title to disply in plot
    :param kwargs: Possibly contains color_generator, ticker
    If a ticker is included, it should be a function which returns labels for integer
    inputs like this:
        def ticker():
            # Replaces the numeric y axis label with the correct term
            # The dict seems to need to be hardcoded since bokeh
            # messes with any args or values which seem like they should be
            # in scope
            dd = {
                1: 'crps',
                2: 'migraine',
                3: 'fibromyalgia'
            }
            term = dd.get( tick )
            return "{}".format( term )
    """
    try:
        # If was passed a custom color generator, initialize it
        colorgen = kwargs['color_generator'](len(terms))
    except:
        # Otherwise use the default color generator
        colorgen = color_generator(len(terms))

    # initialize the notebook output
    output_notebook()

    # create a new plot with a title and axis labels
    p = figure(title=title,
               x_axis_type="datetime",
               plot_width=800,
               plot_height=500,
               x_axis_label='timestamp',
               y_axis_label='term')

    for term in terms:
        color = next(colorgen)
        source = ColumnDataSource(frame[frame.term == term])
        p.circle(x='tweetTime',
                 y=jitter('tweet', width=0.5, range=p.y_range),
                 fill_color=color,
                 source=source,
                 alpha=0.6
                 )

    p.x_range.range_padding = 0
    p.ygrid.grid_line_color = None
    # p.legend.orientation = "horizontal"

    try:
        # If we were passed a ticker function for labeling the y axis
        # we use it here
        ticker = kwargs['ticker']
        # limit the displayed tick locations to those corresponding to the
        # terms in the dataframe
        tick_locations = [x for x in range(1, len(terms) + 1)]
        p.yaxis.ticker = FixedTicker(ticks=tick_locations)

        # Now add the labels instead of the numbers to the y axis
        p.yaxis.formatter = FuncTickFormatter.from_py_func(ticker)
    except:
        # If we didn't get one, as will likely be true if we are only plotting
        # a single term, no worries.
        pass

    # show the results
    show(p)
if __name__ == '__main__':
    pass