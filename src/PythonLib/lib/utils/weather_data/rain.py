# %%
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import calendar
import time
import pandas as pd
# %%
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
# %%
per_month = []
per_month_date = []
for mon in range(1, 13):
    print(mon)
    year = 2019 #CHANGE THIS TO SELECT YEAR
    link = f'https://www.wunderground.com/history/monthly/us/tx/houston/KHOU/date/{year}-{mon}'
    if mon < 10:
        m = f'0{mon}'
    else:
        m = mon

    driver = webdriver.Chrome('CHROMEDRIVER PATH', chrome_options=options)
    
    driver.get(link)
    time.sleep(3)
    data = driver.find_element_by_xpath('//*[@id="inner-content"]/div[2]/div[1]/div[5]/div[1]/div/lib-city-history-observation/div/div[2]/table/tbody/tr/td[7]')
    per_month.append(data.text.split('\n')[1:])
    from_ = f'{year}-{m}-01'
    date = datetime.strptime(from_, "%Y-%m-%d")
    _, days = calendar.monthrange(date.year, date.month)

    days_ = []
    for day in range(1, days+1):
        fech = date.replace(day = day)
        fech = datetime.strftime(fech, "%Y-%m-%d")
        days_.append(fech)
    
    per_month_date.append(days_)
        

# %%
dates = [item for sublist in per_month_date for item in sublist]
precip = [str(float(item)*25.4).replace('.', ',') for sublist in per_month for item in sublist]
# %%
df = pd.DataFrame(dates, index = None)
df['precip'] = precip
# %%
df.columns =['Dates', 'Precip']# %%
df.to_csv('rain_houston.csv', sep=';', index = None)