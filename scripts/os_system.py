from typing import Union
import os
import sys
import platform
import subprocess
import zipfile
from io import BytesIO
import urllib.request

class OSSystem:
    LINUX   = "linux"
    WINDOWS = "win"
    MAC     = "mac"

    @staticmethod
    def get_os_type() -> Union[str,None]:
        os_type = sys.platform
        if os_type == "linux" or os_type == "linux2":
            return OSSystem.LINUX
        elif os_type == "win32":
            return OSSystem.WINDOWS
        elif os_type == "darwin":
            return OSSystem.MAC
        print(f"{os_type} not defined")
        return None
    
    @staticmethod
    def get_os_architecture() -> Union[str,None]:
        os_architecture = platform.machine()
        if os_architecture.endswith("64"):
            return 64
        elif os_architecture.endswith("32"):
            return 32
        print(f"Architecture {os_architecture} not defined")
        return None

    @staticmethod
    def get_os_definition() -> Union[str,None]:
        os_type = OSSystem.get_os_type()
        os_architecture = OSSystem.get_os_architecture()
        if os_type and os_architecture:
            return f"{os_type}{os_architecture}"
        return None
    
    @staticmethod
    def get_absolute_path(path:str) -> Union[str,None]:
        if os.path.exists(path):
            return os.path.abspath(path)
    
    @staticmethod
    def send_command_terminal(cmd:str) -> str:
        with subprocess.Popen(cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL,
                    stdin=subprocess.DEVNULL,
                    shell=True
        ) as stream:
            stdout = stream.communicate()[0].decode()
        return stdout
    
    @staticmethod
    def download_file_from_url(url:str) -> BytesIO:
        response = urllib.request.urlopen(url)
        return BytesIO(response.read())
    
    @staticmethod
    def extract_file(file:BytesIO, path:str) -> None:
        with zipfile.ZipFile(file, 'r') as zip_file:
            zip_file.extractall(path, )
