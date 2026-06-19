# Naukri Profile Auto Updater

## Project Overview

Naukri Profile Auto Updater is a Python-based Selenium automation project designed to automatically update a user's Naukri profile by uploading the latest resume. The solution can be scheduled using Windows Task Scheduler to keep the profile active and regularly updated without manual intervention.

The project follows automation best practices including secure credential management, logging, exception handling, and failure screenshot capture.

---

## Features

* Automated login to Naukri
* Automatic resume upload and profile update
* Secure credential management using environment variables (`.env`)
* Explicit waits for stable element synchronization
* Detailed execution logging
* Automatic screenshot capture on failures
* Windows Task Scheduler integration
* Graceful exception handling and browser cleanup

---

## Tech Stack

| Technology             | Purpose                         |
| ---------------------- | ------------------------------- |
| Python                 | Automation scripting            |
| Selenium WebDriver     | Browser automation              |
| ChromeDriver           | Chrome browser control          |
| python-dotenv          | Environment variable management |
| Windows Task Scheduler | Scheduled execution             |
| Git & GitHub           | Version control                 |

---

## Project Structure

```text
naukri_profile_update/
│
├── naukri.py
├── .env
├── .gitignore
├── automation.log
├── screenshots/
└── README.md
```

---

## Configuration

Create a `.env` file in the project root directory:

```env
NAUKRI_EMAIL=your_email
NAUKRI_PASSWORD=your_password
RESUME_PATH=D:\path\to\resume.pdf
```

> Sensitive information is excluded from version control using `.gitignore`.

---

## Execution

Run the automation manually:

```bash
python naukri.py
```

Or configure the script in Windows Task Scheduler for automated daily execution.

---

## Logging & Error Handling

The project maintains execution logs in:

```text
automation.log
```

In case of failures:

* Error details are logged
* A screenshot is captured automatically
* Browser sessions are terminated safely
* Script exits gracefully

---

## Key Automation Concepts Implemented

* Selenium WebDriver
* XPath Locators
* Explicit Waits (`WebDriverWait`)
* Environment Variables
* Exception Handling
* File Upload Automation
* Logging
* Screenshot Capture
* Task Scheduling

---

## Future Enhancements

* Email notifications after execution
* OTP detection and handling
* Page Object Model (POM)
* TestNG/Java implementation
* Jenkins integration
* HTML reporting

---

## Author

**Abhishek**

QA Automation Enthusiast | Python | Selenium | Java | SQL
