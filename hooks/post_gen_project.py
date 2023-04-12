import json
import os
import shutil

from path import Path
cloud = "Azure"
project_slug = "{{cookiecutter.project_slug}}"
project_name = "{{cookiecutter.project_name}}"
environment = "default"
profile = "{{cookiecutter.profile}}"
workspace_dir = "{{cookiecutter.workspace_dir}}"
artifact_location = "{{cookiecutter.artifact_location}}"

PROJECT_FILE_CONTENT = {
    "environments": {
        environment: {
            "profile": profile,
            "workspace_dir": workspace_dir,
            "artifact_location": artifact_location,
        },
        "staging": {
           "profile": "DEFAULT",
           "workspace_dir": workspace_dir,
           "artifact_location": artifact_location,
        },
        "production": {
            "profile": "DEFAULT",
            "workspace_dir": workspace_dir,
            "artifact_location": artifact_location,
        }
    }
}


def replace_vars(file_path: str):
    _path = Path(file_path)
    content = _path.read_text().format(
        project_name=project_name, environment=environment, profile=profile
    )
    _path.write_text(content)


class PostProcessor:
    @staticmethod
    def process():

        project_file = Path(".dbx/project.json")
        if not project_file.parent.exists():
            project_file.parent.mkdir()
        project_file.write_text(json.dumps(PROJECT_FILE_CONTENT, indent=2))
        Path(".dbx/lock.json").write_text("{}")
        os.system("git init")


if __name__ == "__main__":
    post_processor = PostProcessor()
    post_processor.process()
