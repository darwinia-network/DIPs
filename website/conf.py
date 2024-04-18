project = "dips"
copyright = "2023, Darwinia Network"
author = "Darwinia Network"

extensions = ["myst_parser"]

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_title = "Darwinia Improvement Proposals"
html_logo = "../logo.svg"
html_theme = "furo"
html_static_path = ["_static"]
html_css_files = [
    "custom.css",
]
html_theme_options = {
    "navigation_with_keys": True,
    "sidebar_hide_name": True,
}
