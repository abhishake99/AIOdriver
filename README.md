# AIOdriver
A all in one driver system with support for both chrome and edge with auto update funcationality

## Installation

Run this command to install the package `pip install git+https://github.com/abhishake99/AIOdriver.git`

## Driver Creation Methods

You can create WebDriver instances for different browsers using the `createwebdriver` function from the `AIOdriver.functions` module.


### Chrome WebDriver Creation

To create a Chrome WebDriver:

```python
from AIOdriver.functions import createwebdriver
driver = ''
driver = createwebdriver(driver, driver_type="chrome")  # Chrome driver creation
```

### Edge WebDriver Creation

To create a Edge WebDriver:

```python
from AIOdriver.functions import createwebdriver
driver = ''
driver = createwebdriver(driver, driver_type="edge")  # Edge driver creation
```

### Profile WebDriver Creation

To create a Profile WebDriver:

```python
from AIOdriver.functions import createwebdriver
driver = ''
driver = createwebdriver(driver, driver_type="profile",username='Administrator',profile_directory='Default')  
```

### Mobile WebDriver Creation

To create a Mobile WebDriver:

```python
from AIOdriver.functions import createwebdriver
driver = ''
driver = createwebdriver(driver, driver_type="mobile")  
```

### Selenium wire WebDriver Creation

To create a Selenium wire WebDriver:

```python
from AIOdriver.functions import createwebdriver
driver = ''
driver = createwebdriver(driver, driver_type="chrome",crawler_type="bh")  
```