from math import degrees, atan, sin, radians


def straight_length(point_1: list, point_2: list):

    #         _________________________
    #        /(X2 - X1)^2 + (Y2 - Y1)^2

    return (((point_2[0] - point_1[0]) ** 2) + ((point_2[1] - point_1[1]) ** 2)) ** .5


def angle_straight(point_1: list, point_2: list):

    # (Y2 - Y1)       _1                         _.-`| (X1,Y1) a<
    #  m = ---------    tan   (m)               m _.-`   _|
    #      (X2 - X1)               (X2,Y2) a< _.-`______|_|

    m = (point_2[1] - point_1[1]) / (point_2[0] - point_1[0])
    angles = dict()
    angles['X1 , 0'] = abs(degrees(atan(m)))
    angles['0, Y2'] = 90 - angles['X1 , 0']
    return angles


def circular_coordinates(center_coordinates: list, radius, num_circle_divisions=0, displacement_units=0, direction=''):

    x_center = center_coordinates[0]
    y_center = center_coordinates[1]
    x = y = 0

    try:
        unit_division_circle = 360 / num_circle_divisions

    except ZeroDivisionError:
        return {'x': x_center, 'y': y_center}

    if direction == 'time':
        y = 90 - ((unit_division_circle * displacement_units) + unit_division_circle)
        x = 90 - abs(y)
    elif direction == 'counterclockwise':
        x = - ((unit_division_circle * displacement_units) + unit_division_circle)
        y = 90 - abs(x)
    else:   # radial direction
        x = 90 - (unit_division_circle * displacement_units)
        y = 90 - abs(x)

    cartesian_x = (sin(radians(x)) * radius)
    cartesian_y = (sin(radians(y)) * radius)
    return {'x': x_center + cartesian_x, 'y': y_center - cartesian_y}

#                                   x1+ -->
#                         y1+ +- - - - - |- - - - - - +
#                         |   |      . . 12. .        |
#                         v   |    11    |      1     |
# [oX +, oY -]__/ [-x, +y ]   |  10      |        2   |   [+x ,+y ] \__ [oX +, oY -]
#               \ [+x1,+y1]   |.         | [oX,oY]  . |   [+x1,+y1] /
#                 ------------|9---------|/---------3 |-----------
#                             |.         |          . |
#                             |  8       |        4   |
# [oX +, oY -]__/ [-x, +y ]   |    7     |      5     |   [+x, -y ] \__ [oX +, oY -]
#               \ [+x1,+y1]   |      . . 6 . .        |   [+x1,+y1] /
#                             +- - - - - |- - - - - - +
#


if __name__ == '__main__':
    circ_cord = circular_coordinates([100, 100], 100, 12, 2, 'TIME')
    print(circ_cord)
