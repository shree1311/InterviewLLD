import time
import heapq
from datetime import datetime, timedelta
from threading import Thread, Lock

class Task:
    """A simple task to be executed."""
    def __init__(self, task_id, description):
        self.task_id = task_id
        self.description = description

    def execute(self):
        print(f"Executing Task {self.task_id}: {self.description} at {datetime.now()}")

class ScheduledTask:
    """A wrapper for a Task to include its execution time."""
    def __init__(self, task: Task, execute_at: datetime):
        self.task = task
        self.execute_at = execute_at

    # To make this class comparable for the min-heap
    def __lt__(self, other):
        return self.execute_at < other.execute_at

class TaskScheduler:
    """A scheduler that executes tasks at their scheduled time."""
    def __init__(self):
        self.schedule = []  # Min-heap of ScheduledTask objects
        self._lock = Lock()
        self._running = True
        self.worker_thread = Thread(target=self._run)
        self.worker_thread.start()

    def schedule_task(self, task: Task, delay_seconds: int):
        """Schedules a task to run after a certain delay."""
        execute_at = datetime.now() + timedelta(seconds=delay_seconds)
        scheduled_task = ScheduledTask(task, execute_at)
        
        with self._lock:
            heapq.heappush(self.schedule, scheduled_task)
            print(f"Scheduled Task {task.task_id} to run at {execute_at}")

    def _run(self):
        """The main loop that checks for and runs tasks."""
        while self._running:
            now = datetime.now()
            with self._lock:
                if self.schedule and self.schedule[0].execute_at <= now:
                    task_to_run = heapq.heappop(self.schedule)
                    task_to_run.task.execute()
            
            # Sleep for a short duration to avoid busy-waiting
            time.sleep(0.1)

    def stop(self):
        """Stops the scheduler's worker thread."""
        self._running = False
        self.worker_thread.join()
        print("Task scheduler stopped.")
