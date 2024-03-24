###############################################################################
## an implementation of a ***very*** basic Tetris game in Python using Pygame
###############################################################################
'''rotate --- r
   pause ---- p
   direction buttons for movement'''

import sys
import copy
import pygame
import random

size = width, height = 400, 600
sqrsize, pen_size = 40, 1
occupied_squares = []
top_of_screen = (0, 0)
color = {
    "white": (255,255,255),
    "black": (0,0,0),
    "red" : (255,0,0),
    "orange" : (255,163,47),
    "yellow" : (255,236,33),
    "green" : (147,240,59),
    "blue" : (55,138,255),
    "pink" : (255,119,253),
    "purple" : (149,82,234)
}

SHAPES = [
    [['I', 'I', 'I', 'I']],  # I - Red
    [['T', 'T', 'T'], [' ', 'T', ' ']],  # T - Orange
    [['L', 'L', 'L'], ['L', ' ', ' ']],  # L - Yellow
    [['J', 'J', 'J'], [' ', ' ', 'J']],  # J - Green
    [[' ', 'S', 'S'], ['S', 'S', ' ']],  # S - Blue
    [['O', 'O'], ['O', 'O']],  # O - Pink
    [['Z', 'Z', ' '], [' ', 'Z', 'Z']]  # Z - Purple
]

top_x, top_y = top_of_screen[0], top_of_screen[1]

pygame.init()
screen = pygame.display.set_mode(size)
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((color['white']))
screen.blit(background, top_of_screen)
pygame.display.flip()

################################################################################
#constructors and selectors for a tetrominoe shape
################################################################################
def make_tetrominoe(block1, block2, block3, block4, name):
    """Inputs<- 4 constituent blocks that make up a tetrominoe shape and name
       of tetrominoe shape.
       This returns a tetrominoe shape."""
    return [block1, block2, block3, block4, name]

def get_tetname(tetrominoe):
    """returns the name of a tetrominoe shape"""
    return tetrominoe[4]

def get_blocks(tetrominoe):
    """returns a list of blocks that make up a tetrominoe piece"""
    return tetrominoe[:4]

def get_refblock(tetrominoe):
    """gets reference block.Reference block is one around which other
    blocks are drawn"""
    return tetrominoe[3]

def block_points(tetronimoe):
    """gets the coordinates of the individual blocks that make up a tetrominoe
    piece"""
    blocks = get_blocks(tetronimoe) 
    return [get_point(block) for block in blocks]


###############################################################################
#constructors and selectors for a tetrominoe shape block
###############################################################################
def make_block(point, breadth, length):
    """This returns a block. A block is one of the constituent parts of a
    tetrominoe shape and is made up of a start coordinate,the breadth of the
    block and the lenght"""
    return [point, breadth, length]

def get_point(a_block):
    """returns the coordinate start point of block"""
    return a_block[0]

def block_width(a_block):
    """Returns the width of a block"""
    return a_block[1]

def block_height(a_block):
    """Returns the height of a block"""
    return a_block[2]


#############################################################################    
#constructors and selectors for coordinate points
##############################################################################
def make_point(x_coord, y_coord, colour):
    """Input<-coordinate of a point, color
       returns a point object with the coordinates of the point and color"""
    return [x_coord, y_coord, colour]

def point_x(a_point):
    """Returns the xcoordinate of a point structure"""
    return a_point[0]

def point_y(a_point):
    """Returns the ycoordinate of a point structure"""
    return a_point[1]

def point_color(a_point):
    """Returns the color of a point structure"""
    return a_point[2]


###############################################################################
###############################################################################
def delta_point(a_block, delta_x, delta_y):
    """input<- a block(constituent of a tetrominoe shape), integer, integer
       output->a block
       function which takes a block and increments its POINT"""
    point = get_point(a_block)
    return (make_block(make_point(point_x(point)+delta_x,
                                  point_y(point)+delta_y, point_color(point)),
                       block_width(a_block), block_height(a_block)))

