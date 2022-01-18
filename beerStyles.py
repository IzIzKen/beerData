from selenium import webdriver
from selenium.webdriver.chrome import service as fs
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

# chromeDriverの設定
chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument('--window-size=1920,1080')
chromeOptions.add_argument('--headless')
chromeDriver = "chromedriver.exe"
chrome_service = fs.Service(executable_path=chromeDriver)
driver = webdriver.Chrome(service=chrome_service, options=chromeOptions)
wait = WebDriverWait(driver=driver, timeout=60)

driver.get('http://www.beer365.net/styles/')
wait.until(EC.presence_of_element_located)
time.sleep(1)

id = 1
header = ['id', 'name', 'description']
outputs = []
urls = []

majorStyles = driver.find_element(By.CLASS_NAME, 'styles').find_elements(By.TAG_NAME, 'a')
for majorStyle in majorStyles:
    urls.append(majorStyle.get_attribute("href"))

for url in urls:
    driver.get(url)
    wait.until(EC.presence_of_element_located)
    time.sleep(1)

    styles = driver.find_element(By.CLASS_NAME, 'styles')
    names = styles.find_elements(By.TAG_NAME, 'h3')
    description = styles.find_elements(By.TAG_NAME, 'p')

    for i, name in enumerate(names):
        row = [id, name.text, description[i].text]
        outputs.append(row)
        print(id, name.text, description[i].text)
        id += 1

driver.close()
driver.quit()

# shift-jis, utf8, cp932
with open(f"beerStyles.csv", "w", newline="", encoding="utf8") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(outputs)
