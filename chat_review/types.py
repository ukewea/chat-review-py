from typing import Optional, Pattern


class GitlabConfig:
    def __init__(
        self,
        host: str,
        token: str,
        project_id: str,
        mr_iid: str,
        target: Optional[Pattern] = None,
    ):
        self.host = host
        self.token = token
        self.project_id = project_id
        self.mr_iid = mr_iid
        self.target = target


class ChatGPTConfig:
    def __init__(
        self,
        api_key: str,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        language: Optional[str] = None,
    ):
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.top_p = top_p
        self.language = language


class GitlabDiffRef:
    def __init__(self, base_sha: str, head_sha: str, start_sha: str):
        self.base_sha = base_sha
        self.head_sha = head_sha
        self.start_sha = start_sha


class GitlabChange:
    def __init__(
        self,
        new_path: str,
        old_path: str,
        new_file: bool,
        renamed_file: bool,
        deleted_file: bool,
        diff: str,
        last_new_line: Optional[int] = None,
        last_old_line: Optional[int] = None,
    ):
        self.new_path = new_path
        self.old_path = old_path
        self.new_file = new_file
        self.renamed_file = renamed_file
        self.deleted_file = deleted_file
        self.diff = diff
        self.last_new_line = last_new_line
        self.last_old_line = last_old_line
