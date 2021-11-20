from experta import Fact

from src.engine import FixPCRobot, Checks


def run_engine():
    engine = FixPCRobot()
    engine.reset()
    engine.declare(Fact(Checks.INITIAL))
    engine.run()


if __name__ == '__main__':
    run_engine()
