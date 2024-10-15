import random
from typing import Literal

def find_random_move(gs):
    valid_moves = gs.get_valid_moves()
    if not valid_moves:
        return None  # Return None if no valid moves are available
    return valid_moves[random.randint(0, len(valid_moves) - 1)]


def find_move_minimax(gs, depth, turn: Literal[1, -1], max_depth=float('inf')):
    if gs.is_game_over() is not None or depth >= max_depth:
        return gs.is_game_over()

    valid_moves = gs.get_valid_moves()  # Recalculate valid moves after each board change

    if turn == 1:  # X to move -> maximizing
        max_score = -float('inf')
        for move in valid_moves:
            gs.make_move(move[0], move[1])
            score = find_move_minimax(gs, depth + 1, turn * -1, max_depth)
            gs.undo_move()
            max_score = max(score, max_score)
        return max_score

    elif turn == -1:  # O to move -> minimizing
        min_score = float('inf')
        for move in valid_moves:
            gs.make_move(move[0], move[1])
            score = find_move_minimax(gs, depth + 1, turn * -1, max_depth)
            gs.undo_move()
            min_score = min(score, min_score)
        return min_score


def find_best_move(gs, max_depth=float('inf')):

    valid_moves = gs.get_valid_moves()  # Recalculate valid moves after each board change
    turn = gs.turn
    list_of_moves = []

    if turn == 1:  # X to move -> maximizing
        max_score = -float('inf')
        for move in valid_moves:
            gs.make_move(move[0], move[1])
            score = find_move_minimax(gs, 0, turn * -1, max_depth)
            gs.undo_move()
            if score > max_score:
                max_score = score
                list_of_moves = [move]
            elif score == max_score:
                list_of_moves.append(move)
    elif turn == -1:  # O to move -> minimizing
        min_score = float('inf')
        for move in valid_moves:
            gs.make_move(move[0], move[1])
            score = find_move_minimax(gs, 0, turn * -1, max_depth)
            gs.undo_move()
            if score < min_score:
                min_score = score
                list_of_moves = [move]
            elif score == min_score:
                list_of_moves.append(move)
    
    return list_of_moves
