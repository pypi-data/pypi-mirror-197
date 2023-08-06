import glob
import os
import pathlib
import fnmatch


def find_gitignore(start_dir):
    current_dir = pathlib.Path(start_dir).resolve()
    while current_dir != current_dir.parent:
        gitignore_path = current_dir / ".gitignore"
        if gitignore_path.is_file():
            return gitignore_path
        current_dir = current_dir.parent
    return None


def gitignore_matcher(path, gitignore_path):
    if gitignore_path:
        with open(gitignore_path, "r") as gitignore_file:
            patterns = gitignore_file.readlines()
        for pattern in patterns:
            pattern = pattern.strip()
            if not pattern or pattern.startswith("#"):
                continue
            if fnmatch.fnmatch(path, pattern):
                return True
    return False


def get_file_paths(directory, gitignore_path):
    file_paths = []
    for root, directories, files in os.walk(directory):
        directories[:] = [
            dir for dir in directories if not gitignore_matcher(dir, gitignore_path)
        ]
        for filename in files:
            file_path = os.path.join(root, filename)
            file_paths.append(file_path)
    return file_paths


def take_snapshot(*paths: str, filenames_only=False):
    all_files = set()
    for path in paths:
        for _path in glob.glob(path):
            if os.path.isfile(_path):
                all_files.add(_path)
            elif os.path.isdir(_path):
                gitignore_path = find_gitignore(_path)
                for file in get_file_paths(_path, gitignore_path):
                    if gitignore_matcher(file, gitignore_path):
                        continue
                    all_files.add(file)

    result = []
    for file in all_files:
        if filenames_only:
            result.append(file)
        else:
            with open(file, "r") as f:
                content = f.read()
            result.append(f"{file}\n```\n{content}\n```")

    return all_files, "\n".join(result)
