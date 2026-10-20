from player_game.youtique import auto_sell
from player_game.accidents import tick_temporary_event
import player_game.game_state

def advance_game_tick(cursor, connection):

    player_game.game_state.game_tick += 1
    auto_sell(cursor, connection, player_game.game_state.game_tick)
    tick_temporary_event(player_game.game_state.game_tick)