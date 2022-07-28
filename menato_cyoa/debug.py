import menato_cyoa.engine


def game_loop():
    engine = menato_cyoa.engine.Engine()
    player = "aster_test"
    while True:
        message = input("input: ")
        engine.read_instruction(message, player)

if __name__ == "__main__":
    game_loop()