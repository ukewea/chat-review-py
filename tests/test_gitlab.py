import unittest
from unittest.mock import MagicMock
from chat_review.gitlab import Gitlab
from chat_review.types import GitlabConfig, GitlabDiffRef, GitlabChange

class TestGitlab(unittest.TestCase):
    def setUp(self):
        self.config = GitlabConfig(
            host="https://gitlab.example.com",
            token="your_token",
            project_id=1,
            mr_iid=1,
        )
        self.gitlab = Gitlab(self.config)

    def test_init(self):
        self.assert_multiple([
            lambda: self.assertEqual(self.gitlab.host, "https://gitlab.example.com"),
            lambda: self.assertEqual(self.gitlab.project_id, 1),
            lambda: self.assertEqual(self.gitlab.mr_iid, 1),
        ])

    def assert_multiple(self, asserts):
        for a in asserts:
            with self.subTest():
                a()

    def test_parse_last_diff(self):
        git_diff = """@@ -9,6 +9,7 @@ var app = builder.Build();
            if (!app.Environment.IsDevelopment())
            {
                app.UseExceptionHandler(\"/Error\");
            +    app.UseExceptionHandler(\"/Error2\");
                // The default HSTS value is 30 days.
                app.UseHsts();
            }
            @@ -18,8 +19,6 @@ app.UseStaticFiles();

            app.UseRouting();

            -app.UseAuthorization();
            -
            app.MapRazorPages();

            app.Run();"""
        last_old_line, last_new_line = self.gitlab.parse_last_diff(git_diff)
        self.assert_multiple([
            lambda: self.assertEqual(last_old_line, 14),
            lambda: self.assertEqual(last_new_line, 15)
        ])

    def test_get_changes(self):
        # Mock the request.get method to return a sample response
        self.gitlab.request.get = MagicMock(return_value=MagicMock(json=lambda: {
            "changes": [
                {
                    "new_path": "file.py",
                    "old_path": "file.py",
                    "new_file": False,
                    "renamed_file": False,
                    "deleted_file": False,
                    "diff": """@@ -9,6 +9,7 @@ var app = builder.Build();
            if (!app.Environment.IsDevelopment())
            {
                app.UseExceptionHandler(\"/Error\");
            +    app.UseExceptionHandler(\"/Error2\");
                // The default HSTS value is 30 days.
                app.UseHsts();
            }
            @@ -18,8 +19,6 @@ app.UseStaticFiles();

            app.UseRouting();

            -app.UseAuthorization();
            -
            app.MapRazorPages();

            app.Run();""",
                }
            ],
            "diff_refs": {
                "base_sha": "base_sha",
                "head_sha": "head_sha",
                "start_sha": "start_sha",
            },
            "state": "opened",
        }))

        result = self.gitlab.get_changes()
        self.assert_multiple([
            lambda: self.assertEqual(result["state"], "opened"),
            lambda: self.assertIsInstance(result["changes"], list),
            lambda: self.assertIsInstance(result["changes"][0], GitlabChange),
            lambda: self.assertIsInstance(result["ref"], GitlabDiffRef),
        ])


if __name__ == '__main__':
    unittest.main()