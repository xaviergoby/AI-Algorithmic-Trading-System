from selenium import webdriver



driver = webdriver.Chrome(executable_path=r"C:\Users\XGOBY\chromedriver.exe".replace('\\','/'))

driver.maximize_window()

# driver.get("https://finance.yahoo.com/quote/NVDA/key-statistics?p=NVDA")
# driver.get("https://www.investing.com/equities/nvidia-corp")
driver.get("https://www.google.com/search?q=INDEXNASDAQ:.IXIC&tbm=fin#scso=_GyXwXJfCH4jykwXPtIHwAw2:0&wptab=NEWS")

# get_sport = driver.find_element_by_xpath('//*[@id="pairSublinksLevel1"]/li[4]/a')
# get_sport.click()
