import functools
import os
import pickle
import shutil
import signal
from datetime import datetime
from typing import List

import config
from job import Job
from logger import Logger


class Scheduler:
    """Планировщик задач."""

    def __init__(self, pool_size: int = 10):
        self.state = {}  # для передачи данных между корутинами
        self.logger = Logger.create(
            logger_name=__name__,
            logger_level=config.LOGGER_LEVEL
        )
        self._init_attributes(pool_size)
        # Завершение работы программы по сигналу от ОС.
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, *args) -> None:
        """Завершение работы программы"""
        self._save_attributes()
        self.logger.critical('Завершение работы программы (сигнал от ОС)')
        exit('Выполнение программы завершено!')

    def _save_attributes(self) -> None:
        # этот метод должен сохранять текущее состояние планировщика. 


    def _init_attributes(self, pool_size: int) -> None:
        """Инициализация атрибутов."""
        # этот метод должен инициализировать атрибуты планировщика

    def schedule_soon(self, task: Job) -> None:
        """Поместить в очередь готовые к запуску задачи."""
        # Проверяем что список зависимостей, полностью присутствует в
        # списке завершенных задач

        if ((set(task.dependencies) & set(self.finished_tasks))
                == set(task.dependencies)):
            self.active_tasks.append(task)
        else:
            # если еще не все выполнились задачи из зависимости, то ждем их
            # завершения
            self.delayed_tasks.append(task)

    def logic_in_run_active_tasks(self, task: Job) -> None:
        task.run(self.state)

    def run_active_tasks(self) -> None:
        """Запустить готовые к запуску задачи."""
        for task in self.active_tasks:
            if task.done:
                self.active_tasks.remove(task)
                self.finished_tasks.append(task.name)
                self.logger.info(f'Задача с именем {task.name} завершилась'
                                 f'в {datetime.now()}')
                continue
            # пробуем осуществить запуск задачи

            try:
                self.logger.info(f'Задача с именем {task.name} запустилась'
                                 f'в {datetime.now()}')
                self.logic_in_run_active_tasks(task)
            except Exception as e:
                # если запуск задачи вызвал ошибку, но количество повторных
                # запусков больше 0
                if self.jobs_restart[task.name] > 0:
                    # делаем декремент по количеству попыток перезапуска
                    self.jobs_restart[task.name] -= 1
                    self.logger.error(
                        f'Запуск задачи {self.active_tasks} завершился с '
                        f'ошибкой  ---> {e} <---. '
                        f'Kолличество оставшихся перезапусков '
                        f'{self.jobs_restart[task.name]}'
                    )
                else:
                    # как только счетчик перезапусков стал равен 0,
                    # сообщаем в лог об ошибке
                    self.logger.error(
                        f'Запуск задачи {self.active_tasks} завершился с '
                        f'ошибкой --->  {e} <--- . '
                        f'Задача {task.name} '
                        f'была удалена из списка активных задач'
                    )
                    # и удаляем задачу из списка активеых
                    self.active_tasks.remove(task)

    @staticmethod
    def _compare(task_1: Job, task_2: Job) -> int:
        """ Функция для сравнения требуемого времени запуска для task"""
        # сначала сравниваем приоритеты
        # если одинаковые приоритеты, то сравнение по времени запуска

    def schedule_later(self, task: Job) -> None:
        """Поместить в очередь задачи, требующие задержку."""
        # Записываем в очередь
        if self.jobs_names.get(task.name) is None:
            self.jobs_names[task.name] = True
            self.jobs_restart[task.name] = task.tries
            self.delayed_tasks.append(task)
            # Сортируем очередь, чтобы получить приоритет
            self.delayed_tasks.sort(key=functools.cmp_to_key(self._compare))
        else:
            self.logger.error(
                f'Задача с именем {task.name} уже была запущена,'
                ' измените имя задачи!'
            )

    def check_delayed_tasks(self) -> None:
        """Проверить не требуют ли какие задачи из delayed_tasks запуска."""
        # Если какая задача из delayed_tasks имеет время запуска меньше или
        # равное текущему в системе, то задача переноситься в active_tasks
        delayed_tasks_temp = self.delayed_tasks.copy()
        for task in delayed_tasks_temp:
            # Количество активных задач д.б. не более заданного pool_size
            if len(self.active_tasks) >= self.pool_size:
                # если больше, то просто ждем когда освободится ресурс
                self.logger.debug(f'Задача с именем {task.name}'
                                  f' не смогла запуститься в {datetime.now()}'
                                  f' превышен лимит на количество задач!')
                return
            # если заданы приоритеты, то сразу такие задачи попадают в активные
            if (
                    task.priority != float('inf')
                    or task.start_at <= datetime.now()
            ):
                self.schedule_soon(task)
                self.delayed_tasks.remove(task)

    def check_max_working_time(self) -> None:
        """Проверить не превышено ли время работы задачи."""
        for i, task in enumerate(self.active_tasks):
            if task.max_working_time == -1:
                continue
            if task.max_working_time <= datetime.now():
                self.active_tasks.pop(i)
                self.finished_tasks.append(task.name)
                self.logger.info(f'Задача с именем {task.name} завершилась'
                                 f'в {datetime.now()}')

    def run(self) -> None:
        """Основной цикл программы."""
        # Пока есть задачи в одной из очередей
            # Проверяем есть ли задачи, которые надо сделать активными
            # Проверяем есть ли задачи, которые надо удалить из активных
            # (лимит времени)
                # Запускаем активные задачи
