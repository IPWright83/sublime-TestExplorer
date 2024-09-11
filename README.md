# TestExplorer

TestExplorer is a simple plugin for Sublime Text allowing you to navigation around test files in various different languages

It supports the concept of a group of tests, and then the names of test themselves, allowing you to search or arrow key through different sections with the active view following your current selection.

# Installation

1. Install the Sublime Text Package Control plugin if you don't have it already.
1. Open the command palette and start typing `Package Control: Install Package`.
1. Enter `TestExplorer`

# Demo


# Configuration

The settings allow you to support different syntaxes for different languages that you might be using within Sublime:

```
{
    "file_types": [
        {
            "extensions": [".js", ".jsx", ".ts", ".tsx"],
            "group": {
                "name": "describe",
                "match": "describe\\(\\s*([\\'\"`])(.*?)\\1"
            },
            "test": {
                "name": "it",
                "match": "it\\(\\s*([\\'\"`])(.*?)\\1"
            }
        }
    ]
}
```

You can specify a set of different entries within `file_types` where the set of `extensions` for an entry dictates which rules the plugin should use when searching files.

## Group

The `group` setting represents a logical grouping of tests within your language. For example a typical JavaScript group would look like:

```
describe("a collection of tests", () => {
    ...
});
```

`match`: This should be a Regex pattern (suitable for python) to match the groups in your language
`name`: This is used to present the results in the dropdown

## Test

The `test` setting represents an individual test within your language. For example a typical JavaScript test would look like:

```
it("a single test", () => {
    ...
});
```

`match`: This should be a Regex pattern (suitable for python) to match the tests in your language
`name`: This is used to present the results in the dropdown
