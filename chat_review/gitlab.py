import re
from requests import RequestException, Session
from typing import Tuple
from .types import GitlabConfig, GitlabDiffRef, GitlabChange
from .utils import logger


class Gitlab:
    def __init__(self, config: GitlabConfig):
        self.host = config.host.rstrip("/")
        self.request = Session()
        self.mr_iid = config.mr_iid
        self.project_id = config.project_id
        self.target = config.target or re.compile(r"\..+$")
        self.headers = {"PRIVATE-TOKEN": config.token}

    def get_changes(self):
        # https://docs.gitlab.com/ee/api/merge_requests.html#get-single-merge-request-changes
        try:
            response = self.request.get(
                f"{self.host}/api/v4/projects/{self.project_id}/merge_requests/{self.mr_iid}/changes",
                headers=self.headers,
            )
            response.raise_for_status()
            data = response.json()
            changes, diff_ref, state = data["changes"], data["diff_refs"], data["state"]

            code_changes = [
                GitlabChange(
                    new_path=change["new_path"],
                    old_path=change["old_path"],
                    new_file=change["new_file"],
                    renamed_file=change["renamed_file"],
                    deleted_file=change["deleted_file"],
                    diff=change["diff"],
                )
                for change in changes
                if not change["renamed_file"]
                and not change["deleted_file"]
                and self.target.search(change["new_path"])
            ]

            for item in code_changes:
                last_old_line, last_new_line = self.parse_last_diff(item.diff)
                item.last_old_line = last_old_line
                item.last_new_line = last_new_line

            return {
                "state": state,
                "changes": code_changes,
                "ref": GitlabDiffRef(**diff_ref),
            }
        except RequestException as error:
            logger.error(error)
            return {
                "state": "",
                "changes": [],
                "ref": GitlabDiffRef("", "", ""),
            }

    @staticmethod
    def parse_last_diff(git_diff: str) -> Tuple[int, int]:
        diff_list = git_diff.split("\n")[::-1]
        last_line_first_char = (
            diff_list[1][0] if len(diff_list) > 1 and len(diff_list[1]) > 0 else ""
        )
        last_diff = next(
            (
                item
                for item in diff_list
                if re.search(r"^@@ -\d+,\d+ \+\d+,\d+ @@", item)
            ),
            "",
        )

        match = re.search(r"@@ -(\d+),(\d+) \+(\d+),(\d+) @@.*", last_diff)

        last_old_line_count, last_new_line_count = (
            (
                int(match.group(1)) + int(match.group(2)),
                int(match.group(3)) + int(match.group(4)),
            )
            if match
            else ("-1", "-1")
        )

        last_old_line = (
            -1 if last_line_first_char == "+" else int(last_old_line_count) - 1
        )
        last_new_line = (
            -1 if last_line_first_char == "-" else int(last_new_line_count) - 1
        )

        return last_old_line, last_new_line

    def post_comment(
        self, newPath=None, newLine=None, oldPath=None, oldLine=None, body="", ref=None
    ):
        # https://docs.gitlab.com/ee/api/discussions.html#create-a-new-thread-in-the-merge-request-diff
        try:
            response = self.request.post(
                f"{self.host}/api/v4/projects/{self.project_id}/merge_requests/{self.mr_iid}/discussions",
                json={
                    "body": body,
                    "position": {
                        "position_type": "text",
                        "base_sha": ref.base_sha,
                        "head_sha": ref.head_sha,
                        "start_sha": ref.start_sha,
                        "new_path": newPath,
                        "new_line": newLine,
                        "old_path": oldPath,
                        "old_line": oldLine,
                    },
                },
                headers=self.headers,
            )
            response.raise_for_status()
            return response.text
        except RequestException as error:
            logger.error(error)

    def code_review(self, change: GitlabChange, message: str, ref: GitlabDiffRef):
        last_new_line, last_old_line, new_path, old_path = (
            change.last_new_line,
            change.last_old_line,
            change.new_path,
            change.old_path,
        )

        if last_new_line == -1 and last_old_line == -1:
            logger.error("Code line error")
            return

        params = {}

        if last_old_line != -1:
            params["oldLine"] = last_old_line
            params["oldPath"] = old_path

        if last_new_line != -1:
            params["newLine"] = last_new_line
            params["newPath"] = new_path
            params["body"] = message
            params["ref"] = ref

            return self.post_comment(**params)