###############################################################################
## game controller
###############################################################################
def tetris():
    
    """Sets up the whole game play and handles event handling"""
    mov_delay = 150
    events = {276: 'left', 275: 'right', 112: 'pause'}

    while True:
        draw_grid()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        move_dir = 'down' #default move direction
        game = 'playing'  #default game state play:- is game paused or playing?

        tet_shape = random_shape()

        if legal(tet_shape):
            draw_shape(tet_shape)
        else:
            break  #game over

        dets = find_column(get_tetname(tet_shape))

        sel_col = dets[0]
        rotate_count = dets[-1]

        mov_cnt = (sel_col - 80) / sqrsize

        if mov_cnt < 0:
            move_dir = 'left'
        elif mov_cnt > 0:
            move_dir = 'right'
        elif mov_cnt == 0:
            move_dir = 'down'

        mov_cnt = abs(mov_cnt)

        while rotate_count > 0:
            new_tet_shape = rotate(tet_shape)
            if legal(new_tet_shape):
                prev_tet, tet_shape = tet_shape, new_tet_shape
                draw_and_clear(tet_shape, prev_tet, mov_delay)
            rotate_count = rotate_count - 1

        while mov_cnt > 0:
            new_tet_shape = move(tet_shape, move_dir)
            if legal(new_tet_shape):
                prev_tet, tet_shape = tet_shape, new_tet_shape
                draw_and_clear(tet_shape, prev_tet, mov_delay)
            mov_cnt = mov_cnt - 1


        while True:
            if game == 'paused':
                for event in pygame.event.get((pygame.KEYDOWN, pygame.KEYUP)):
                    if event.key == pygame.K_p:
                        game, move_dir = 'playing', 'down'  
            else:
                for event in pygame.event.get((pygame.KEYDOWN, pygame.KEYUP)):
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p:
                            game, move_dir = 'paused', 'pause'
                            break

                    elif event.type == pygame.KEYUP:
                        mov_delay, move_dir = mov_delay, 'down'


                move_dir = 'down'
                new_tet_shape = move(tet_shape, move_dir)
                if legal(new_tet_shape):
                    prev_tet, tet_shape = tet_shape, new_tet_shape
                    draw_and_clear(tet_shape, prev_tet, mov_delay) 
                else:
                    #If shape didn't move and direction of movement is down
                    #then shape has come to rest so we can check for a full row
                    #which we delete before exiting loop and generating a new
                    #tetrominoe. if direction for movement is sideways
                    #and   block did not move it should be moved down rather
                    if move_dir == 'down':
                        occupied_squares.extend(block_points(tet_shape))
                        for row_no in range(height, -sqrsize, -sqrsize):
                            while row_filled(row_no):
                                delete_row(row_no)
                                background.fill(color['white'])
                                for point in occupied_squares:
                                    draw_block(point)
                        break
                    else:
                        draw_shape(tet_shape)
                        pygame.time.delay(mov_delay)


###########################################################################
###########################################################################                      
def draw_and_clear(tetrominoe, prev_tet, delay):
    """input<-two tetrominoe shapes
       clear the previously drawn tetrominoe first and then draw a new
       tetrominoe"""
    for point in block_points(prev_tet):
        background.fill((color['white']), (point_x(point), point_y(point),
                                           sqrsize, sqrsize))
        screen.blit(background, top_of_screen)
        pygame.display.update()
    draw_shape(tetrominoe)
    pygame.time.delay(delay)


############################################################################
############################################################################
def draw_shape(tetrominoe):
    """input<-tetriminoe shape
       This draws a tetrominoe shape to game board"""
    for point in block_points(tetrominoe):
        x, y = point_x(point), point_y(point)
        # Draw black border
        pygame.draw.rect(background, color['black'], (x, y, sqrsize, sqrsize))
        # Draw tetromino with its color
        #pygame.draw.rect(background, color[get_tetname(tetrominoe)], (x + pen_size, y + pen_size, sqrsize - 2 * pen_size, sqrsize - 2 * pen_size))
    screen.blit(background, top_of_screen)
    pygame.display.update()

############################################################################
############################################################################
    
