import sublime

from unittest import TestCase

from TestExplorer.test_explorer import TestExplorerMenuCommand


class TestParseTestFile(TestCase):
    """Tests for TestExplorerMenuCommand.parse_test_file, run with UnitTesting."""

    def setUp(self):
        self.view = sublime.active_window().new_file()
        self.view.set_scratch(True)
        self.command = TestExplorerMenuCommand(self.view)
        # the default configuration of the package, for .js files
        self.config = self.command.get_config_for_file("example.test.js")

    def tearDown(self):
        self.view.close()

    def parse(self, content):
        self.view.run_command("append", {"characters": content})
        return self.command.parse_test_file(self.config)

    def test_plain_titles(self):
        results = self.parse(
            "describe('math', () => {\n"
            "  it('adds', () => {});\n"
            "  it('subtracts', () => {});\n"
            "});\n"
        )
        self.assertEqual(
            results,
            [("math", 1, "group"), ("adds", 2, "test"), ("subtracts", 3, "test")],
        )

    def test_test_title_with_regex_characters(self):
        results = self.parse(
            "describe('math', () => {\n"
            "  it('adds', () => {});\n"
            "  it('handles (a|b) input', () => {});\n"
            "  it('works', () => {});\n"
            "});\n"
        )
        self.assertEqual(
            results,
            [
                ("math", 1, "group"),
                ("adds", 2, "test"),
                ("handles (a|b) input", 3, "test"),
                ("works", 4, "test"),
            ],
        )

    def test_group_title_with_regex_characters(self):
        results = self.parse(
            "describe('parse [a-z]+ (x|y)', () => {\n"
            "  it('works', () => {});\n"
            "});\n"
        )
        self.assertIn(("parse [a-z]+ (x|y)", 1, "group"), results)
        self.assertIn(("works", 2, "test"), results)

    def test_title_with_unbalanced_regex_characters(self):
        results = self.parse(
            "describe('unbalanced (', () => {\n"
            "  it('opens [ only', () => {});\n"
            "});\n"
        )
        self.assertIn(("unbalanced (", 1, "group"), results)
        self.assertIn(("opens [ only", 2, "test"), results)
