from model import *
def play(game):
    if game == 'chess':
        ch = ChessBoard()
    elif game == 'checkers':
        ch = CheckersBoard()
    else:
        return 'Wrong game'
    ch.make_record()
    print(ch)
    while True:
        step = input('Введите ход: ').upper().split()
        if step[0] == 'END':
            break
        if step[0] == 'BACKUP':
            ch.backup(int(step[1]))
            print(ch)
            continue
        if step[0] == 'DANG' and game == 'chess':
            print(ch.show_all_dangerous())
            continue
        if step[0] == 'SHOW' and game == 'chess':
            end = ch.convert_position(step[1])
            print(ch.show_moves(end))
            continue
        start = ch.convert_position(step[0])
        end = ch.convert_position(step[1])
        color = ch.check_color()
        if not ch.board_move(start, end, color):
            continue
        if game == 'checkers':
            ch.check_kings()
        if ch.check_endrow():
            ch.renderboard()
            ch.board_id-=1
        ch.renderboard()
        ch.make_record()
        if ch.check_win():
            print(ch)
            break
        print(ch)


if __name__ == '__main__':
    h = play('chess')
    print(h)