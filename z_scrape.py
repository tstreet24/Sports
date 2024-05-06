## SCRAPING TIME

import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from unidecode import unidecode
from concurrent.futures import ThreadPoolExecutor, as_completed
from fuzzywuzzy import fuzz
import numpy as np

def normalize_text(text, for_comparison=True):
    """Normalize text for reliable matching: remove HTML tags, accents, and special characters.
       Set `for_comparison` to False to keep the original text formatting."""
    text = BeautifulSoup(text, "html.parser").get_text(strip=True)  # Remove HTML tags
    if for_comparison:
        text = unidecode(text)  # Transliterate to closest ASCII representation
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  # Keep only alphanumeric characters and spaces
        text = re.sub(r'\s+', ' ', text)  # Normalize whitespace to single spaces
        return text.lower()
    return text

def is_correct_page(soup, fighter_1, fighter_2, threshold=90):
    """Check if the page contains both fighters' names with fuzzy matching."""
    page_text = normalize_text(str(soup), for_comparison=True)
    
    text = []
    for itm in page_text.split(" "):
        try:
            integer = int(itm)
            break
        except:
            pass
        text.append(itm.lower())
    relevant_text = " ".join(text)
    
    fighter_1_normalized = normalize_text(fighter_1, for_comparison=True)
    fighter_2_normalized = normalize_text(fighter_2, for_comparison=True)
    
    # Use fuzzy matching to check for fighter names in the page text
    match_1 = fuzz.partial_ratio(fighter_1_normalized, relevant_text)
    match_2 = fuzz.partial_ratio(fighter_2_normalized, relevant_text)
    # print(f"{fighter_1=}, {fighter_1_normalized=}, {match_1}, {fighter_2=}, {fighter_2_normalized=}, {match_2}, {relevant_text=}")
    
    # Both names must meet or exceed the threshold to consider the page correct
    return match_1 >= threshold and match_2 >= threshold

def extract_judge_info(soup):
    """Extract judges' names and scores from the page, without altering judge names."""
    judge_info = {}
    judge_names = soup.find_all('td', class_='judge')
    # Find all 'td' elements for scores, then navigate to 'b' tag for the actual scores
    left_scores = [td.find('b').text for td in soup.find_all('td', class_='bottom-cell', align='center')]
    right_scores = left_scores[1::2]  # Assuming the pattern is left-right-left-right for scores, extract every second element starting from the second
    left_scores = left_scores[::2]  # Extract every second element starting from the first

    for i, (judge, left_score, right_score) in enumerate(zip(judge_names, left_scores, right_scores), start=1):
        # Extract judge names without normalizing
        judge_name = normalize_text(judge.get_text(), for_comparison=False)
        judge_info[f'Judge-{i}-Name'] = judge_name.strip()  # .strip() to remove leading/trailing whitespace
        # Scores are already extracted as text, so just format them
        judge_info[f'Judge-{i}-Score'] = f"{left_score}-{right_score}"

        if i == 3:  # Only consider up to 3 judges
            break

    return judge_info

from concurrent.futures import ThreadPoolExecutor, as_completed

