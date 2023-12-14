import os
import re


def replace_pattern_in_file(file_path, pattern, replacement):
    with open(file_path, "r+") as file:
        file_contents = file.read()
        updated_contents = re.sub(pattern, replacement, file_contents)

        file.seek(0)
        file.write(updated_contents)


for root, dirs, files in os.walk(
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "DIPs")
):
    for filename in files:
        if filename.endswith(".md"):
            file_path = os.path.join(root, filename)

            replace_pattern_in_file(
                file_path,
                r"\.\./LICENSE",
                "https://github.com/darwinia-network/DIPs/blob/main/LICENSE",
            )

print("Replacement complete.")
