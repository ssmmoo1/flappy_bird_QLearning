from flappy_bird import run_game
from player_ai import Agent
from game_config import *

run_game()
#states y dist to gap, x dist to gap
ai_player = Agent(table_shape=(SCREEN_HEIGHT, SCREEN_WIDTH, NUM_ACTIONS))
#wai_player.load_agent("q_table.pkl")
count = 0
while 1:
    count+=1
    run_game(agent=ai_player, framerate=-1)
    print(f"Game count: {count}")
    if count%100 == 0:
        print("Saving pkl")
        ai_player.save_agent("q_table.pkl")
        run_game(agent=ai_player, framerate=5)
