import asyncio
import time
import uuid

from plugin_server.facefusion import face_swap_internal


# 队列管理
# In queue 0
# Processing 1
# Completed 2
# Failed 3
class Task:
    def __init__(self):
        self.tasks = {}
        self.queue = asyncio.Queue()
        self.queue_task = []

    async def start_task(self, task_id: str, args):
        # Processing
        self.tasks[task_id] = 1
        loop = asyncio.get_event_loop()
        # 换脸
        success = await loop.run_in_executor(None, face_swap_internal, task_id, args)
        if success:
            # Completed
            self.tasks[task_id] = 2
        else:
            # Failed
            self.tasks[task_id] = 3

    async def process_queue(self):
        print("Process queue")
        while True:
            if self.queue.empty():
                break
            (task_id, *args) = await self.queue.get()
            await self.start_task(task_id, *args)
            self.queue.task_done()
            self.queue_task.pop(0)

    async def handle_request(self, *args):
        task_id = str(uuid.uuid4())

        # In queue
        self.tasks[task_id] = 0
        await self.queue.put((task_id, *args))

        if len(self.queue_task) == 0:
            asyncio.create_task(self.process_queue())

        self.queue_task.append(task_id)

        return task_id

    def get_queue_position(self, task_id):
        """
        通过task id查询排队排在第几位
        :param task_id: 任务id
        :return: 排队位置，如果任务不在排队中则返回-1
        """
        if task_id in self.queue_task:
            return self.queue_task.index(task_id)
        else:
            return -1
