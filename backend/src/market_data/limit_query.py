import asyncio
from src.logging import Logging

class LimitQuery:
    def __init__(self, cluster, limit, sleep_time):
        self.cluster = cluster
        self.limit = limit
        self.sleep_time = sleep_time
        self.waiting = []
        self.execution = {}
        for i in range(cluster):
            self.execution[i] = [None] * self.limit

    def query_by_limit(self, *args, **kwargs):
        future = asyncio.Future()
        self.push(future, args, kwargs)
        return future

    def push(self, future, args, kwargs):
        self.waiting.append((future, args, kwargs))
        self.start_one_run()

    def get_empty_postion(self):
        for i in range(len(self.execution)):
            for j in range(len(self.execution[i])):
                if self.execution[i][j] == None:
                    return i, j
        return None, None

    def start_one_run(self):
        position = self.get_empty_postion()
        if position == (None, None):
            return

        print(f"find position: {position} is empty")

        if len(self.waiting) == 0:
            return
        next = self.waiting.pop(0)

        self.execution[position[0]][position[1]] = next
        asyncio.create_task(self.run(position, *next))
    
    async def run(self, position, future, args, kwargs):
        try:
            value = self.query(*args, **kwargs)
            future.set_result(value)
        except Exception as e:
            Logging.log(e)

        await asyncio.sleep(self.sleep_time)
        self.execution[position[0]][position[1]] = None
        self.start_one_run()