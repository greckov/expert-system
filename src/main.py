from experta import Fact

from src.engine import FixPCRobot, Checks


def run_engine():
    # Инициализация "движка" экспертной системы
    engine = FixPCRobot()
    # Сброс всего состояния "движка" для последующего его запуска
    engine.reset()
    # Передача начального факта в ЭС
    engine.declare(Fact(Checks.INITIAL))
    # Запуск "движка" экспертной системы
    engine.run()


if __name__ == '__main__':
    run_engine()
