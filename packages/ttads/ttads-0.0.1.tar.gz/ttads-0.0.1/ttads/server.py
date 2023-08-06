import argparse
import threading
import zipfile
from io import BytesIO
from pathlib import Path
from time import sleep

from flask import Flask, send_file

from tunnel import Tunnel


class TappServer:

    def __init__(self, path='.'):
        self.path = Path(path).absolute()
        self.paths_projects = [
            path for path in self.path.iterdir()
            if path.is_dir() and not path.stem.startswith('.') and (path / 'module').exists()
        ]

        if not self.paths_projects:
            raise ValueError(f'No projects found in path: "{self.path}"')

        self.names_projects = {path.name for path in self.paths_projects}
        self.app = Flask(self.__class__.__name__)

        self.app.route('/<name_project>')(self.serve_tapp)
        self.thread = threading.Thread(target=self.start_app)
        self.start()

    def start(self):
        self.thread.start()

    def start_app(self):
        self.app.run(port=80)

    def close(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.close()

    def wait(self):
        while self.thread.is_alive():
            sleep(1)

    def serve_tapp(self, name_project):

        name_project = Path(name_project).stem
        if name_project not in self.names_projects:
            raise ValueError(f'Unknown project "{name_project}"')

        path_project = self.path / name_project
        path_tapp = Path(path_project.stem).with_suffix('.tapp')
        path_module = path_project / Path('module')
        path_autoexec = path_project / Path('autoexec.be')

        byte_buffer = BytesIO()
        with zipfile.ZipFile(byte_buffer, mode='w') as zip_file:
            zip_file.write(path_autoexec, arcname=path_autoexec.name)
            for file_path in path_module.iterdir():
                if file_path.is_file():
                    zip_file.write(file_path, arcname=file_path.name)

        byte_buffer.seek(0)

        response = send_file(byte_buffer, as_attachment=True, download_name=str(path_tapp))
        return response


def start(path):
    # paths_projects=[path for path in PATH_PROJECTS.iterdir() if path.is_dir() and not path.stem.startswith('.') and (path/'module').exists()]

    with TappServer(path) as tapp_server:
        with Tunnel() as tunnel:
            for name_project in tapp_server.names_projects:
                print(
                    f'Serving project "{name_project}": `tasmota.urlfetch("{tunnel.tunnel.public_url}/{name_project}.tapp")`')
            tapp_server.wait()
            # berry_expression=f'`tasmota.urlfetch("{tunnel.tunnel.public_url}/") tasmota.cmd("restart 1")`'
            # print(f"""It's now running. You can download your .tapp to you device using {berry_expression} at the Berry console.\nIntrospection URL: {tunnel.tunnel.api_url}""")


def start_cli():
    parser = argparse.ArgumentParser(description=TappServer.__name__)
    parser.add_argument('path', type=str, help='Path to projects directory', default='.', nargs='?')
    args = parser.parse_args()
    start(path=args.path)


if __name__ == '__main__':
    start_cli()
