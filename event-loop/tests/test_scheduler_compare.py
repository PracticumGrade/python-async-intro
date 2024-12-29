from datetime import datetime, timedelta

from job import Job
from scheduler import Scheduler

class TestScheduler:
    class MockJob(Job):
        """Класс для создания тестовых задач."""

        def run(self, state):
            pass

    def test_compare_priority(self):
        """Тестирование сравнения задач по приоритету."""
        task1 = self.MockJob(name='task1', priority=1, start_at=datetime.now())
        task2 = self.MockJob(name='task2', priority=2, start_at=datetime.now())

        result = Scheduler._compare(task1, task2)
        assert result == -1  # task1 имеет меньший приоритет

        result = Scheduler._compare(task2, task1)
        assert result == 1  # task2 имеет больший приоритет

    def test_compare_start_at(self):
        """Тестирование сравнения задач с одинаковым приоритетом по времени запуска."""
        now = datetime.now()
        task1 = self.MockJob(name='task1', priority=1, start_at=now)
        task2 = self.MockJob(name='task2', priority=1,
                             start_at=now + timedelta(minutes=1))

        result = Scheduler._compare(task1, task2)
        assert result == 1  # task1 запускается раньше

        result = Scheduler._compare(task2, task1)
        assert result == -1  # task2 запускается позже

    def test_compare_equal(self):
        """Тестирование сравнения задач с одинаковым приоритетом и временем запуска."""
        now = datetime.now()
        task1 = self.MockJob(name='task1', priority=1, start_at=now)
        task2 = self.MockJob(name='task2', priority=1, start_at=now)
        assert  Scheduler._compare(task1, task2) == 0
