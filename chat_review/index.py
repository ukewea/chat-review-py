from .gitlab import Gitlab
from .chatgpt import ChatGPT
from .types import GitlabConfig, ChatGPTConfig
from .utils import logger


async def run(gitlab_config: GitlabConfig, chatgpt_config: ChatGPTConfig):
    gitlab = Gitlab(gitlab_config)
    chatgpt = ChatGPT(chatgpt_config)

    state_changes_ref = gitlab.get_changes()
    state = state_changes_ref["state"]
    changes = state_changes_ref["changes"]
    ref = state_changes_ref["ref"]

    if state != "opened":
        logger.log("MR is closed")
        return

    for change in changes:
        message = await chatgpt.code_review(change.diff)
        result = gitlab.code_review(change, message, ref)
        logger.info(message)
        if result:
            logger.info(result)
