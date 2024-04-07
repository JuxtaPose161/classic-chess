class Board():
    letters = [_ for _ in 'ABCDEFGH']
    numbers = [_ for _ in '87654321']
    def __init__(self):
        self.board_id = 0
        self.history = []
        self.board = [[None for _ in range(8)] for _ in range(8)]

    def __str__(self):
        count = 8
        result = ''
        for row in self.board:
            result+= f' {str(count)} '
            count -= 1
            for figure in row:
                if figure == None:
                    figure = ' '
                result += f'[{str(figure)}] '
            result+='\n'
        result += ' #  A   B   C   D   E   F   G   H'
        return result

    def convert_position(self, position):
        row = Board.numbers.index(position[1])
        column = Board.letters.index(position[0])
        return [row, column]
    def renderboard(self):
        for row in range(8):
            for column in range(8):
                if self.board[row][column] == None:
                    continue
                if self.board[row][column].position != [row, column]:
                    newrow, newcolumn = self.board[row][column].position
                    self.board[newrow][newcolumn] = self.board[row][column]
                    self.board[row][column] = None
        self.board_id+=1

    def check_color(self):
        return 'white' if self.board_id % 2 == 0 else 'black'
    def check_obstacles(self, start, end, ignore):
        if ignore == True:
            print('All good')
            return True
        row_steps = end[0]-start[0]
        column_steps = end[1]-start[1]
        if row_steps != 0:
            row_steps = [i for i in range(0, row_steps, row_steps//abs(row_steps))][1:]
        if column_steps != 0:
            column_steps = [i for i in range(0, column_steps, column_steps//abs(column_steps))][1:]
        if row_steps == 0:
            row_steps = [0]*len(column_steps)
        if column_steps == 0:
            column_steps = [0]*len(row_steps)
        for i in range(len(row_steps)):
            if self.board[start[0]+row_steps[i]][start[1]+column_steps[i]] != None:
                print('Wrong figure move (obstacles in path)')
                return False
        print('You can move that')
        return True
    def make_record(self):
        cast = []
        for row in range(8):
            r = []
            for column in range(8):
                if self.board[row][column] != None:
                    r.append(self.board[row][column])
                else:
                    r.append(None)
            cast.append(r)
        self.history.append(cast)
    def _unpack_record(self, rec:list):
        for row in range(8):
            for column in range(8):
                if rec[row][column] != None:
                    self.board[row][column] = rec[row][column]
                    self.board[row][column].position = [row, column]
                else:
                    self.board[row][column] = None
    def backup(self, steps):
        self.board_id -= steps
        self._unpack_record(self.history[self.board_id])
        self.history = self.history[:self.board_id+1]
class Figure():
    def __init__(self, color):
        self.position = None
        self.color = color
        self.ignore_obstacle = False
class Pawn(Figure):
    def __str__(self):
        return 'P' if self.color == 'white' else 'p'

    def check_move(self, start, end):
        if self.color == 'white':
            if start[1] != end[1]:
                if abs(start[0] - end[0]) == 1 and abs(start[1] - end[1]) == 1 and start[0]==3:
                    return True
                return False
            if (start[0] - end[0]) == 2 and self.position[0] != 6:
                return False
            if (start[0] - end[0]) not in (1, 2):
                return False
            return True
        if self.color == 'black':
            if start[1] != end[1]:
                if abs(start[0] - end[0]) == 1 and abs(start[1] - end[1]) == 1 and start[0]==4:
                    return True
                return False
            if (end[0] - start[0]) == 2 and self.position[0] != 1:
                return False
            if (end[0] - start[0]) not in (1, 2):
                return False
            return True

    def check_attack(self, start, end):
        if abs(start[0] - end[0]) == 1 and abs(start[1] - end[1]) == 1:
            return True

        return False
class Bishop(Figure):
    def __str__(self):
        return 'B' if self.color == 'white' else 'b'

    def check_move(self, start, end):
        if abs(start[0]-end[0]) != abs(start[1]-end[1]):
            print('Wrong Bishop move (wrong column or row)')
            return False

        print('Good move)')
        return True

    def check_attack(self, start, end):
        if abs(start[0]-end[0]) != abs(start[1]-end[1]):
            print('Wrong Bishop attack (wrong column or row)')
            return False

        print('Good move)')
        return True
class Knight(Figure):
    def __init__(self, color):
        super().__init__(color)
        self.ignore_obstacle = True

    def __str__(self):
        return 'N' if self.color == 'white' else 'n'

    def check_move(self, start, end):
        if abs(start[0]-end[0])==1 and abs(start[1]-end[1])==2 or abs(start[0]-end[0])==2 and abs(start[1]-end[1])==1:
            print('Good move)')
            return True
        print('Wrong Knight move (wrong column or row)')
        return False

    def check_attack(self, start, end):
        if abs(start[0] - end[0]) == 1 and abs(start[1] - end[1]) == 2 or abs(start[0] - end[0]) == 2 and abs(start[1] - end[1]) == 1:
            print('Good move)')
            return True
        print('Wrong Knight move (wrong column or row)')
        return False
class Rook(Figure):
    def __str__(self):
        return 'R' if self.color == 'white' else 'r'

    def check_move(self, start, end):
        if (start[0]==end[0]) != (start[1]==end[1]):
            print('Good move)')
            return True
        print('Wrong Rook move (wrong column or row)')
        return False

    def check_attack(self, start, end):
        if (start[0]==end[0]) != (start[1]==end[1]):
            print('Good move)')
            return True
        print('Wrong Rook move (wrong column or row)')
        return False
class Queen(Figure):
    def __str__(self):
        return 'Q' if self.color == 'white' else 'q'

    def check_move(self, start, end):
        if ((start[0]==end[0]) != (start[1]==end[1])) or (abs(start[0]-end[0]) == abs(start[1]-end[1])):
            print('Good move)')
            return True
        print('Wrong Queen move (wrong column or row)')
        return False

    def check_attack(self, start, end):
        if ((start[0]==end[0]) != (start[1]==end[1])) or (abs(start[0]-end[0]) == abs(start[1]-end[1])):
            print('Good move)')
            return True
        print('Wrong Queen move (wrong column or row)')
        return False
class King(Figure):
    def __str__(self):
        return 'K' if self.color == 'white' else 'k'

    def check_move(self, start, end):
        if abs(start[0]-end[0])<=1 and abs(start[1]-end[1])<=1:
            print('Good move)')
            return True
        print('Wrong King move (wrong column or row)')
        return False

    def check_attack(self, start, end):
        if abs(start[0]-end[0])<=1 and abs(start[1]-end[1])<=1:
            print('Good move)')
            return True
        print('Wrong King move (wrong column or row)')
        return False
class Checker(Figure):
    def __str__(self):
        return 'O' if self.color == 'white' else 'o'

    def check_move(self, start, end):
        if self.color == 'white':
            if start[0] - end[0] == 1 and abs(start[1] - end[1]) == 1:
                print('Good move')
                return True
            print('Wrong Pawn move')
            return False
        if self.color == 'black':
            if end[0] - start[0] == 1 and abs(end[1] - start[1]) == 1:
                print('Good move')
                return True
            print('Wrong Pawn move')
            return False

    def check_attack(self, start, end):
        if abs(start[0] - end[0]) == 2 and abs(start[1] - end[1]) == 2:
            print('Good move')
            return True
        print('Wrong Pawn attack (your try to attack is bullshit)')
        return False
class CheckerKing(Figure):
    def __str__(self):
        return 'K' if self.color == 'white' else 'k'

    def check_move(self, start, end):
        if abs(start[0]-end[0]) != abs(start[1]-end[1]):
            print('Wrong Bishop move (wrong column or row)')
            return False
        print('Good move)')
        return True

    def check_attack(self, start, end):
        if abs(start[0]-end[0]) != abs(start[1]-end[1]):
            print('Wrong Bishop attack (wrong column or row)')
            return False
        print('Good move)')
        return True
class ChessBoard(Board):
    def __init__(self):
        super().__init__()
        for i in range(8):
            self.board[1][i] = Pawn('black')
            self.board[6][i] = Pawn('white')
        for i in 0,7:
            self.board[0][i] = Rook('black')
            self.board[7][i] = Rook('white')
        for i in 1,6:
            self.board[0][i] = Knight('black')
            self.board[7][i] = Knight('white')
        for i in 2,5:
            self.board[0][i] = Bishop('black')
            self.board[7][i] = Bishop('white')
        self.board[0][3] = Queen('black')
        self.board[7][3] = Queen('white')
        self.board[0][4] = King('black')
        self.board[7][4] = King('white')
        for row in 0,1,6,7:
            for column in range(8):
                self.board[row][column].position = [row, column]
    def check_passant(self, start, end):
        if type(self.board[start[0]][start[1]])!=Pawn:
            return True
        if abs(start[0] - end[0]) == 1 and abs(start[1] - end[1]) == 1:
            if type(self.board[start[0]][end[1]])==Pawn:
                self.board[start[0]][end[1]]=None
                return True
            else:
                return False
        return True

    def check_endrow(self):
        for row in 0,7:
            for column in range(8):
                if self.board[row][column]==None:
                    continue
                elif type(self.board[row][column])==Pawn:
                    while True:
                        new_figure = input('Choose new figure: Rook, Bishop, Knight or Queen\n').upper()
                        if new_figure == 'ROOK':
                            self.board[row][column] = Rook(self.board[row][column].color)
                            break
                        elif new_figure == 'BISHOP':
                            self.board[row][column] = Bishop(self.board[row][column].color)
                            break
                        elif new_figure == 'KNIGHT':
                            self.board[row][column] = Knight(self.board[row][column].color)
                            break
                        elif new_figure == 'QUEEN':
                            self.board[row][column] = Queen(self.board[row][column].color)
                            break
                        else:
                            print('Wrong name of figure, try again')
                    self.board[row][column].position = [row, column]
                    return True
        return False
    def board_move(self, start, end, side):
        if self.board[start[0]][start[1]] == None:
            print('There is no Figure')
            return False
        if self.board[start[0]][start[1]].color != side:
            print('Its not your turn')
            return False
        if self.board[end[0]][end[1]] == None:
            if self.board[start[0]][start[1]].check_move(start,end):
                if self.check_obstacles(start, end, self.board[start[0]][start[1]].ignore_obstacle) and self.check_passant(start, end):
                    self.board[start[0]][start[1]].position = end
                    return True
            return False
        else:
            if self.board[start[0]][start[1]].check_attack(start, end) and self.board[start[0]][start[1]].color != self.board[end[0]][end[1]].color:
                if self.check_obstacles(start, end, self.board[start[0]][start[1]].ignore_obstacle):
                    self.board[start[0]][start[1]].position = end
                    return True
            print('Or you try to eat your figure. -_-')
            return False
    def check_win(self):
        kinglist = []
        for row in range(8):
            for column in range(8):
                if type(self.board[row][column]) == King:
                    kinglist.append(self.board[row][column])
        if len(kinglist)!=2:
            print(f'{kinglist[0].color} wins')
            return True
        return False
    def show_dangerous(self, position):
        dangerous = []
        side = self.check_color()
        for row in range(8):
            for column in range(8):
                figure = self.board[row][column]
                if figure == None:
                    continue
                if figure.color != side:
                    if figure.check_attack(figure.position, position) and self.check_obstacles(figure.position, position, figure.ignore_obstacle):
                        dangerous.append(f'{str(figure)} in {Board.letters[figure.position[1]]}{Board.numbers[figure.position[0]]}')
        if dangerous == []:
            return ''
        return f'For {str(self.board[position[0]][position[1]])} in {Board.letters[position[1]]}{Board.numbers[position[0]]} dangerous is:\n'+"\n".join(dangerous)
    def show_all_dangerous(self):
        all_dangerous = []
        for row in range(8):
            for column in range(8):
                if self.board[row][column]!=None and self.board[row][column].color==self.check_color():
                    all_dangerous.append(self.show_dangerous([row,column]))
        return ''.join(all_dangerous)
    def show_moves(self, position):
        count = 8
        board = ''
        side = self.check_color()
        for row in range(8):
            r = f' {str(count)} '
            count -= 1
            for column in range(8):
                figure = self.board[row][column]
                if figure==None:
                    if self.board[position[0]][position[1]].check_move(position, [row, column]) and self.check_obstacles(position, [row, column], self.board[position[0]][position[1]].ignore_obstacle):
                        r += '[.] '
                    else:
                        r += '[ ] '
                elif figure.color != side:
                    if self.board[position[0]][position[1]].check_attack(position, figure.position) and self.check_obstacles(position, figure.position, self.board[position[0]][position[1]].ignore_obstacle):
                        r += '[X] '
                    else:
                        r += f'[{str(figure)}] '
                else:
                    r += f'[{str(figure)}] '
            r+='\n'
            board+=r
        board+=' #  A   B   C   D   E   F   G   H'
        return board
class CheckersBoard(Board):
    def __init__(self):
        super().__init__()
        for i in range(3):
            for j in range(8):
                if (i+j) % 2 != 0:
                    self.board[i][j] = Checker('black')

        for i in range(5,8):
            for j in range(8):
                if (i+j) %2 != 0:
                    self.board[i][j] = Checker('white')

        for row in 0, 1, 2, 5, 6, 7:
            for column in range(8):
                if self.board[row][column] != None:
                    self.board[row][column].position = [row, column]

    def board_move(self, start, end, side):
        if self.board[start[0]][start[1]] == None:
            print('There is no Figure')
            return False
        if self.board[start[0]][start[1]].color != side:
            print('Its not your turn')
            return False
        if self.board[end[0]][end[1]] != None:
            print('You cant stop at figure')
        else:
            if self.board[start[0]][start[1]].check_move(start,end):
                self.board[start[0]][start[1]].position = end
                return True
            elif self.board[start[0]][start[1]].check_attack(start, end) and self.check_obstacles(start, end, False)==False:
                if start[0] < end[0]:
                    if self.board[end[0]-1][end[1]-((end[1]-start[1])//abs(end[1]-start[1]))].color != self.board[start[0]][start[1]].color:
                        self.board[end[0]-1][end[1]-((end[1]-start[1])//abs(end[1]-start[1]))]=None
                        self.board[start[0]][start[1]].position = end
                        return True
                    return False
                else:
                    if self.board[end[0]+1][end[1]-((end[1]-start[1])//abs(end[1]-start[1]))].color != self.board[start[0]][start[1]].color:
                        self.board[end[0]+1][end[1]-((end[1]-start[1])//abs(end[1]-start[1]))]=None
                        self.board[start[0]][start[1]].position = end
                        return True
                    return False
            else:
                print('Strange move -_-')
                return False
    def check_kings(self):
        for i in range(8):
            if self.board[0][i] != None:
                if self.board[0][i].color == 'white':
                    self.board[0][i] = CheckerKing('white')
                    self.board[0][i].position = [0, i]
            if self.board[7][i] != None:
                if self.board[7][i].color == 'black':
                    self.board[7][i] = CheckerKing('black')
                    self.board[7][i].position = [7, i]
    def check_win(self):
        whites = None
        blacks = None
        for row in range(8):
            for column in range(8):
                if self.board[row][column] == None:
                    continue
                if self.board[row][column].color == 'white':
                    whites = True
                if self.board[row][column].color == 'black':
                    blacks = True
        if whites == None:
            print('Black wins!')
            return True
        if blacks == None:
            print('White wins')
            return True
        return False

