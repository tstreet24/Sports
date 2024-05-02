import pandas as pd
import unidecode
import re

def reorder_names(row):
    j1 = row['Judge-1-Name']
    j2 = row['Judge-2-Name']
    j3 = row['Judge-3-Name']
    
    j1_name = j1.split(" ")[1]
    j2_name = j2.split(" ")[1]
    j3_name = j3.split(" ")[1]
    
    names = [j1_name, j2_name, j3_name]
    index_map = {0: j1, 1: j2, 2: j3}
    name_map = {'Mike Bell': 'Michael Bell',
                'Michael Beltran': 'Mike Beltran',
                'Chamion': 'Champion',
                'Mikkelsen': 'Mikkelson', 
                "D'amato": "D'Amato", 
                "-": " ",
                "Doug": "Douglas",
                "Marco Borges": "Marco Aurelio Borges",
                "Rodriquez": "Rodriguez",
                "Hickmont": "Hickmott",
                "Gregory Jackson": "Dr. Greg Jackson",
                "Leblanc": "LeBlanc",
                "Depasquale": "Depasquale Jr."}
    sorted_names = [j1_name, j2_name, j3_name]
    sorted_names.sort()
    
    return_names = []
    
    for i in range(len(names)):
        idx_name = sorted_names[i]
        correct_name = index_map[names.index(idx_name)]
        for old_name, new_name in name_map.items():
            correct_name = correct_name.replace(old_name, new_name)
        return_names.append(correct_name)
    
    row['Judge-1-Name'] = return_names[0]
    row['Judge-2-Name'] = return_names[1]
    row['Judge-3-Name'] = return_names[2]
    return row

def clean_names(name):
    name = unidecode.unidecode(name)
    new = name.lower()
    new = re.sub(r'[àáâãäå]', 'a', new)
    new = re.sub(r'[èéêë]', 'e', new)
    new = re.sub(r'[ìíîï]', 'i', new)
    new = re.sub(r'[òóôõö]', 'o', new)
    new = re.sub(r'[ùúûü]', 'u', new)
    return new

all_fights = pd.read_csv("final_fight_scraping_df.csv")
left_cols = ["Fighter_1", "Fighter_2", "Judge-1-Name", "Judge-2-Name", "Judge-3-Name"]
all_fights = all_fights.drop('Fight_ID', axis=1)
all_fights = all_fights.apply(lambda row: reorder_names(row), axis=1)

found_fights = pd.read_csv("found_fights.csv")
found_fights['found'] = True
righ_cols = ["Fighter_1", "Fighter_2", "Judge-1-Name", "Judge-2-Name", "Judge-3-Name"]

for l_col, r_col in zip(left_cols, righ_cols):
    if l_col != "F1_W":
        all_fights[l_col] = all_fights[l_col].str.replace("\xa0", " ").apply(lambda x: clean_names(x))
    if r_col != "F1_W":
        found_fights[r_col] = found_fights[r_col].str.replace("\xa0", " ").apply(lambda x: clean_names(x))

# all_fights.to_csv("final_fight_scraping_df.csv", index=False)
# found_fights.to_csv("found_fights.csv", index=False)

# print(all_fights[joining_columns].head().values)
# print(found_fights[joining_columns].head().values)
 
all_cols = set(all_fights.columns)
found_cols = set(found_fights.columns)
shared_cols = all_cols.intersection(found_cols)
print(f"\nShared columns: {list(shared_cols)}")

a_n = all_fights.shape[0]
f_n = found_fights.shape[0]
print(f"\n{all_fights.shape=}")
print(f"{found_fights.shape=}")
print(f"Need to find {a_n - f_n} fights")
print()

joined_df = all_fights.merge(right=found_fights,
                             left_on=left_cols,
                             right_on=righ_cols,
                             how="left")
print(joined_df.info())

new_to_get_df = joined_df.loc[joined_df['found'] != True]
new_to_get_df = new_to_get_df.sort_values('Date')
new_to_get_df = new_to_get_df.drop(labels=['Fight_ID', 'F1_W_y', 'Judge-1-Score', 'Judge-2-Score', 'Judge-3-Score', 'found'], axis=1)
new_to_get_df = new_to_get_df.rename(columns={'F1_W_x': 'F1_W'})
                                     
all_cols2 = set(all_fights.columns)
found_cols2 = set(new_to_get_df.columns)
shared_cols2 = all_cols2.intersection(found_cols2)
print(f"\nShared columns [all fights and need to find]: {len(list(shared_cols2))}, should be {len(list(all_fights.columns))}")

new_to_get_df.to_csv("need_to_scrape.csv", index=False)

n = new_to_get_df.shape[0]
split = n // 2
zack_scrape = new_to_get_df.iloc[split:, :]
ethan_scrape = new_to_get_df.iloc[:split, :]

print(f"{zack_scrape.shape=}")
print(f"{ethan_scrape.shape=}")
print(f"Final data check (should be True): {zack_scrape.shape[0] + ethan_scrape.shape[0] == new_to_get_df.shape[0]}")

zack_scrape.to_csv('zack_scrape.csv', index=False)
ethan_scrape.to_csv('ethan_scrape.csv', index=False)