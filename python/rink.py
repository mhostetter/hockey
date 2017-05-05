import matplotlib.pyplot as plt
import os

RINK_DX                 = 200/2 # ft from center ice
RINK_DY                 = 85/2 # ft from center ice
BLUE_LINE_DX            = 25 # ft from center ice
FACE_OFF_DOT_DX         = 69 # ft from center ice
GOAL_LINE_DX            = 89 # ft from center ice
BUFFER_L                = 5 # ft on the left side of the rink
BUFFER_R                = 5 # ft on the right side of the rink
BUFFER_B                = 5 # ft on the bottom side of the rink
BUFFER_T                = 12 # ft on the top side of the rink
FIGURE_WIDTH            = BUFFER_L + RINK_DX*2 + BUFFER_R
FIGURE_HEIGHT           = BUFFER_B + RINK_DY*2 + BUFFER_T
SIDES                   = ['home', 'away']

class RinkFigure():
    def __init__(self, width_in=10):
        """
        Create a new matplotlib NHL rink figure
        """
        # Set up figure with only 1 axis and no border
        self.fig = plt.figure(frameon=False)
        self.fig.set_size_inches(width_in, FIGURE_HEIGHT/FIGURE_WIDTH*width_in)
        self.ax = plt.Axes(self.fig, [0.0, 0.0, 1.0, 1.0])
        self.fig.add_axes(self.ax)
        self.ax.axes.get_xaxis().set_visible(False)
        self.ax.axes.get_yaxis().set_visible(False)

        # Read rink image
        rink_file = os.path.join(os.path.dirname(__file__), '../images/rink.png')
        rink = plt.imread(rink_file)

        # Plot rink on figure
        self.ax.imshow(rink, origin='upper', alpha=0.4, extent=(-RINK_DX, RINK_DX, -RINK_DY, RINK_DY))

        # Force axes
        self.ax.set_xlim((-RINK_DX - BUFFER_L, RINK_DX + BUFFER_R))
        self.ax.set_ylim((-RINK_DY - BUFFER_B, RINK_DY + BUFFER_T))

        # Add author credit
        self.ax.text(RINK_DX + BUFFER_R, -RINK_DY - BUFFER_B, '@matthostetter ', horizontalalignment='right', verticalalignment='bottom')


    def add_team_logo(self, side, team):
        """
        Add NHL team logo to home or away side of the rink.
            :param fig: A matplotlib figure handle
            :param fig: A matplotlib axis handle
            :param side: Either 'home' or 'away'
            :param team: A valid NHL tricode, e.g. 'WSH', 'PIT', etc. 
        """
        # Read logo image
        logo_file = os.path.join(os.path.dirname(__file__), '../images/teams/{}.png'.format(team))
        if not os.path.exists(logo_file):
            raise ValueError('Invalid NHL team tricode')
            return
        logo = plt.imread(logo_file)

        # Center team logo between the blue line and the offensive zone faceoff dot
        center_x = BLUE_LINE_DX + (FACE_OFF_DOT_DX - BLUE_LINE_DX)/2
        center_y = 0
        if side == 'home':
            center_x *= -1

        # Maintain logo scale but fix the width
        width = (BLUE_LINE_DX + FACE_OFF_DOT_DX)/5
        height = width*logo.shape[0]/logo.shape[1]

        # Plot logo on figure
        self.ax.imshow(logo, origin='upper', alpha=0.4, extent=(center_x-width/2, center_x+width/2, center_y-height/2, center_y+height/2))


    def add_title(self, title):
        center_x = 0
        center_y = RINK_DY + 5
        self.ax.text(center_x, center_y, title, horizontalalignment='center', verticalalignment='bottom', size='x-large', weight='bold')


    def add_team_name(self, side, name, statistic=''):
        if side not in SIDES:
            raise ValueError('side must be in {}'.format(SIDES))
        center_x = BLUE_LINE_DX/4 if side == 'away' else -BLUE_LINE_DX/4
        center_y = RINK_DY + 1
        alignment = 'left' if side == 'away' else 'right'

        if statistic != '':
            statistic = '(' + statistic + ')'

        self.ax.text(center_x, center_y, '{} {}'.format(name, statistic), horizontalalignment=alignment, verticalalignment='bottom', size='medium')


    def add_markers(self, side, x, y, color1, color2, marker='o', labels=None):
        if side not in SIDES:
            raise ValueError('side must be in {}'.format(SIDES))
        if len(x) != len(y):
            raise ValueError('x and y must be of same length')
        if labels and len(labels) != len(x):
            raise ValueError('labels must be of same length as x and y')
        self.ax.scatter(x, y, marker=marker, color=color1, edgecolors=color2, linewidths=1, s=30, picker=True)
        self.fig.canvas.mpl_connect('pick_event', self.on_pick3)


    def on_pick3(self, event):
        # ind = event.ind
        print('Test')
        # print 'onpick3 scatter:', ind, npy.take(x, ind), npy.take(y, ind)


    def save(self, filename):
        plt.savefig(filename, pad_inches=0.0)
