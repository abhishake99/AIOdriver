# AIOdriver
A all in one driver system with support for both chrome and edge with auto update funcationality

## Driver Creation Methods

You can create WebDriver instances for different browsers using the `createwebdriver` function from the `AIOdriver.functions` module.


### Chrome WebDriver Creation

To create a Chrome WebDriver:

```python
from AIOdriver.functions import createwebdriver

driver = ''
driver = createwebdriver(driver, driver_type="chrome")  # Chrome driver creation
```

### Chrome WebDriver Creation
To create a Edge WebDriver:

```python
from AIOdriver.functions import createwebdriver
driver = ''
driver = createwebdriver(driver, driver_type="edge")  # Edge driver creation
```