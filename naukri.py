from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from datetime import  datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os
import sys

# Load environment variables
load_dotenv()
os.makedirs("screenshots", exist_ok=True)

# Configuration

RESUME_PATH=os.getenv("RESUME_PATH")
NAUKRI_EMAIL = os.getenv("NAUKRI_EMAIL")
NAUKRI_PASSWORD = os.getenv("NAUKRI_PASSWORD")
print("email is",NAUKRI_EMAIL)
print("Password loaded",NAUKRI_PASSWORD is not None)

def log(msg): 
    with open("automation.log", "a") as f:
        f.write(f"{datetime.now()} - {msg}\n")

def update_naukri_profile():
    """Main function to update Naukri profile"""
    
    # Verify resume file exists
    if not os.path.exists(RESUME_PATH):
        print(f"Error: Resume file not found at {RESUME_PATH}")
        return
    
    log("Initializing Browser")
    
    chrome_options = Options()
    
    
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    driver = None
    
    try:
        # Initialize driver
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        
        driver.maximize_window()
        log("Browser Opened Successfully")
        
        # Open Naukri
        driver.get("https://www.naukri.com/")
        log("Navigated to Naukri.com")
        time.sleep(3)
        
        # Check if already logged in, if not, perform login
        try:
            # Look for login button
            login_button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, "login_Layer"))
            )
            log("Not logged in. Attempting to login...")
            
            # Click login button
            login_button.click()
            time.sleep(2)
            
            # Enter email
            email_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter your active Email ID / Username']"))
            )
            email_field.clear()
            email_field.send_keys(NAUKRI_EMAIL)
            time.sleep(1)
            
            # Enter password
            password_field = driver.find_element(By.XPATH, "//input[@placeholder='Enter your password']")
            password_field.clear()
            password_field.send_keys(NAUKRI_PASSWORD)
            time.sleep(1)
            
            # Click login submit button
            login_submit = driver.find_element(By.XPATH, "//button[@type='submit' and text()='Login']")
            login_submit.click()
            log("Login credentials submitted.")
            time.sleep(5)
            
        except:
            print("Already logged in or login element not found.")
        
        # Navigate to profile/resume section
        log("Navigating to profile section...")
        
        # Click on "View Profile" or navigate directly to profile update page
        try:
            # Try clicking on profile/view profile
            view_profile = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[@href='/mnjuser/profile']"))
            )
            view_profile.click()
            log("Clicked on View Profile")
            time.sleep(3)
        except:
            # Alternative: Direct navigation
            driver.get("https://www.naukri.com/mnjuser/profile")
            log("Navigated directly to profile page")
            time.sleep(3)
        
        # Click on "Update Resume" button
        log("Looking for Update Resume button...")
        try:
            # # Method 1: By text
            # update_resume_btn = WebDriverWait(driver, 10).until(
            #     EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Update resume')]"))
            # )
            # update_resume_btn.click()
            update_resume_btn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Update resume']")))
            update_resume_btn.click()
        except:
            try:
                # Method 2: By class or alternative xpath
                update_resume_btn = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[@class='resumeSection']//button"))
                )
                update_resume_btn.click()
            except:
                # Method 3: Click on edit icon near resume
                update_resume_btn = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[@class='icon edit']"))
                )
                update_resume_btn.click()
        
        log("Clicked on Update Resume button")
        time.sleep(2)
        
        # Upload resume file
        log("Uploading resume...")
        
        # Find file input element
        file_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
        )
        
        # Send file path to input
        file_input.send_keys(RESUME_PATH)
        log(f"Resume file selected: {RESUME_PATH}")
        time.sleep(3)
        
        # Click Save/Upload button
        try:
            save_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Save') or contains(text(), 'Upload')]"))
            )
            save_button.click()
            log("Clicked Save/Upload button")
            time.sleep(5)
        except:
            log("Save button not found or resume auto-uploaded")
        
        # Verify success
        try:
            success_message = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'successfully') or contains(text(), 'updated')]"))
            )
            log("✓ Profile updated successfully!")
        except:
            log("Success message not found, but resume likely uploaded")
        
        time.sleep(3)
        
        # Logout (optional)
        try:
            log("Logging out...")
            # Click on profile dropdown
            profile_dropdown = driver.find_element(By.XPATH, "//div[@class='nI-gNb-drawer__icon']")
            profile_dropdown.click()
            time.sleep(1)
            
            # Click logout
            logout_btn = driver.find_element(By.XPATH, "//a[contains(text(), 'Logout')]")
            logout_btn.click()
            log("Logged out successfully")
            time.sleep(2)
        except:
            log("Logout not performed (optional step)")
        
        log("Automation completed successfully!")
        
    # except Exception as e:
    #     log(f"An error occurred: {str(e)}")
    #     # Take screenshot for debugging
    #     try:
    #         if driver:
    #             driver.save_screenshot("error_screenshot.png")
    #             log("Error screenshot saved as 'error_screenshot.png'")
    #     except:
    #
    # except Exception as e:
    except Exception as e:

        log(f"ERROR: {str(e)}")

        print(f"An error occurred: {str(e)}")

    try:
        if driver:

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            screenshot_name = f"error_{timestamp}.png"

            driver.save_screenshot(screenshot_name)

            log(f"Screenshot saved: {screenshot_name}")

            print(f"Screenshot saved: {screenshot_name}")

    except Exception as screenshot_error:

        log(f"Screenshot Error: {str(screenshot_error)}")
        pass
    
    finally:
        # Close browser
        if driver:
            log("Closing browser...")
            time.sleep(2)
            driver.quit()
            log("Browser closed.")
            sys.exit(0)
            

# Main execution
if __name__ == "__main__":
    print("=" * 50)
    print("Naukri Profile Auto-Update Script")
    print("=" * 50)
    
    # Run the automation immediately
    update_naukri_profile()
    
    print("=" * 50)
    log("Script execution completed!")
    print("=" * 50)