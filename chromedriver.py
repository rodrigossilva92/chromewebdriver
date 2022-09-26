import os
import re
import urllib.request
import xml.etree.ElementTree as ET
from system import OSSystem

class ChromedriverManager:
    CHROME  = "google-chrome"
    PATTERN = r"\d+\.\d+\.\d+\.\d+"

    @classmethod
    def _get_version(cls, program_name:str) -> str:
        version = re.search(ChromedriverManager.PATTERN, program_name)
        version = version.group(0) if version else version
        return version
    
    @classmethod
    def _get_major_version(cls, version:str) -> str:
        try:
            return version.split('.')[0]
        except:
            return

    @staticmethod
    def get_chrome_version() -> str:
        cmd_chrome_mapping = {
            OSSystem.LINUX: "google-chrome --version",
            OSSystem.MAC: r"/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version",
            OSSystem.WINDOWS: ['powershell', '-command', '$(Get-ItemProperty -Path Registry::HKEY_CURRENT_USER\\Software\\Google\\chrome\\BLBeacon).version']
        }
        cmd = cmd_chrome_mapping[OSSystem.get_os_type()]
        output = OSSystem.send_command_terminal(cmd)
        version = ChromedriverManager._get_version(output)
        return version

    @staticmethod
    def get_chromedriver_version(path_chromedriver:str) -> str:
        path_chromedriver = OSSystem.get_absolute_path(path_chromedriver)
        cmd = f"{path_chromedriver} --version"
        output = OSSystem.send_command_terminal(cmd)
        version = ChromedriverManager._get_version(output)
        return version

    @staticmethod
    def verify_chrome_versions_compatibility(path_chromedriver:str) -> bool:
        major_version_chrome = ChromedriverManager._get_major_version(ChromedriverManager.get_chrome_version())
        major_version_chromedriver = ChromedriverManager._get_major_version(ChromedriverManager.get_chromedriver_version(path_chromedriver))
        return major_version_chrome == major_version_chromedriver
    
    @classmethod
    def get_chromedriver_matching_available_version(cls, chrome_major_version:str) -> str:
        response = urllib.request.urlopen('https://chromedriver.storage.googleapis.com').read()
        root = ET.fromstring(response)
        for i in root.iter('{http://doc.s3.amazonaws.com/2006-03-01}Key'):
            if i.text.find(chrome_major_version + '.') == 0:
                return i.text.split('/')[0]

    @staticmethod
    def download_chromedriver(path_save_chromedriver:str) -> None:
        os_url_mapping = {
            "linux": "linux64",
            "win": "win32"
        }
        file_name_mapping = {
            "linux": "chromedriver",
            "win": "chromedriver.exe"
        }
        os_type = os_url_mapping[OSSystem.get_os_type()]
        chrome_version = ChromedriverManager.get_chrome_version()
        chrome_major_version = ChromedriverManager._get_major_version(chrome_version)
        chromedriver_download_version = ChromedriverManager.get_chromedriver_matching_available_version(chrome_major_version)
        url = "https://chromedriver.storage.googleapis.com/" + chromedriver_download_version + '/chromedriver_' + os_type + ".zip"
        file = OSSystem.download_file_from_url(url)
        OSSystem.extract_file(file, path_save_chromedriver) 
        file_name = file_name_mapping[OSSystem.get_os_type()]
        path_chromedriver = os.path.join(path_save_chromedriver, file_name)
        os.chmod(path_chromedriver, 0o744)
            
    @staticmethod
    def manage_chromedriver(path_chromedriver:str) -> None:
        if ChromedriverManager.verify_chrome_versions_compatibility(path_chromedriver):
            return
        if os.path.isfile(path_chromedriver):
            os.remove(path_chromedriver)
            path_save_chromedriver = os.path.dirname(path_chromedriver)
        else:
            path_save_chromedriver = path_chromedriver
        os.makedirs(path_save_chromedriver, exist_ok=True)
        ChromedriverManager.download_chromedriver(path_save_chromedriver)
    

# print(ChromedriverManager.get_chrome_version())
# print(OSSystem.verify_powershell())

ChromedriverManager.download_chromedriver('.')