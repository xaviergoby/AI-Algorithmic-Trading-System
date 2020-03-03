from selenium import webdriver



driver = webdriver.Chrome(executable_path=r"C:\Users\XGOBY\chromedriver.exe".replace('\\','/'))

driver.maximize_window()
driver.get("https://finance.yahoo.com/quote/NVDA/key-statistics?p=NVDA")