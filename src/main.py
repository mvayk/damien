import engine.engine as engine
import game.game as game

if __name__ == "__main__":
    engine = engine.Engine()
    game = game.Game(engine)

    engine.run()
