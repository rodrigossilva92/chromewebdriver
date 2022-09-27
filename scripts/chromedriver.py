from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import WebDriverException
from scripts.chromedriver_manager import ChromedriverManager

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

        if self.__path_chromedriver is None:
            self.__path_chromedriver = ChromedriverManager.download_chromedriver(Chromedriver.PATH_SAVE_CHROMEDRIVER)
        
        chrome_service = ChromeService(executable_path=self.__path_chromedriver)
        chrome_options = ChromeOptions()

        try:
            self.driver = Chrome(service=chrome_service, options=chrome_options)
        except WebDriverException:
            try:
                ChromedriverManager.manage_chromedriver(self.__path_chromedriver)
                self.driver = Chrome(service=chrome_service, options=chrome_options)
            except Exception as e:
                print(e)
        except Exception as e:
            print(e)