def process_fight(fighter_1, fighter_2, estimated_fight_id, f1_won, last_id):
    if fighter_1 == "Marco Polo Reyes":
        fighter_1 = "Polo Reyes"
    elif fighter_1 == "Timothy Johnson":
        fighter_1 = "Tim Johnson"
    elif fighter_1 == "Katlyn Chookagian":
        fighter_1 = "Katlyn Cerminara"
    elif fighter_1 == "Azunna Anyanwu":
        fighter_1 = "Zu Anyanwu"
    elif fighter_1 == "Jacare Souza":
        fighter_1 = "Ronaldo Souza"
    elif fighter_1 == "Pingyuan Liu":
        fighter_1 = "Liu Pingyuan"
    elif fighter_1 == "Bibulatov Magomed":
        fighter_1 = "Magomed Bibulatov"
    elif fighter_1 == "Inoue Mizuki":
        fighter_1 = "Mizuki Inoue"
    elif fighter_1 == "Joanne Calderwood":
        fighter_1 = "Joanne Wood"
    # elif fighter_1 == "Weili Zhang":
        # fighter_1 = "Zhang Weili"
    elif fighter_1 == "Loopy Godinez":
        fighter_1 = "Lupita Godinez"
    elif fighter_1 == "Grigory Popov":
        fighter_1 = "Grigorii Popov"
    elif fighter_1 == "Aleksandra Albu":
        fighter_1 = "Alexandra Albu"
    
    if fighter_2 == "Marco Polo Reyes":
        fighter_2 = "Polo Reyes"
    elif fighter_2 == "Timothy Johnson":
        fighter_2 = "Tim Johnson"
    elif fighter_2 == "Katlyn Chookagian":
        fighter_2 = "Katlyn Cerminara"
    elif fighter_2 == "Azunna Anyanwu":
        fighter_2 = "Zu Anyanwu"
    elif fighter_2 == "Jacare Souza":
        fighter_2 = "Ronaldo Souza"
    elif fighter_2 == "Pingyuan Liu":
        fighter_2 = "Liu Pingyuan"
    elif fighter_2 == "Bibulatov Magomed":
        fighter_2 = "Magomed Bibulatov"
    elif fighter_2 == "Inoue Mizuki":
        fighter_2 = "Mizuki Inoue"
    elif fighter_2 == "Joanne Calderwood":
        fighter_2 = "Joanne Wood"
    # elif fighter_2 == "Weili Zhang":
        # fighter_2 = "Zhang Weili"
    elif fighter_2 == "Loopy Godinez":
        fighter_2 = "Lupita Godinez"
    elif fighter_2 == "Grigory Popov":
        fighter_2 = "Grigorii Popov"
    elif fighter_2 == "Aleksandra Albu":
        fighter_2 = "Alexandra Albu"
        
    print(f"Starting: {fighter_1} vs {fighter_2}")
    winning_fighter, losing_fighter = (fighter_1, fighter_2) if f1_won == 1 else (fighter_2, fighter_1)
    for fight_id in range(last_id, last_id+1):
        if fight_id - last_id > 400:
            break
        if (winning_fighter == "Alexander Volkov") and (losing_fighter == "Timothy Johnson"):
            fight_id_n = 7476
            url = f"http://mmadecisions.com/decision/{fight_id_n}/fight"
        else:
            url = f"http://mmadecisions.com/decision/{fight_id}/{winning_fighter.replace(' ', '-')}-vs-{losing_fighter.replace(' ', '-')}"
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            check_page = is_correct_page(soup, fighter_1, fighter_2)
            print(f"{check_page=}, {fight_id}/{winning_fighter.replace(' ', '-')}-vs-{losing_fighter.replace(' ', '-')}")
            if check_page:
                # print(soup)
                judge_info = extract_judge_info(soup)
                print(f"\nCompleted: {fighter_1} vs {fighter_2} | Fight ID: {fight_id}\n")
                last_id = max(last_id, fight_id)
                return {'Fighter_1': fighter_1, 'Fighter_2': fighter_2, 'Fight_ID': fight_id, 'F1_W': f1_won, **judge_info}, last_id
    print(f"Failed to find correct page for: {fighter_1} vs {fighter_2}")
    return None, last_id

def main(practice, last_id):
    # with ThreadPoolExecutor(max_workers=10) as executor:
    #     futures = []
    #     for index, row in practice.iterrows():
    #         future = executor.submit(process_fight, row['Fighter_1'], row['Fighter_2'], row['Fight_ID'], row['F1_W'])
    #         futures.append(future)
            
    #     results = []
    #     for future in as_completed(futures):
    #         result = future.result()
    #         if result:
    #             results.append(result)
    #             # You can also print something here if you want to signal the completion of processing

    results = []
    for index, row in practice.iterrows():
        result, last_id = process_fight(row['Fighter_1'], row['Fighter_2'], row['Fight_ID'], row['F1_W'], last_id)
        if result:
            results.append(result)
    fight_data_df = pd.DataFrame(results)
    return fight_data_df, last_id

