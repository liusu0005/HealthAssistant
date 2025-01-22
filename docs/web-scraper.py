import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime

def scrape_heart_disease_articles():
    # Example heart diseases and corresponding example URLs (for demonstration purposes)
    heart_diseases = {
        "Coronary Artery Disease": [
            "https://www.mayoclinic.org/diseases-conditions/coronary-artery-disease/diagnosis-treatment/drc-20350619"
        ],
        "Heart Failure": [
            "https://my.clevelandclinic.org/health/diseases/17069-heart-failure-understanding-heart-failure",
            "https://myhealth.alberta.ca/Health/aftercareinformation/pages/conditions.aspx?hwid=abk1946#:~:text=Weigh%20yourself%20every%20day.,about%20making%20a%20personal%20plan."
        ],
        "Arrhythmia": [
            "https://www.pennmedicine.org/updates/blogs/heart-and-vascular-blog/2022/may/heart-arrhythmia-dos-and-donts#:~:text=DON'T%20skimp%20out%20on,the%20sleep%20apnea%2C%20too.%E2%80%9D"
        ],
        "Valvular Heart Disease": [
            "https://myhealth.alberta.ca/Health/aftercareinformation/pages/conditions.aspx?hwid=uh3409"
        ],
        "Congenital Heart Defects": [
            "https://www.mayoclinic.org/diseases-conditions/congenital-heart-defects-children/diagnosis-treatment/drc-20350080#:~:text=Lifestyle%20and%20home%20remedies,your%20child%20needs%20preventive%20antibiotics."
        ]
    }

    # Create a directory for saving individual files with today's date
    today = datetime.now().strftime("%Y-%m-%d")
    output_dir = f"heart_disease_articles_{today}"
    os.makedirs(output_dir, exist_ok=True)

    for disease, urls in heart_diseases.items():
        for i, url in enumerate(urls, start=1):
            try:
                response = requests.get(url)
                response.raise_for_status()

                # Parse the webpage content
                if "pdf" in url:
                    filename = f"{disease.replace(' ', '_')}_{i}.txt"
                    with open(os.path.join(output_dir, filename), "w") as file:
                        file.write(f"Disease: {disease}\nURL: {url}\nType: PDF Document\n")
                else:
                    soup = BeautifulSoup(response.content, "html.parser")
                    title = soup.title.string if soup.title else "No Title Found"
                    all_text = soup.get_text(strip=True)  # Extract all text from the page

                    # Generate a filename based on the disease name and index
                    filename = f"{disease.replace(' ', '_')}_{i}.txt"

                    with open(os.path.join(output_dir, filename), "w") as file:
                        file.write(f"Disease: {disease}\nURL: {url}\nTitle: {title}\nContent: {all_text}\n")

            except Exception as e:
                error_filename = f"{disease.replace(' ', '_')}_{i}_error.txt"
                with open(os.path.join(output_dir, error_filename), "w") as file:
                    file.write(f"Disease: {disease}\nURL: {url}\nError: {str(e)}\n")

    print(f"Scraping completed. Individual files saved in '{output_dir}' directory.")

# Run the scraper
scrape_heart_disease_articles()