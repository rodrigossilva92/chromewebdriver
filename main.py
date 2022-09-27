

from scripts.chromedriver import Chromedriver
from scripts.config import PATH_CHROMEDRIVER

driver = Chromedriver(path_chromedriver=PATH_CHROMEDRIVER)
driver.driver.get("https://www.google.com/")
input()

# import os
# print(os.path.isfile("assets/chromedriver/chromedriver"))
# print(os.path.dirname("/home/rodrigo/Development/Codes/teste/assets/chromedriver/chromedriver"))

# os.remove("assets/chromedriver/chromedriver")