def interpolate(df):
    ## CODE FOR INTERPOLATING FIGHT IDS
    actual_ids_dates = [
        (902, '2007-11-17'),
        (956, '2008-02-02'), 
        (1083, '2008-09-17'),
        (1264, '2009-06-20'),
        (2355, '2011-03-03'),
        (3691, '2012-09-29'),
        (4344, '2013-07-27'),
        (5739, '2014-12-06'),
        (8519, '2017-10-28'),
        (9310, '2018-08-25'),
        (11887, '2021-05-01')
    ]

    actual_ids_dates = [(id_, pd.Timestamp(date)) for id_, date in actual_ids_dates]

    # Sort the anchor points by date
    actual_ids_dates.sort(key=lambda x: x[1])

    # Initialize an empty dictionary to store the interpolated IDs
    interpolated_id_dict = {}

    # Interpolate the IDs between each pair of adjacent anchor points
    for i in range(len(actual_ids_dates) - 1):
        start_id, start_date = actual_ids_dates[i]
        end_id, end_date = actual_ids_dates[i + 1]
        
        # Generate dates between start_date and end_date (inclusive) at daily intervals
        interpolated_dates = pd.date_range(start=start_date, end=end_date, freq='D')
        
        # Calculate the corresponding interpolated IDs for the interpolated dates
        # This calculates the slope of the line connecting the two anchor points and applies it to the range of dates
        total_days = (end_date - start_date).days
        id_increment_per_day = (end_id - start_id) / total_days
        interpolated_ids = np.round(start_id + (interpolated_dates - start_date).days * id_increment_per_day)
        
        # Update the dictionary with the interpolated IDs for the corresponding dates
        interpolated_id_dict.update(dict(zip(interpolated_dates, interpolated_ids)))

    # Map the interpolated IDs to the 'Date' column of the DataFrame
    df['Fight_ID'] = df['Date'].map(interpolated_id_dict).astype('Int64')
    return df['Fight_ID']

def clean_names(name):
    name = unidecode(name)
    new = name.lower()
    new = re.sub(r'[àáâãäå]', 'a', name)
    new = re.sub(r'[èéêë]', 'e', name)
    new = re.sub(r'[ìíîï]', 'i', name)
    new = re.sub(r'[òóôõö]', 'o', name)
    new = re.sub(r'[ùúûü]', 'u', name)
    return new

# Assuming 'practice' is your DataFrame
# Call the main function and pass your DataFrame
if __name__ == '__main__':
    # scrape_df = pd.read_csv("zack_scrape.csv")
    scrape_df = pd.read_csv("z_still_need_to_scrape.csv")
    scrape_df.columns = [x.strip() for x in scrape_df.columns]
    
    last_id = None
    # for i in range(100, len(scrape_df), 2):
    for i, x in enumerate([7420, 7455, 7476, 10363, 10596, 10655, 10984, 11854]):
        found_df = pd.read_csv("zack_found.csv")
        # sub_scrape_df = scrape_df.iloc[i:i+2, :]
        sub_scrape_df = scrape_df
        sub_scrape_df['Fight_ID'] = False
        last_id = x
        fight_data_df, last_id = main(sub_scrape_df, last_id)
        if not fight_data_df.empty:
            print("Data extraction complete. Displaying partial data:")
            print(fight_data_df.head())
            found_df = pd.concat([found_df, fight_data_df])
            for col in found_df.columns:
                if col not in ('Fight_ID', 'F1_W', 'Judge-1-Score', 'Judge-2-Score', 'Judge-3-Score', 'F1_media_votes', 'F2_media_votes', 'media_votes_draw', 'media_votes_count', 'media_votes_correct'):
                    found_df[col] = found_df[col].str.replace("\xa0", " ").apply(lambda x: clean_names(x))
            found_df.to_csv("zack_found.csv", index=False)
        else:
            print("No data was extracted. Please check the input and URL patterns.")
    found_df = pd.read_csv("zack_found.csv")
    found_df = found_df.drop_duplicates()
    found_df.sort_values(by='Fight_ID', ascending=True).to_csv("zack_found.csv", index=False)