def draw_grid():
    for x in range(0, width, sqrsize):
        pygame.draw.line(background, color['black'], (x, 0), (x, height))
    for y in range(0, height, sqrsize):
        pygame.draw.line(background, color['black'], (0, y), (width, y))



#############################################################################
#############################################################################
def draw_block(a_point):
    """draws a basic shape to screen"""
    pygame.draw.rect(background, point_color(a_point), (point_x(a_point),
                     point_y(a_point), sqrsize, sqrsize))
    pygame.draw.rect(background, point_color(a_point), (point_x(a_point),
                     point_y(a_point), sqrsize, sqrsize),1)


############################################################################
############################################################################
def row_filled(row_no, board=None):
    """input<-tetriminoe shape
       checks if a row on game board is fully occupied by a shape block"""
    if board:
        filled_coords = [(point_x(point), point_y(point)) for point in board]
        for col in range(0, width, sqrsize):
            if (col, row_no) in filled_coords:
                continue
            else:
                return False
        return True 

    else:
        filled_coords = [[point_x(pt), point_y(pt)] for pt in occupied_squares]
        for col in range(0, width, sqrsize):
            if [col, row_no] in filled_coords:
                continue
            else:
                return False
        return True 


##############################################################################
##############################################################################
def delete_row(row_no):
    """input<-integer(a row number)
       output->list of points
       removes all squares on a row from the occupied_squares list and then
       moves all square positions which have y-axis coord less than row_no down
       board"""
    global occupied_squares
    occupied_squares = [point for point in occupied_squares
                        if point_y(point) != row_no]
    for index in range(len(occupied_squares)):
        if point_y(occupied_squares[index]) < row_no:
            occupied_squares[index] = make_point(point_x(occupied_squares[index]),
                                    point_y(occupied_squares[index]) + sqrsize,
                                    point_color(occupied_squares[index]))


##############################################################################
##############################################################################
def legal(tet_shape):
    """Checks if a tetromino is in a legal portion of the board."""
    tet_block_points = block_points(tet_shape)
    filled_coords = [(point_x(pt), point_y(pt)) for pt in occupied_squares]
    for point in tet_block_points:
        new_x, new_y = point_x(point), point_y(point)
        if ((new_x, new_y) in filled_coords or (new_y >= height or
                                                (new_x >= width or new_x < top_x))):
            return False
    return True


##############################################################################
##############################################################################
def move(shape, direction, undo=False):
    """input<- a tetrominoe shape
       output<- a terominoe shape
       function moves a tetrominoe shape by moving all constituent blocks
       by a fixed amount in a direction given by 'direction' argument"""
    no_move = 0
    directions = {'down':(no_move, sqrsize), 'left':(-sqrsize, no_move),
        'right':(sqrsize, no_move), 'pause': (no_move, no_move)}
    delta_x, delta_y = directions[direction]
    if undo:
        delta_x, delta_y = -delta_x, -delta_y
    new_blocks = [delta_point (block, delta_x, delta_y)
                  for block in get_blocks(shape)]
    return (make_tetrominoe(new_blocks[0], new_blocks[1],
                            new_blocks[2], new_blocks[3], get_tetname(shape)))


