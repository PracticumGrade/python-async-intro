from scheduler import Scheduler


class TestScheduler:
    def test_init_attributes(self):
        """Тестирование инициализации атрибутов."""
        scheduler = Scheduler(pool_size=5)
        scheduler.active_tasks = ['task1', 'task2']
        scheduler.delayed_tasks = ['task3']
        scheduler.finished_tasks = ['task4']
        scheduler.jobs_restart = {'task1': 1, 'task2': 2}

        # Сохраняем атрибуты
        scheduler._save_attributes()

        # Создаем новый экземпляр планировщика
        new_scheduler = Scheduler(pool_size=5)

        # Проверяем, что атрибуты инициализированы корректно
        assert new_scheduler.active_tasks == ['task1', 'task2']
        assert new_scheduler.delayed_tasks == ['task3']
        assert new_scheduler.finished_tasks == ['task4']
        assert new_scheduler.jobs_restart == {'task1': 1, 'task2': 2}
        assert new_scheduler.pool_size == 5
