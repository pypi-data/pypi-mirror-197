from typing import Dict, List

from lupin_grognard.core.commit.commit import Commit
from lupin_grognard.core.tools.utils import info
from lupin_grognard.core.doc_generator.jinja_generator import JinjaGenerator
from lupin_grognard.core.git import Git


class CodeReview(JinjaGenerator):
    def __init__(self, commits: List[Commit]):
        self.commits = commits
        self.git = Git()

    def generate(self):
        project_url = self.git.get_remote_origin_url()
        project_name = project_url.split("/")[-1]
        info(msg=f"Collecting approvers report from {project_name}")
        approvers_report = self._get_approvers_report()
        self._generate_file(
            file_name="code_review",
            file_extension=".html",
            context={
                "approvers_report": approvers_report,
                "project_name": project_name,
                "project_url": project_url,
            },
        )

    def _generate_file(
        self, file_name: str, file_extension: str, context: Dict
    ) -> None:
        return super()._generate_file(file_name, file_extension, context)

    def _get_approvers_report(self) -> List[dict]:
        approvers_report = []
        for commit in self.commits:
            if commit.associated_closed_issue:
                info(
                    msg=f"Collecting report for issue {commit.associated_closed_issue}"
                )
                approvers_report.append(
                    {
                        "issue_id": commit.associated_closed_issue,
                        "title": commit.title,
                        "autor": commit.author,
                        "date": commit.author_date,
                        "approvers": commit.associated_mr_approvers,
                        "approver_date": commit.associated_mr_approvers_date,
                    }
                )
        return approvers_report
