from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

chrome_options = Options()

# Replace with your Windows username
chrome_options.add_argument(
    r"--user-data-dir=C:\Users\DELL\AppData\Local\Google\Chrome\User Data"
)

# Usually "Default"
chrome_options.add_argument("--profile-directory=Default")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options
)

driver.maximize_window()

# Open Naukri
driver.get("https://www.naukri.com/")

print("Naukri opened successfully.")

# Wait so you can verify login status
time.sleep(20)

driver.quit()