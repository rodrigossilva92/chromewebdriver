from selenium.webdriver import Chrome
import os

path_cwd = os.getcwd()

path_chromedriver = os.path.join(path_cwd, 'chromedriver')

driver = Chrome(executable_path=path_chromedriver)

print(driver.capabilities['browserVersion'])
print(driver.capabilities['chrome']['chromedriverVersion'])

input()



driver.quit()



# def linux_browser_apps_to_cmd(*apps:str) -> str:
#     """Create 'browser --version' command from browser app names.

#     Result command example:
#         chromium --version || chromium-browser --version
#     """
#     ignore_errors_cmd_part = " 2>/dev/null" if os.getenv(
#         "WDM_LOG_LEVEL") == "0" else ""
#     return " || ".join(f"{i} --version{ignore_errors_cmd_part}" for i in apps)

# print(linux_browser_apps_to_cmd(
#                 "google-chrome",
#                 "google-chrome-stable",
#                 "google-chrome-beta",
#                 "google-chrome-dev",
#             ))

# import subprocess
# import re
# def read_version_from_cmd(cmd, pattern):
#     with subprocess.Popen(
#             cmd,
#             stdout=subprocess.PIPE,
#             stderr=subprocess.DEVNULL,
#             stdin=subprocess.DEVNULL,
#             shell=True,
#     ) as stream:
#         stdout = stream.communicate()[0].decode()
#         version = re.search(pattern, stdout)
#         version = version.group(0) if version else None
#     return version