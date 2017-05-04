import matplotlib.pyplot as plt
import os


RINK_X                  = 200 # ft
RINK_Y                  = 85 # ft
BLUE_LINE_DX            = 25 # ft from center line
FACE_OFF_DOT_DX         = 69 # ft from center line
GOAL_LINE_DX            = 89 # ft from center line
BUFFER_X                = 5 # ft
BUFFER_Y                = 5 # ft


def new_rink_plot(size_x_in=20, size_y_in=6):
    """
    Create a new matplotlib NHL rink figure
    """
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    # Read rink image
    rink_file = os.path.join(os.path.dirname(__file__), '../images/rink.png')
    rink = plt.imread(rink_file)

    # Plot rink on figure
    ax.imshow(rink, origin='upper', alpha=0.9, extent=(-RINK_X/2, RINK_X/2, -RINK_Y/2, RINK_Y/2))
    fig.set_size_inches(size_x_in, size_y_in)

    return fig, ax


def add_team_logo(fig, ax, side, team):
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
        return fig, ax
    logo = plt.imread(logo_file)

    # Center team logo between the blue line and the offensive zone faceoff dot
    center_x = (BLUE_LINE_DX + FACE_OFF_DOT_DX)/2
    center_y = 0
    if side == 'home':
        center_x *= -1

    # Maintain logo scale but fix the width
    width = (BLUE_LINE_DX + FACE_OFF_DOT_DX)/3
    height = width*logo.shape[0]/logo.shape[1]

    # Plot logo on figure
    ax.imshow(logo, origin='upper', alpha=0.5, extent=(center_x-width/2, center_x+width/2, center_y-height/2, center_y+height/2))

    return fig, ax
