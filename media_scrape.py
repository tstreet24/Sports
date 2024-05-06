import pandas as pd
import requests
import re
import unidecode
from bs4 import BeautifulSoup

def clean_names(name):
    try:
        name = unidecode.unidecode(name)
        new = name.lower()
        new = re.sub(r'[àáâãäå]', 'a', new)
        new = re.sub(r'[èéêë]', 'e', new)
        new = re.sub(r'[ìíîï]', 'i', new)
        new = re.sub(r'[òóôõö]', 'o', new)
        new = re.sub(r'[ùúûü]', 'u', new)
        return new.title()
    except:
        name

def get_media_scores(fighter_1, fighter_2, f1_w, fight_id, show=False):
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
    
    url = f"http://mmadecisions.com/decision/{fight_id}/{fighter_1.replace(' ', '-') if f1_w == 1 else fighter_2.replace(' ', '-')}-vs-{fighter_1.replace(' ', '-') if f1_w == 0 else fighter_2.replace(' ', '-')}"
    
    if show:
        print(url)
        
    payload = requests.get(url)

    # print(payload.links)
    # print()
    # print(payload.text)
    # print()
    soup = BeautifulSoup(payload.content, 'html.parser')

    soups = soup.get_text(separator="  ", strip=True).split("MEDIA SCORES")
    soup = soups[1]
    soups = soup.split("YOUR SCORECARD")
    soup = soups[0]
    # print(soup)
    # print()
    bits = soup.split("  ")

    if show:
        print(bits)
    # print()

    fighter_1_count = 0
    fighter_2_count = 0
    draw_count = 0
    scores_count = 0
    for i in range(0, len(bits)):
        bit = bits[i]
        if bit == "DRAW":
            draw_count += 1
            
        elif '-' not in bit:
            if (any([True if clean_names(sub) in fighter_1 else False for sub in bit.split(" ")])) and (len(bit) > 1):
                fighter_1_count += 1
            elif (any([True if clean_names(sub) in fighter_2 else False for sub in bit.split(" ")])) and (len(bit) > 1):
                fighter_2_count += 1
                
        elif '-' in bit:
            sub_bits = bit.split('-')
            if (any([True if clean_names(sub) in fighter_1 else False for sub_bit in sub_bits for sub in sub_bit.split(" ")])) and (len(bit) > 5):
                fighter_1_count += 1
            elif (any([True if clean_names(sub) in fighter_2 else False for sub_bit in sub_bits for sub in sub_bit.split(" ")])) and (len(bit) > 5):
                fighter_2_count += 1
        
        if ("-" in bit) and not ("." in bit):
            if (len(bit) == 5) and (bit[0].isnumeric()):
                scores_count += 1
    return fighter_1_count, fighter_2_count, draw_count, scores_count

def alt_main():
    fighter_1 = "Alexander Volkanovski"
    fighter_2 = "Max Holloway"
    f1_w = 1
    fight_id = 10781
    scores = get_media_scores(fighter_1, fighter_2, f1_w, fight_id, show=True)
    print(f"\n{fighter_1} got {scores[0]} votes | {fighter_2} got {scores[1]} votes | {scores[2]} votes for draw | {scores[3]} total votes\n")

    fighter_1 = "Michael Bisping"  	
    fighter_2 = "Rashad Evans"
    f1_w = 0
    fight_id = 902
    scores = get_media_scores(fighter_1, fighter_2, f1_w, fight_id, show=True)

    print(f"\n{fighter_1} got {scores[0]} votes | {fighter_2} got {scores[1]} votes | {scores[2]} votes for draw | {scores[3]} total votes\n")

    fighter_1 = "Ignacio Bahamondes"
    fighter_2 = "John Makdessi"
    f1_w = 0
    fight_id = 11829
    scores = get_media_scores(fighter_1, fighter_2, f1_w, fight_id, show=True)
    print(f"\n{fighter_1} got {scores[0]} votes | {fighter_2} got {scores[1]} votes | {scores[2]} votes for draw | {scores[3]} total votes\n")

    fighter_1 = "Bobby Green"
    fighter_2 = "Rashid Magomedov"
    f1_w = 0
    fight_id = 7985
    scores = get_media_scores(fighter_1, fighter_2, f1_w, fight_id, show=True)
    print(f"\n{fighter_1} got {scores[0]} votes | {fighter_2} got {scores[1]} votes | {scores[2]} votes for draw | {scores[3]} total votes\n")

    fighter_1 = "Martin Day"
    fighter_2 = "Pingyuan Liu"
    f1_w = 0
    fight_id = 9535
    scores = get_media_scores(fighter_1, fighter_2, f1_w, fight_id, show=True)
    print(f"\n{fighter_1} got {scores[0]} votes | {fighter_2} got {scores[1]} votes | {scores[2]} votes for draw | {scores[3]} total votes\n")
    
    fighter_1 = "Elias Theodorou"
    fighter_2 = "Eryk Anders"
    f1_w = 1
    fight_id = 9630
    scores = get_media_scores(fighter_1, fighter_2, f1_w, fight_id, show=True)
    print(f"\n{fighter_1} got {scores[0]} votes | {fighter_2} got {scores[1]} votes | {scores[2]} votes for draw | {scores[3]} total votes\n")

def main():
    fights_df = pd.read_csv("post_scraping_all_fights.csv")
    # fights_df = fights_df.iloc[:11, :]
    fights_df['F1_media_votes'] = None
    fights_df['F2_media_votes'] = None
    fights_df['media_votes_draw'] = None
    fights_df['media_votes_count'] = None
    fights_df['media_votes_correct'] = False
    
    for idx, row in fights_df.iterrows():
        output = get_media_scores(row['Fighter_1'], row['Fighter_2'], row['F1_W'], row['Fight_ID'])
        fights_df.iloc[idx, list(fights_df.columns).index('F1_media_votes')] = output[0]
        fights_df.iloc[idx, list(fights_df.columns).index('F2_media_votes')] = output[1]
        fights_df.iloc[idx, list(fights_df.columns).index('media_votes_draw')] = output[2]
        fights_df.iloc[idx, list(fights_df.columns).index('media_votes_count')] = output[3]
        fights_df.iloc[idx, list(fights_df.columns).index('media_votes_correct')] = True if ((output[0] + output[1] + output[2]) == output[3]) else False
        print(f'{idx} / {fights_df.shape[0]}')
    
    print(fights_df['media_votes_correct'].value_counts())
    fights_df.to_csv("post_scraping_all_fights_media.csv", index=False)
    
if __name__ == "__main__":
    main()