##############################################################################
##############################################################################
def tetrominoe_shape(shape, start_x=80, start_y=0):
    """function returns a random tetrominoe piece"""
    shapes = {'S': make_tetrominoe(make_block(make_point(start_x + 1*sqrsize,
                                                         start_y + 2*sqrsize,
                                                         (0, 0, 0)),
                                             sqrsize, sqrsize),
                                  make_block(make_point(start_x, start_y,
                                                        (0, 0, 0)),
                                             sqrsize, sqrsize),
                                  make_block(make_point(start_x,
                                                        start_y + 1*sqrsize,
                                                        (0, 0, 0)),
                                             sqrsize, sqrsize),
                                  make_block(make_point(start_x + 1*sqrsize,
                                                    start_y + 1*sqrsize,
                                                    (0, 0, 0)),
                                             sqrsize, sqrsize)
                                  , 'S'),

        'O': make_tetrominoe(make_block(make_point(start_x + 1*sqrsize,
                                                  start_y + 1*sqrsize,
                                                ((255,119,253))),
                                        sqrsize, sqrsize),
                            make_block(make_point(start_x, start_y,
                                                  ((255,119,253))),
                                       sqrsize, sqrsize),
                            make_block(make_point(start_x, start_y + 1*sqrsize,
                                                  ((255,119,253))),
                                       sqrsize, sqrsize),
                            make_block(make_point(start_x + 1*sqrsize, start_y,
                                                  ((255,119,253))),
                                       sqrsize, sqrsize),
                            'O'),

        'I': make_tetrominoe(make_block(make_point(start_x, start_y + 3*sqrsize,
                                                   (0, 255, 0)),
                                       sqrsize, sqrsize),
                            make_block(make_point(start_x, start_y,
                                                  (0, 255, 0)),
                                       sqrsize, sqrsize),
                            make_block(make_point(start_x, start_y + 2*sqrsize,
                                                  (0, 255, 0)),
                                       sqrsize, sqrsize),
                            make_block(make_point(start_x, start_y + 1*sqrsize,
                                                  (0, 255, 0)),
                                       sqrsize, sqrsize),
                            'I'),

        'L':make_tetrominoe(make_block(make_point(start_x + 1*sqrsize,
                                                  start_y + 2*sqrsize,
                                                  (0, 0, 255)),
                                       sqrsize, sqrsize),
                            make_block(make_point(start_x, start_y,
                                                  (0, 0, 255)),
                                        sqrsize, sqrsize),
                            make_block(make_point(start_x, start_y + 2*sqrsize,
                                                  (0, 0, 255)),
                                       sqrsize, sqrsize),
                            make_block(make_point(start_x, start_y + 1*sqrsize,
                                                  (0, 0, 255)),
                                       sqrsize, sqrsize), 'L'),

        'T':make_tetrominoe(make_block(make_point(start_x + 1*sqrsize,
                                                  start_y + 1*sqrsize,
                                                  (255, 0, 0)),
                                       sqrsize, sqrsize),
                            make_block(make_point(start_x, start_y,
                                                  (255, 0, 0)),
                                       sqrsize, sqrsize),
                            make_block(make_point(start_x - 1*sqrsize,
                                                  start_y + 1*sqrsize,
                                                  (255, 0, 0)),
                                        sqrsize, sqrsize),
                            make_block(make_point(start_x,
                                                        start_y + 1*sqrsize,
                                                        (255, 0, 0)),
                                        sqrsize, sqrsize), 'T')
        }
    return shapes[shape]


#####
#####
def random_shape(start_x=80, start_y=0):
    """return a random tetrominoe shape"""
    tets = ['S', 'O', 'I', 'L', 'T']
    return tetrominoe_shape(tets[random.randint(0, 4)], start_x, start_y)


##############################################################################
##############################################################################
def rotate(tetrominoe):
    """input<- tetrominoe shape
       ouput-> tetrominoe shape
       rotates a tetrominoe shape if possible about a reference block."""
    #global occupied_squares
    if get_tetname(tetrominoe) == 'O':
        return tetrominoe
    else:
        ref_point = get_point(get_refblock(tetrominoe)) 
        x_coord = point_x(ref_point)
        y_coord = point_y(ref_point)

        tetblock_coords = block_points(tetrominoe) 

        new_tet = make_tetrominoe(make_block(make_point(x_coord +
                                            y_coord-point_y(tetblock_coords[0]),
                            y_coord - (x_coord - point_x(tetblock_coords[0])),
                            point_color(ref_point)), sqrsize, sqrsize,
                                             ),

                        make_block(make_point(x_coord + y_coord -
                                              point_y(tetblock_coords[1]),
                            y_coord - (x_coord - point_x(tetblock_coords[1])),
                            point_color(ref_point)), sqrsize, sqrsize),

                        make_block(make_point(x_coord + y_coord -
                                              point_y(tetblock_coords[2]),
                            y_coord - (x_coord - point_x(tetblock_coords[2])),
                            point_color(ref_point)), sqrsize, sqrsize),

                        make_block(make_point(x_coord, y_coord,
                                              point_color(ref_point)),
                                   sqrsize, sqrsize),
                    get_tetname(tetrominoe))

        #if legal(new_tet):
        return new_tet
        #else:
         #   return tetrominoe
