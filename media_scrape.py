import pandas as pd
import requests
from bs4 import BeautifulSoup

def get_media_scores(fighter_1, fighter_2, f1_w, fight_id, show=False):
    url = f"http://mmadecisions.com/decision/{fight_id}/{fighter_1.replace(' ', '-') if f1_w == 1 else fighter_2.replace(' ', '-')}-vs-{fighter_1.replace(' ', '-') if f1_w == 0 else fighter_2.replace(' ', '-')}"
    
    if print:
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
    bits = soup.split(" ")

    # print(bits)
    # print()

    fighter_1_count = 0
    fighter_2_count = 0
    draw_count = 0
    scores_count = 0
    for i in range(0, len(bits)):
        if bits[i] == "DRAW":
            draw_count += 1
        elif (bits[i] in fighter_1) and (len(bits[i]) > 1):
            fighter_1_count += 1
        elif (bits[i] in fighter_2) and (len(bits[i]) > 1):
            fighter_2_count += 1
        
        if ("-" in bits[i]) and not ("." in bits[i]):
            scores_count += 1
    return fighter_1_count, fighter_2_count, draw_count, scores_count

if __name__ == "__main__":
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