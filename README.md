# AIOdriver

All-in-one WebDriver helper for Windows with automatic driver download/update support for Chrome (stable and chrome-for-testing) and Edge. Designed to simplify creating Selenium WebDriver instances including profiles, mobile emulation, selenium-wire, and undetected_chromedriver usage.

## Installation

Install from GitHub:
```bash
pip install git+https://github.com/abhishake99/AIOdriver.git
```

## Requirements / Notes

- This project targets Windows (registry-based browser detection and default paths).
- Python packages used: selenium, requests, selenium-wire (optional, for crawler_type 'bh'/'rr'), undetected-chromedriver (optional, driver_type 'uc').
- The library manages Chrome/Edge driver downloads into folders under C:\ (e.g. C:\new_chrome, C:\latest_chrome_driver, C:\new_edge).

## Key functions

- createwebdriver(driver, crawler_type='osa', driver_type='chrome', username='Administrator', profile_directory='Default', use_old_chrome=False)

Parameters summary:
- driver: existing driver instance (will be closed if present for some flows).
- crawler_type: 'osa' (default) or 'bh' / 'rr' — when 'bh'/'rr' the function creates a selenium-wire Chrome instance using chrome-for-testing.
- driver_type: one of:
  - "chrome" — launches Chrome using chrome-for-testing (auto-download to C:\new_chrome\extract). Set use_old_chrome=True to use C:\old_chrome.
  - "edge" — detects Edge version and auto-downloads matching msedgedriver to C:\new_edge\extract.
  - "profile" — launches Chrome using a local user profile (username, profile_directory).
  - "mobile" — launches Chrome with mobile emulation settings.
  - "uc" — launches undetected_chromedriver.
  - "chrome_old" — ensures old testing Chrome is downloaded (C:\old_chrome).
  - "cdrive" — copies chromedriver to C:\latest_chrome_driver and launches Chrome from that driver.

Examples

Chrome (default, uses chrome-for-testing):
```python
from AIOdriver.functions import createwebdriver
driver = createwebdriver('', driver_type="chrome")
```

Edge:
```python
from AIOdriver.functions import createwebdriver
driver = createwebdriver('', driver_type="edge")
```

Profile (use an existing Windows Chrome profile):
```python
driver = createwebdriver('', driver_type="profile", username='Administrator', profile_directory='Default')
```

Mobile emulation:
```python
driver = createwebdriver('', driver_type="mobile")
```

Selenium-wire (crawler_type 'bh' or 'rr'):
```python
driver = createwebdriver('', driver_type="chrome", crawler_type="bh")
```

Undetected Chrome:
```python
driver = createwebdriver('', driver_type="uc")
```

Use old chrome-for-testing artifacts:
```python
driver = createwebdriver('', driver_type="chrome", use_old_chrome=True)
```

## Utility functions (exposed in functions.py)
- get_chrome_version(), get_chromedriver_url(...), download_chromedriver(...), c_driver_chromedriver() — helpers to detect and install ChromeDriver.
- download_chromedriver_testing_new(), download_chromedriver_testing_old() — manage chrome-for-testing downloads.
- get_edge_version(), get_edgedriver_version(...), download_and_extract_edgedriver(...) — Edge driver helpers.
- driver_initialisation_profile(...), mobile_emulation_driver() — helper constructors for specific modes.

## Behavior & Paths

- New chrome-for-testing artifacts are downloaded under: C:\new_chrome\extract
- Old testing artifacts are under: C:\old_chrome\extract
- Latest chrome driver copy is stored at: C:\latest_chrome_driver\chromedriver.exe
- Edge driver extracted at: C:\new_edge\extract

## Limitations

- Registry-based browser detection and default file paths are Windows-specific.
- Network access required to download driver archives.
- Some flows will pip-install missing packages (e.g., selenium-wire) at runtime if not present.

For any usage questions or to adapt paths/behavior for other OSes, inspect AIOdriver/functions.py and adjust paths or detection logic.
