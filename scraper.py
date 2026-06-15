from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import csv
import time

def scrape_flashscore():
    url = "https://www.flashscore.se/fotboll/sverige/superettan/resultat/"
    
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    
    # Vänta och scrolla för att ladda allt innehåll
    time.sleep(3)
    driver.execute_script("window.scrollTo(0, 500);")
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, 1000);")
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, 2000);")
    time.sleep(2)
    
    # Hämta alla match-element
    matches = driver.find_elements(By.CLASS_NAME, "event__match")
    
    results = []
    
    for match in matches:
        match_text = match.text
        
        # Varje match-text ser ut så här:
        # "11.06. 19:00\nHelsingborgs IF\nLandskrona BoIS\n0\n3"
        lines = match_text.strip().split('\n')
        
        if len(lines) >= 5:  # Datum/tid, hemmalag, bortalag, hemmamål, bortamål
            # Hoppa över datum-raden, ta lagnamn och mål
            hemmalag = lines[1]
            bortalag = lines[2]
            hemmamal = lines[3]
            bortamal = lines[4]
            
            results.append({
                "hemmalag": hemmalag,
                "hemma_mal": hemmamal,
                "bortalag": bortalag,
                "borta_mal": bortamal
            })
    
    # Spara till CSV
    with open("superettan_resultat.csv", "w", newline="", encoding="utf-8") as f:
        fieldnames = ["hemmalag", "hemma_mal", "bortalag", "borta_mal"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    
    print(f"Sparade {len(results)} matcher till superettan_resultat.csv")
    

    
    driver.quit()

def scrape_upcoming_matches():
    url = "https://www.flashscore.se/fotboll/sverige/superettan/matcher/"
    
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    
    time.sleep(3)
    
    # Klicka "Visa mer"
    clicks = 0
    while clicks < 20:
        try:
            show_more = driver.find_element(By.CLASS_NAME, "event__more")
            driver.execute_script("arguments[0].scrollIntoView();", show_more)
            time.sleep(1)
            show_more.click()
            clicks += 1
            time.sleep(2)
        except:
            break
    
    time.sleep(2)
    
    matches = driver.find_elements(By.CLASS_NAME, "event__match")
    upcoming = []
    
    for match in matches:
        lines = match.text.strip().split('\n')
        if len(lines) >= 3:
            # Skippa matcher som redan har resultat
            if len(lines) >= 4 and any(c.isdigit() for c in lines[3]):
                continue
            
            upcoming.append({
                "hemmalag": lines[1],
                "bortalag": lines[2]
            })
    
    # Spara till CSV (endast lagnamn)
    with open("kommande_matcher.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["hemmalag", "bortalag"])
        for match in upcoming:
            writer.writerow([match["hemmalag"], match["bortalag"]])
    
    print(f"Sparade {len(upcoming)} kommande matcher till kommande_matcher.csv")
    driver.quit()

scrape_flashscore()
scrape_upcoming_matches()