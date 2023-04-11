import argparse
import asyncio
from chat_review.index import run
from chat_review.types import GitlabConfig, ChatGPTConfig


def main():
    parser = argparse.ArgumentParser(description="Chat-based Code Review")
    parser.add_argument("--chatgpt", type=str, required=True, help="OpenAI API key")
    parser.add_argument("--token", type=str, required=True, help="GitLab private token")
    parser.add_argument("--project", type=str, required=True, help="GitLab project ID")
    parser.add_argument("--mr", type=str, required=True, help="Merge request IID")
    parser.add_argument("--host", type=str, required=True, help="GitLab host URL")

    args = parser.parse_args()

    gitlab_config = GitlabConfig(
        host=args.host, token=args.token, project_id=args.project_id, mr_iid=args.mr_iid
    )

    chatgpt_config = ChatGPTConfig(api_key=args.api_key)

    asyncio.run(run(gitlab_config, chatgpt_config))


if __name__ == "__main__":
    main()
