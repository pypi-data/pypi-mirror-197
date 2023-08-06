import string


class BulkLoadCommitOptions:
    def __init__(self, workspace: string, vc: string, async_commit: bool, poll_times: int, poll_interval_ms: int):
        self.workspace = workspace
        self.vc = vc
        self.async_commit = async_commit
        self.poll_times = poll_times
        self.poll_interval_ms = poll_interval_ms
