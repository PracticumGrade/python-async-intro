import abc
from datetime import datetime
from typing import Union, List, Any, Callable


class Job(abc.ABC):
    """
    Базовый класс задач.
    name - имя задания, должно быть уникальным (обязательный параметр)
    start_at - дата запуска задания (опциональный параметр)
    max_working_time - дата окончания выполнения задания(опциональный параметр)
    tries - количество перезапусков в случае ошибки (опциональный параметр)
    dependencies - зависимости от других заданий (опциональный параметр)
    """

    def __init__(
            self,
            name: str,
            start_at: datetime = datetime.now(),
            max_working_time: Union[datetime, int] = -1,
            tries: int = 0,
            dependencies: List[str] = [],
            priority: float = float('inf')
    ):
        self.name = name
        self.start_at = start_at
        self.max_working_time = max_working_time
        self.tries = tries
        self.dependencies = dependencies
        self.priority = priority

    @abc.abstractmethod
    def run(self, state) -> Any:
        pass

    def __repr__(self):
        return (
            f' Задание - {self.name} \n'
            f' запустить в - {self.start_at} \n'
            f' зависимости - {self.dependencies} \n'
            f' попыток перезапуска - {self.tries} \n'
        )


class ReadFile(Job):
    """Класс для чтения данных из файла."""
    pass


class StringCapitalizer(Job):
    """Класс делающий первую букву слова большой."""
    pass


class WriteFile(Job):
    """Класс для записи данных в файл."""
    pass
