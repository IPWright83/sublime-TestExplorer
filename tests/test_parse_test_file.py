import importlib
import unittest

import sublime


PACKAGE = __name__.split(".")[0]
test_explorer = importlib.import_module(PACKAGE + ".test_explorer")

SETTINGS = "TestExplorer.sublime-settings"


class ParseTestFileTests(unittest.TestCase):
    def setUp(self):
        self.view = sublime.active_window().new_file()
        self.view.set_scratch(True)
        file_types = sublime.load_settings(SETTINGS).get("file_types")
        self.config = [c for c in file_types if ".js" in c["extensions"]][0]

    def tearDown(self):
        self.view.close()

    def parse(self, text):
        self.view.run_command("append", {"characters": text})
        command = test_explorer.TestExplorerMenuCommand(self.view)
        return command.parse_test_file(self.config)

    def test_plain_titles(self):
        results = self.parse(
            "describe('math', () => {\n"
            "  it('adds', () => {});\n"
            "});\n"
        )
        self.assertEqual(results, [("math", 1, "group"), ("adds", 2, "test")])

    def test_test_title_with_alternation(self):
        results = self.parse(
            "describe('input', () => {\n"
            "  it('handles (a|b) input', () => {});\n"
            "});\n"
        )
        self.assertIn(("handles (a|b) input", 2, "test"), results)

    def test_group_title_with_regex_characters(self):
        results = self.parse(
            "describe('[a-z]+ (x|y)', () => {\n"
            "  it('works', () => {});\n"
            "});\n"
        )
        self.assertIn(("[a-z]+ (x|y)", 1, "group"), results)

    def test_unbalanced_brackets(self):
        results = self.parse(
            "describe('open [ bracket', () => {\n"
            "  it('open ( paren', () => {});\n"
            "});\n"
        )
        self.assertIn(("open [ bracket", 1, "group"), results)
        self.assertIn(("open ( paren", 2, "test"), results)
