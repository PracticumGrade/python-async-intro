from job import ReadFile, StringCapitalizer, WriteFile
from scheduler import Scheduler

if __name__ == '__main__':
    reader = ReadFile(name='reader', file_name='test.txt', priority=1)
    capitalizer = StringCapitalizer(name='capitalizer', priority=2)
    writer = WriteFile(name='writer', file_name='new_test.txt', priority=3)

    scheduler = Scheduler()
    scheduler.schedule_later(capitalizer)
    scheduler.schedule_later(writer)
    scheduler.schedule_later(reader)
    scheduler.run()
