"""
handles the main game, including user and algorithm moves, and game display
"""

import game_engine
import pygame
import graphics
import move_finder
from multiprocessing import Process, Queue
import time
import random
import cProfile

pygame.init()

if __name__ == "__main__":
    BOARD_SIZE = 4
    WIN_CONDITION = 4 #number of symbols in a row for a win
    gs = game_engine.GameState(BOARD_SIZE, WIN_CONDITION)
    graphics = graphics.Graphics(BOARD_SIZE)

    graphics.load_images()
    game_over = False
    running = True

    ai_thinking = False
    move_finder_process = None
    move_undone = False

    player_x = False  # If a human is playing X, this will be true. If it's an AI playing X, it will be false
    player_o = True  # Same as above but for O
    player_x_wins = 0
    player_o_wins = 0
    draws = 0

    while running:
        is_human_turn = (gs.turn == 1 and player_x) or (gs.turn == -1 and player_o)
        valid_moves = gs.get_valid_moves()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            # mouse handlers
            elif is_human_turn and e.type == pygame.MOUSEBUTTONDOWN:
                if not game_over:
                    location = pygame.mouse.get_pos()
                    col = location[0] // graphics.SQ_SIZE
                    row = location[1] // graphics.SQ_SIZE
                    gs.make_move(row, col)
                # key handlers
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_z:  # undo when 'z' is pressed
                    gs.undo_move()
                    game_over = False
                    result = None
                    
                if e.key == pygame.K_r:  # resets game when r is pressed
                    gs = game_engine.GameState(BOARD_SIZE, WIN_CONDITION)
                    game_over = False
                    result = None
                    valid_moves = None

        if not game_over and not is_human_turn and valid_moves: #26.23s, 26.53s vs. 26.52s, 26.13s
            # start_time = time.time()
            # pr = cProfile.Profile()
            # pr.enable()
            
            ai_moves = move_finder.find_best_move(gs)
            print(f"ai_moves: {ai_moves}")
            if not ai_moves:
                ai_move = move_finder.find_random_move(gs)
            else:
                ai_move = ai_moves[random.randint(0, len(ai_moves) - 1)][0]
            print(f"ai_move: {ai_move}")
            gs.make_move(ai_move[0], ai_move[1])
            time.sleep(.4)

            # end_time = time.time()
            # print(f"Time taken: {end_time - start_time:.6f} seconds")
            # pr.disable()
            # pr.print_stats() 
            # #78.336s for check_game_over; 38.44s for count_consecutive; 21.348s for count_in_direction; 15.872s for append()
            # #41.816s for check_game_over; 28.063s for count_consecutive; 16.027s for count_in_direction; 11.115s for append(); 146.799s total
            # #35.733s for check_game_over; 23.8s for count_consecutive; 13.715s for count_in_direction; 9.596s for append(); 124.457s total
            # #36.019s for check_game_over; 24.096s for count_consecutive; 13.809s for count_in_direction; 9.635s for append(); 125.475s total
            # #---#

        graphics.draw_game_state(gs.board)
        result = gs.is_game_over()
        if result != None:
            if result == 1:
                text = "X wins"
                player_x_wins += 1
            elif result == -1:
                text = "O wins"
                player_o_wins += 1
            elif result == 0:
                text = "Tie"
                draws += 1

            graphics.draw_end_text(text)
            game_over = True

            #reset game as soon as it ends. this is used to test how the ai performs against itself.
            """print(f"x: {player_x_wins}")
            print(f"o: {player_o_wins} \n")
            print(f"draws: {draws}")
            gs = game_engine.GameState(BOARD_SIZE, WIN_CONDITION)
            game_over = False
            result = None"""

        pygame.display.flip()

