
import re
import time
from playwright.sync_api import Page, expect, sync_playwright
from fit_file_decoder import FitFileDecoder
from collections import defaultdict


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time


if __name__ == "__main__":
    paces = defaultdict(list)
    kupa = FitFileDecoder(r"C:\Users\Pan Mirek\Downloads\13_DOZ_Maraton.fit")
    kupa.define_records("heart_rate", "enhanced_speed", "timestamp")
    kupa.define_hr_limits(120, 151)
    pace = kupa.calculate_average_pace()
    key, value = next(iter(pace.items()))
    paces[key] = value






