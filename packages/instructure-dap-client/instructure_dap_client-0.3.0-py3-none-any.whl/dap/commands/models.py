from dataclasses import dataclass

from ..dap_types import JobID, Object, ObjectID


@dataclass
class ContextAwareObject(Object):
    def __init__(self, id: ObjectID, index: int, total_count: int, job_id: JobID):
        super().__init__(id=id)
        self._index = index
        self._total_count = total_count
        self._job_id = job_id

    def __str__(self):
        return f"[object {self._index + 1}/{self._total_count} - job {self._job_id}]"
