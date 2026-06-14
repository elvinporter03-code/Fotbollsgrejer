from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import csv
import time
import re

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

scrape_flashscore()