
import re
from playwright.sync_api import Page, expect, sync_playwright
from fit_file_decoder import FitFileDecoder
from collections import defaultdict

# with sync_playwright() as p:
#     browser = p.chromium.launch(headless=False,  args=["--start-maximized"])
#     context = browser.new_context(
#         user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
#     )
#     page = context.new_page()
#     page.goto("https://connect.garmin.com/signin/")
#     page.wait_for_load_state("networkidle")
#     inputs = page.query_selector_all("input")
#     page.fill('input[name="email"]', 'kamilmatuszewski95@gmail.com')
#     page.fill('input[name="password"]', 'y@yhVch0gn#020')
#     time.sleep(0.5)
#     page.click('button.g__button--contained--ocean-blue')
#     page.pause()
#     page.screenshot(path="screenshot.png")
#     browser.close()


if __name__ == "__main__":
    paces = defaultdict(list)
    kupa = FitFileDecoder(r"C:\Users\Pan Mirek\Downloads\FitSDKRelease_21.158.00\java\16770612681_ACTIVITY.fit")
    kupa.define_records("heart_rate", "enhanced_speed", "timestamp")
    kupa.define_hr_limits(120, 151)
    pace = kupa.calculate_average_pace()
    key, value = next(iter(pace.items()))
    paces[key] = value






