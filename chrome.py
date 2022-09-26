import subprocess
import os
import sys
import platform
import re
import urllib.request
import xml.etree.ElementTree as ET
from io import BytesIO
import zipfile
from typing import Union


class OSType:
    LINUX   = "linux"
    WINDOWS = "win"
    MAC     = "mac"

def get_os_type() -> Union[str,None]:
    os_type = sys.platform
    if os_type == "linux" or os_type == "linux2":
        return OSType.LINUX
    elif os_type == "win32":
        return OSType.WINDOWS
    elif os_type == "darwin":
        return OSType.MAC
    print(f"{os_type} not defined")
    return None

def get_os_architecture() -> Union[int,None]:
    os_architecture = platform.machine()
    if os_architecture.endswith("64"):
        return 64
    elif os_architecture.endswith("32"):
        return 32
    print(f"Architecture {os_architecture} not defined")
    return None

def get_os() -> Union[str,None]:
    os_type = get_os_type()
    os_architecture = get_os_architecture()
    if os_type and os_architecture:
        return f"{os_type}{os_architecture}"
    return None

class ChromeType:
    CHROME      = "google-chrome"
    CHROMIUM    = "chromium"
    BRAVE       = "brave-browser"
    MSEDGE      = "edge"

PATTERN = {
    ChromeType.CHROMIUM: r"\d+\.\d+\.\d+",
    ChromeType.CHROME: r"\d+\.\d+\.\d+",
    ChromeType.MSEDGE: r"\d+\.\d+\.\d+",
    "brave-browser": r"(\d+)",
    "firefox": r"(\d+.\d+)",
}

def get_browser_version(browser_type=None):
    cmd_browser_mapping = {
        ChromeType.CHROME: {
            OSType.LINUX: get_linux_terminal_command(
                "google-chrome",
                "google-chrome-stable",
                "google-chrome-beta",
                "google-chrome-dev",
            ),
            OSType.MAC: r"/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version",
            OSType.WINDOWS: get_windows_terminal_command(
                r'(Get-Item -Path "$env:PROGRAMFILES\Google\Chrome\Application\chrome.exe").VersionInfo.FileVersion',
                r'(Get-Item -Path "$env:PROGRAMFILES (x86)\Google\Chrome\Application\chrome.exe").VersionInfo.FileVersion',
                r'(Get-Item -Path "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe").VersionInfo.FileVersion',
                r'(Get-ItemProperty -Path Registry::"HKCU\SOFTWARE\Google\Chrome\BLBeacon").version',
                r'(Get-ItemProperty -Path Registry::"HKLM\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\Google Chrome").version',
            ),
            },
        ChromeType.CHROMIUM: {
            OSType.LINUX: get_linux_terminal_command("chromium", "chromium-browser"),
            OSType.MAC: r"/Applications/Chromium.app/Contents/MacOS/Chromium --version",
            OSType.WINDOWS: get_windows_terminal_command(
                r'(Get-Item -Path "$env:PROGRAMFILES\Chromium\Application\chrome.exe").VersionInfo.FileVersion',
                r'(Get-Item -Path "$env:PROGRAMFILES (x86)\Chromium\Application\chrome.exe").VersionInfo.FileVersion',
                r'(Get-Item -Path "$env:LOCALAPPDATA\Chromium\Application\chrome.exe").VersionInfo.FileVersion',
                r'(Get-ItemProperty -Path Registry::"HKCU\SOFTWARE\Chromium\BLBeacon").version',
                r'(Get-ItemProperty -Path Registry::"HKLM\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\Chromium").version',
            ),
        }
    }
    try:
        cmd = cmd_browser_mapping[browser_type][get_os_type()]
        pattern = PATTERN[browser_type]
        version = read_version_from_terminal(cmd, pattern)
        return version
    except Exception:
        raise Exception(f"{browser_type} not found in the system")

def get_linux_terminal_command(*apps:str) -> str:
    return " || ".join(f"{i} --version" for i in apps)

def get_windows_terminal_command(*apps:str) -> str:
    shell = verify_powershell()
    first_hit_attempt = "$tmp = {expression}; if ($tmp) {{echo $tmp; Exit;}};"
    script = "$ErrorActionPreference='silentlycontinue'; " + \
                " ".join(first_hit_attempt.format(expression=i) for i in apps)
    return f"{shell} -NoProfile '{script}'"

def verify_powershell() -> str:
    cmd = "(dir 2>&1 *`|echo CMD);&<# rem #>echo powershell"
    with subprocess.Popen(cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.DEVNULL,
                        stdin=subprocess.DEVNULL,
                        shell=True
    ) as stream:
        stdout = stream.communicate()[0].decode()
    return "" if stdout == "powershell" else "powershell"

def read_version_from_terminal(cmd, pattern):
    with subprocess.Popen(cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.DEVNULL,
                        stdin=subprocess.DEVNULL,
                        shell=True
    ) as stream:
        stdout = stream.communicate()[0].decode()
        version = re.search(pattern, stdout)
        version = version.group(0) if version else None
    return version


# print(get_browser_version("google-chrome"))


def get_chromedriver_version(path_chromedriver:str) -> Union[str,None]:
    # try:
    # cmd_run = subprocess.run(f"{path_chromedriver} --version",
    #                             capture_output=True,
    #                             text=True)
    # except:
    #     print("No chromedriver.exe found in specified path\n")
    #     return None
    # print(cmd_run)
    cmd = f"{path_chromedriver} --version"
    with subprocess.Popen(cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.DEVNULL,
                        stdin=subprocess.DEVNULL,
                        shell=True
    ) as stream:
        stdout = stream.communicate()[0].decode()
    return stdout

def get_available_chromedriver_version(major_version:str) -> str:
    doc = urllib.request.urlopen('https://chromedriver.storage.googleapis.com').read()
    root = ET.fromstring(doc)
    for i in root.iter('{http://doc.s3.amazonaws.com/2006-03-01}Key'):
        if i.text.find(major_version + '.') == 0:
            return  i.text.split('/')[0]

def download_chromedriver_file(os_type, version, path):
    if os_type == "win":
        os_type = "win32"
    elif os_type == "linux":
        os_type = "linux64"
    url = "https://chromedriver.storage.googleapis.com/" + version + '/chromedriver_' + os_type + ".zip"
    response = urllib.request.urlopen(url)
    archive = BytesIO(response.read())
    with zipfile.ZipFile(archive, 'r') as zip_file:
        zip_file.extractall(path)
    
# version=get_available_chromedriver_version('105')
# print(version)
# download_chromedriver_file('linux', version, '.')

print(get_chromedriver_version('chromedriver'))
path_cwd = os.getcwd()

path_chromedriver = os.path.join(path_cwd, 'chromedriver')
print(path_chromedriver)
os.chmod(path_chromedriver, 0o744)
print(get_chromedriver_version(path_chromedriver))
