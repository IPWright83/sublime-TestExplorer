import sublime
import sublime_plugin
import re

class TestExplorerMenuCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # Grab the current file name
        file_name = self.view.file_name()
        if not file_name:
            return None

        # Grab the appropriate config for the file
        config = self.get_config_for_file(file_name)
        if not config:
            return None

        # Parse the current view to extract out describe and it blocks
        test_names = self.parse_test_file(config)

        # Generate test menu sub-tree
        test_menu = self.generate_test_menu(test_names, config)

        # Display the test menu
        self.window().show_quick_panel(test_menu, self.on_done, 0, -1, self.on_done)

    def filter_empty(value): 
        if (value):
            return True
        return False

    def get_config_for_file(self, file_name):
        settings = sublime.load_settings("TestExplorer.sublime-settings")
        
        for fileGroup in settings.get('file_types', []):
            for extension in fileGroup.get('extensions', []):
                if file_name.endswith(extension):
                    return fileGroup;

        return None

    def parse_test_file(self, config):
        group = config.get('group')
        test = config.get('test')

        group_rgx = re.compile(group.get('match'))
        test_rgx = re.compile(test.get('match'))

        content = self.view.substr(sublime.Region(0, self.view.size()))

        group_blocks = group_rgx.findall(content)
        test_blocks = test_rgx.findall(content)
        results = []

        ## Find line numbers
        for block in group_blocks:
            description = next((item for item in block if item), None)  # Get the first non-empty string
            if description:
                region = self.view.find(r'\b{}\b'.format(re.escape(description)), 0)
                if region:
                    line_number, _ = self.view.rowcol(region.begin())
                    results.append((description, line_number + 1, 'group'))

        ## Find line numbers
        for block in test_blocks:
            it = next((item for item in block if item), None)
            if it:
                region = self.view.find(r'\b{}\b'.format(re.escape(it)), 0)
                if region:
                    line_number, _ = self.view.rowcol(region.begin())
                    results.append((it, line_number + 1, 'test'))

        return results

    def generate_test_menu(self, test_names, config):
        group = config.get('group')
        test = config.get('test')
        test_menu = []

        self.sorted_names = sorted(test_names, key=lambda x:x[1])
        max_description_width = max(len(block[0]) for block in self.sorted_names) + 4

        for match in self.sorted_names:
            if match[2] == "group":
                name = match[0]
                item = "{}: {}".format(group.get('name'), match[0])
                test_menu.append(item)
            else:
                name = match[0]
                item = "      {}: {}".format(test.get('name'), match[0])
                test_menu.append(item)

        return test_menu

    def on_done(self, index):
        if index != -1:
            item = self.sorted_names[index]
            if item != None:
                line_number = item[1];
                self.view.run_command("goto_line", {"line": line_number})
                pass

    def window(self):
        return self.view.window()
