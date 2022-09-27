from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from scripts.libs.chromedriver_manager import ChromedriverManager

class Chromedriver:
    PATH_SAVE_CHROMEDRIVER = "assets"

    def __init__(self, path_chromedriver:str=None, headless:bool=False) -> None:        
        self.__path_chromedriver = path_chromedriver
        self.__headless = headless
        self.__start_driver()

    def __del__(self) -> None:
        try:
            self.driver.quit()
        except:
            pass

    def __start_driver(self) -> bool:       
        self.__path_chromedriver = ChromedriverManager.manage_chromedriver(self.__path_chromedriver)
        chrome_service = ChromeService(executable_path=self.__path_chromedriver)
        chrome_options = ChromeOptions()

        if self.__headless:
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--window-size=1920x1080")
        else:
            chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-extensions")
        
        self.driver = Chrome(service=chrome_service, options=chrome_options)

