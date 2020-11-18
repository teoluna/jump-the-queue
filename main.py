from selenium import webdriver
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import requests
import ast
import credentials

class Bot:
    def __init__(self, driver):
        self.driver = driver

    def press_tab(self, sleep_time=1):
        ActionChains(self.driver).send_keys(Keys.TAB).perform()
        sleep(sleep_time)

    def press_shift_tab(self, sleep_time=1):
        ActionChains(self.driver).key_down(Keys.SHIFT).send_keys(Keys.TAB).key_up(Keys.SHIFT).perform()
        sleep(sleep_time)

    def press_enter(self, sleep_time=1):
        ActionChains(self.driver).send_keys(Keys.ENTER).perform()
        sleep(sleep_time)

    def press_arrow_right(self, sleep_time=1):
        ActionChains(self.driver).send_keys(Keys.ARROW_RIGHT).perform()
        sleep(sleep_time)

    def press_arrow_left(self, sleep_time=1):
        ActionChains(self.driver).send_keys(Keys.ARROW_LEFT).perform()
        sleep(sleep_time)

    def press_arrow_down(self, sleep_time=1):
        ActionChains(self.driver).send_keys(Keys.ARROW_DOWN).perform()
        sleep(sleep_time)

    def press_space(self, sleep_time=1):
        ActionChains(self.driver).send_keys(Keys.SPACE).perform()
        sleep(sleep_time)

    def is_calendar_day_available(self, element):
        """
            Check if available (bold font) and if not weekend
        """
        classname = element.get_attribute("class")
        if "text-gray" not in classname:
            # get parent element ./..
            # parent of parent ./../..
            element = element.find_element_by_xpath("./../../..") 
            classname = element.get_attribute("class")
            if "vc-grid-cell-col-7" not in classname and "vc-grid-cell-col-6" not in classname:
                return True

        return False

driver = webdriver.Firefox(executable_path='geckodriver.exe')
driver.get("https://bezkolejki.eu/luw-gorzow/Reservation")
wait = WebDriverWait(driver, 30)
element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "footer-btn")))
driver.maximize_window()

# Send request and check available dates
token = driver.execute_script("return sessionStorage.getItem('token');") # get token
headers = {
    "authority": "bezkolejki.eu", 
    "authorization": f"Bearer {token}",
}

category = 6 # change the number to preferable category

operations = {1:7063, 2:7064, 3:7066, 4:7071, 5:7073, 6:7074}
operation = operations[category]

while True:
    response = requests.get(f'https://bezkolejki.eu/api/Slot/GetAvailableDaysForOperation/{operation}', headers=headers).text # use GET request to webpage with token
    dictionary = ast.literal_eval(response)
    available_days = dictionary['availableDays']
    print("Checking available dates...")
    sleep(1)
    if len(available_days) > 0:
        break

bot = Bot(driver)
bot.press_space()

# Step 1: Choose category   
for i in range(category+4): 
    bot.press_tab(0.1)

bot.press_enter()

for i in range(len(operations)+1-category):
    bot.press_tab(0.1)
bot.press_enter()

# Step 2: Select available date
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
driver.find_element_by_class_name("day-1").click()

initial_calendar_day = driver.switch_to.active_element
element = initial_calendar_day

while not bot.is_calendar_day_available(element):
    bot.press_arrow_right(0.05)
    element = driver.switch_to.active_element

bot.press_enter()
element = wait.until(EC.element_to_be_clickable((By.ID, "selectTime")))
element.click()
bot.press_arrow_down()
bot.press_enter()
bot.press_shift_tab()
bot.press_enter()

# Step 3: Fill in the form
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
bot.press_shift_tab()
ActionChains(driver).send_keys(credentials.email).perform()
bot.press_shift_tab()
ActionChains(driver).send_keys(credentials.surname).perform()
bot.press_shift_tab()
ActionChains(driver).send_keys(credentials.name).perform()
bot.press_tab()
bot.press_tab()
bot.press_tab()
bot.press_enter()

# Step 4: Confirmation
bot.press_shift_tab()
bot.press_space()
bot.press_tab()
bot.press_enter()
