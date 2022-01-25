class Path:
    @staticmethod
    def generate_task_path(task_name: str) -> str:
        task_base_path = "tasks/"
        return task_base_path + task_name

    @staticmethod
    def valid_path(abs_parent, child):
        if abs_parent[-1] not in ("\\", "/"):
            abs_parent += "/"
        return abs_parent + child