####
####
def drop_shape(shape):
    """drop a shape into postion on a column"""
    new_shape = move(shape, 'down')
    prev_shape, new_shape = shape, new_shape
    while legal(new_shape):
        prev_shape, new_shape = new_shape, move(new_shape, 'down')
    return prev_shape


####
####
def bubble_count(shape):
    """returns number of new empty spots generated when a shape is placed at a 
    legal point"""
    count = 0
    points = [(point_x(pt), point_y(pt)) for pt in block_points(shape)]
    board = [(point_x(pt), point_y(pt)) for pt in occupied_squares]
    for pt in points:
        for i in range(point_y(pt) + sqrsize, height, sqrsize):
            if (pt[0], i) in board or (pt[0], i) in points:
                break
            else:
                count += 1
    return count

####
###
def shape_lowest_row(shape):
    """return the lowest row of a shape"""
    points = [(point_x(pt), point_y(pt)) for pt in block_points(shape)]
    points = sorted(points, key=lambda point: point[1], reverse=True)
    return points[0]

#####
#####
def row_filln_column(shape):
    """return a list of columns, rows filled tuple for each column on the 
    board if there are n columns for which a shape dropped in column fills
    a row"""
    rows_filled = []
    shape_rotates = {'S':2, 'I':1, 'O':0, 'L':3, 'T':3}
    rotate_count = shape_rotates[shape]
    curr_cnt = 0
    while True:
        for col in range(0, width, sqrsize):
            board = copy.deepcopy(occupied_squares)
            tet_shape = tetrominoe_shape(shape, start_x=col, start_y=0)
            cnt = curr_cnt
            while cnt > 0:
                tet_shape = rotate(tet_shape)
                cnt -= 1

            if not legal(tet_shape): # check shape is in board sideways
                continue
            tet_shape = drop_shape(tet_shape)
            board.extend(block_points(tet_shape))
            rows = 0
            for row in range(height, 0, -sqrsize):
                if row_filled(row, board=board):
                    rows += 1
            if rows > 0:
                rows_filled.append((col, rows, curr_cnt))
            tet_shape = rotate(tet_shape)

        if rotate_count == curr_cnt:
            break
        curr_cnt += 1
    if rows_filled:
        return rows_filled
    return None

####
####
def next_best_columns(shape):
    """return list of columns which a shape can go into if the shape cannot
    fill any rows"""
    next_best = []
    shape_rotates = {'S':2, 'I':1, 'O':0, 'L':3, 'T':3}
    rotate_count = shape_rotates[shape]
    curr_cnt = 0
    while True:
        for col in range(0, width, sqrsize):
            board = copy.deepcopy(occupied_squares)
            tet_shape = tetrominoe_shape(shape, start_x=col, start_y=0)
            cnt = curr_cnt
            while cnt > 0:
                tet_shape = rotate(tet_shape)
                cnt -= 1

            if not legal(tet_shape):
                continue
            tet_shape = drop_shape(tet_shape)
            board.extend(block_points(tet_shape))
            bubble_cnt = bubble_count(tet_shape)
            next_best.append((col, bubble_cnt, shape_lowest_row(tet_shape)[1],
                             curr_cnt))
            #print col, bubble_cnt
        if rotate_count == curr_cnt:
            break
        curr_cnt += 1
    return next_best

#####
#####
def find_column(shape):
    """find column of best fit to drop down a tetrominoe shape from"""
    # search for if any rows can be filled up by shape
    rows_filled = row_filln_column(shape)
    if not rows_filled:
        next_best = next_best_columns(shape)
        next_best =  sorted(next_best, key=lambda col: col[2], reverse=True)
        cols = sorted(next_best, key=lambda col: col[1])
        return cols[0]
    rows_filled = sorted(rows_filled, key=lambda row_filled: row_filled[1])
    return rows_filled[-1] #col with most rows filled


def m():
    draw_grid()
    tetris()
