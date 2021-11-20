from enum import Enum, auto

from experta import KnowledgeEngine, Rule, Fact, OR

from src.utils import ask_yes_no


# Определяем список возмонжных состояний для фактов
# Здесь используется Enum (перечесления), так как они позвоняют удобно
# определять список всевозможных значений в конкретном контексте. Язык
# Python имее встроенную поддержку для них в модуле enum
class Checks(Enum):
    INITIAL = auto()
    BLACK_SCREEN_CHECK = auto()
    CABLE_CHECK = auto()
    CABLE_PLUGGED_CHECK = auto()
    OS_CHECK = auto()
    DISK_CHECK = auto()
    CLEAN_RAM_CHECK = auto()
    REPLACE_RAM_CHECK = auto()
    REINSTALL_OS_CHECK = auto()
    FLASH_BIOS_CHECK = auto()
    CPU_CHECK = auto()
    REPLACE_CPU_CHECK = auto()
    GPU_CHECK = auto()
    MOTHERBOARD_CHECK = auto()


# Данный миксин был создан для того, чтобы вынести все возможные правила для левой ветки дерева правил
# с помощью этого разделения программа становится более логичной и простой для понимания
class MonitorShowingBranchMixin:
    @Rule(Fact(Checks.BLACK_SCREEN_CHECK, False))
    def black_screen_no(self):
        print('ОС загружается?')
        self._ask_and_declare(Checks.OS_CHECK)

    @Rule(Fact(Checks.OS_CHECK, False))
    def os_check_no(self):
        print('Жесткий диск работает?')
        self._ask_and_declare(Checks.DISK_CHECK)

    @Rule(Fact(Checks.DISK_CHECK, True))
    def disk_check_yes(self):
        print('Попробуйте переустановить систему. Помогло?')
        self._ask_and_declare(Checks.REINSTALL_OS_CHECK)

    @Rule(Fact(Checks.DISK_CHECK, False))
    def disk_check_no(self):
        print('Замените жёсткий диск на заведомо рабочий')
        self.halt()

    @Rule(Fact(Checks.REINSTALL_OS_CHECK, False))
    def reinstall_os_no(self):
        print('Прошейте BIOS. Помогло?')
        self._ask_and_declare(Checks.FLASH_BIOS_CHECK)

    @Rule(Fact(Checks.FLASH_BIOS_CHECK, False))
    def flash_bios_no(self):
        print('Обратитесь в сервисный центр')
        self.halt()


# Данный миксин был создан для того, чтобы вынести все возможные правила для правой ветки дерева правил
# с помощью этого разделения программа становится более логичной и простой для понимания
class MonitorBlackBranchMixin:
    @Rule(Fact(Checks.BLACK_SCREEN_CHECK, True))
    def black_screen_yes(self):
        print('Кабель к экрану подключен?')
        self._ask_and_declare(Checks.CABLE_CHECK)

    @Rule(Fact(Checks.CABLE_CHECK, False))
    def cable_check_no(self):
        print('Подключите кабель. Помогло?')
        self._ask_and_declare(Checks.CABLE_PLUGGED_CHECK)

    @Rule(OR(Fact(Checks.CABLE_PLUGGED_CHECK, False), Fact(Checks.CABLE_CHECK, True)))
    def ask_about_ram_clean(self):
        print('Почистите контакты оперативной памяти. Работает?')
        self._ask_and_declare(Checks.CLEAN_RAM_CHECK)

    @Rule(Fact(Checks.CLEAN_RAM_CHECK, False))
    def suggest_to_replace_ram(self):
        print('Поменяйте плашки ОЗУ. Помогло?')
        self._ask_and_declare(Checks.REPLACE_RAM_CHECK)

    @Rule(Fact(Checks.REPLACE_RAM_CHECK, False))
    def suggest_to_replace_cpu(self):
        print('Замените процессор. Помогло?')
        self._ask_and_declare(Checks.REPLACE_CPU_CHECK)

    @Rule(Fact(Checks.REPLACE_CPU_CHECK, False))
    def suggest_to_run_without_discrete_gpu(self):
        print('Попробуйте запустить без дискретной видеокарты на встроенной. Картинка есть?')
        self._ask_and_declare(Checks.GPU_CHECK)

    @Rule(Fact(Checks.GPU_CHECK, True))
    def suggest_to_send_gpu_to_service(self):
        print('Отдайте видеокарту в сервисный центр на ремонт')
        self.halt()

    @Rule(Fact(Checks.GPU_CHECK, False))
    def suggest_to_replace_motherboard(self):
        print('Замените материнскую плату с таким же сокетом. Помогло?')
        self._ask_and_declare(Checks.MOTHERBOARD_CHECK)

    @Rule(Fact(Checks.MOTHERBOARD_CHECK, False))
    def suggest_to_send_mb_to_service(self):
        print('Обратитесь в сервисный центр с ремонтом материнской платы')
        self.halt()


# Главный класс "движка" для экспертной системы. Она наследуется от KnowledgeEngine класса,
# который предоставляет функиональность различную функциональность для работыс ЭС. Данный
# класс содержит правила, по которым будет работать ЭС. Данная ЭС расширяется при помощи добавлений
# новых правил. Правила добавляются последством создания нового метода и декорированием его при помощи
# @Rule, куда уже передается предикат для активации правила
class FixPCRobot(MonitorShowingBranchMixin, MonitorBlackBranchMixin, KnowledgeEngine):
    def _ask_and_declare(self, state):
        self.declare(Fact(state, ask_yes_no()))

    @Rule(Fact(Checks.INITIAL))
    def initial_ask(self):
        print('Экран чёрный?')
        self._ask_and_declare(Checks.BLACK_SCREEN_CHECK)

    @Rule(OR(
        Fact(Checks.OS_CHECK, True),
        Fact(Checks.REINSTALL_OS_CHECK, True),
        Fact(Checks.FLASH_BIOS_CHECK, True),
        Fact(Checks.CABLE_PLUGGED_CHECK, True),
        Fact(Checks.CLEAN_RAM_CHECK, True),
        Fact(Checks.REPLACE_RAM_CHECK, True),
        Fact(Checks.REPLACE_CPU_CHECK, True),
        Fact(Checks.MOTHERBOARD_CHECK, True)
    ))
    def problem_solved(self):
        print('Проблема решена')
        self.halt()
