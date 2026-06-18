from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os
import sys

# Load environment variables
load_dotenv()

# Configuration
RESUME_PATH = r"D:\abhi\Abhishek_Resume.pdf"  # Update this with your resume path
NAUKRI_EMAIL = os.getenv("NAUKRI_EMAIL")
NAUKRI_PASSWORD = os.getenv("NAUKRI_PASSWORD")
print("email is",NAUKRI_EMAIL)
print("Password loaded",NAUKRI_PASSWORD is not None)

def update_naukri_profile():
    """Main function to update Naukri profile"""
    
    # Verify resume file exists
    if not os.path.exists(RESUME_PATH):
        print(f"Error: Resume file not found at {RESUME_PATH}")
        return
    
    print("Initializing browser...")
    
    chrome_options = Options()
    
    # IMPORTANT: Close all Chrome windows before running the script
    # Comment out these lines if you want to login manually each time
    # chrome_options.add_argument(
    #     r"--user-data-dir=C:\Users\DELL\AppData\Local\Google\Chrome\User Data"
    # )
    # chrome_options.add_argument("--profile-directory=Profile 1")
    
    # Additional options for stability
    
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
        print("Browser opened successfully.")
        
        # Open Naukri
        driver.get("https://www.naukri.com/")
        print("Navigated to Naukri.com")
        time.sleep(3)
        
        # Check if already logged in, if not, perform login
        try:
            # Look for login button
            login_button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, "login_Layer"))
            )
            print("Not logged in. Attempting to login...")
            
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
            print("Login credentials submitted.")
            time.sleep(5)
            
        except:
            print("Already logged in or login element not found.")
        
        # Navigate to profile/resume section
        print("Navigating to profile section...")
        
        # Click on "View Profile" or navigate directly to profile update page
        try:
            # Try clicking on profile/view profile
            view_profile = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[@href='/mnjuser/profile']"))
            )
            view_profile.click()
            print("Clicked on View Profile")
            time.sleep(3)
        except:
            # Alternative: Direct navigation
            driver.get("https://www.naukri.com/mnjuser/profile")
            print("Navigated directly to profile page")
            time.sleep(3)
        
        # Click on "Update Resume" button
        print("Looking for Update Resume button...")
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
        
        print("Clicked on Update Resume button")
        time.sleep(2)
        
        # Upload resume file
        print("Uploading resume...")
        
        # Find file input element
        file_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
        )
        
        # Send file path to input
        file_input.send_keys(RESUME_PATH)
        print(f"Resume file selected: {RESUME_PATH}")
        time.sleep(3)
        
        # Click Save/Upload button
        try:
            save_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Save') or contains(text(), 'Upload')]"))
            )
            save_button.click()
            print("Clicked Save/Upload button")
            time.sleep(5)
        except:
            print("Save button not found or resume auto-uploaded")
        
        # Verify success
        try:
            success_message = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'successfully') or contains(text(), 'updated')]"))
            )
            print("✓ Profile updated successfully!")
        except:
            print("Success message not found, but resume likely uploaded")
        
        time.sleep(3)
        
        # Logout (optional)
        try:
            print("Logging out...")
            # Click on profile dropdown
            profile_dropdown = driver.find_element(By.XPATH, "//div[@class='nI-gNb-drawer__icon']")
            profile_dropdown.click()
            time.sleep(1)
            
            # Click logout
            logout_btn = driver.find_element(By.XPATH, "//a[contains(text(), 'Logout')]")
            logout_btn.click()
            print("Logged out successfully")
            time.sleep(2)
        except:
            print("Logout not performed (optional step)")
        
        print("Automation completed successfully!")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        # Take screenshot for debugging
        try:
            if driver:
                driver.save_screenshot("error_screenshot.png")
                print("Error screenshot saved as 'error_screenshot.png'")
        except:
            pass
    
    finally:
        # Close browser
        if driver:
            print("Closing browser...")
            time.sleep(2)
            driver.quit()
            sys.exit(0)
            print("Browser closed.")

# Main execution
if __name__ == "__main__":
    print("=" * 50)
    print("Naukri Profile Auto-Update Script")
    print("=" * 50)
    
    # Run the automation immediately
    update_naukri_profile()
    
    print("=" * 50)
    print("Script execution completed!")
    print("=" * 50)