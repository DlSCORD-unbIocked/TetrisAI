import neat

import graphics

# import tetris
import os
from board import Board
import time

# AI GEN


def eval_genomes(genomes, config):
    board_list = []
    totals = {"w": 0, " ": 0, "a": 0, "d": 0}
    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        board_list.append(Board(10, 20, genome, net))
    render = graphics.Graphics()
    while len(board_list) > 0:
        for board in board_list:
            board.clear_active()

            output = board.net.activate(
                [
                    board.piece.get_x(),
                    board.piece.get_y(),
                    board.calculate_stack_height(),
                    board.completed_lines,
                    board.find_first_rows(),
                    board.calculate_holes(),
                ]
            )
            board.put_active()
            key = ["w", " ", "a", "d"][output.index(max(output))]
            totals[key] += 1
            if not (board.update("s")):
                board_list.remove(board)
                continue
            if not (board.update(key)):
                board_list.remove(board)
        if len(board_list) == 0:
            break
        render.draw_board(board_list[0])
    print(totals)


def play_best_genome(best_genome, config):
    net = neat.nn.FeedForwardNetwork.create(best_genome, config)
    board = Board(10, 20, best_genome, net)
    render = graphics.Graphics()
    while not board.game_over:
        board.clear_active()
        output = board.net.activate(
            [
                board.calculate_stack_height(),
                board.completed_lines,
                board.find_first_rows(),
                board.calculate_holes(),
            ]
        )
        board.put_active()
        key = ["w", " ", "a", "d"][output.index(max(output))]
        if not (board.update("s")):
            break
        if not (board.update(key)):
            break
        render.draw_board(board)
        time.sleep(0.05)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    cfg = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path,
    )
    p = neat.Population(cfg)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    # testing with 1
    winner = p.run(eval_genomes, 40)

    print("\nBest genome:\n{!s}".format(winner))

    play_best_genome(winner, cfg)
