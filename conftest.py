import pytest
import pytest_html
import os
from selenium import webdriver


# Function to capture screenshot
def capture_screenshot():
    driver = webdriver.Chrome()  # Use the appropriate driver for your browser
    screenshot_path = os.path.join(os.path.expanduser("~"), "Desktop", "screenshot.png")
    driver.save_screenshot(screenshot_path)
    driver.quit()
    return screenshot_path


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    extras = getattr(report, "extras", [])

    if report.when == "call":
        # always add url to report
        extras.append(pytest_html.extras.url("http://www.example.com/"))
        xfail = hasattr(report, "wasxfail")

        if (report.skipped and xfail) or (report.failed and not xfail):
            # Capture screenshot on failure
            screenshot_path = capture_screenshot()
            if os.path.exists(screenshot_path):
                # Attach the screenshot as an image in the HTML report
                extras.append(pytest_html.extras.image(screenshot_path))

        report.extras = extras
