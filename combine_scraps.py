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
    new = new.strip().title()

    # have to invert custom-changed names for the found fights since MMA decisions.com has them different
    if new == "Marco Polo Reyes":
        new = "Polo Reyes"
    elif new == "Timothy Johnson":
        new = "Tim Johnson"
    elif new == "Katlyn Chookagian":
        new = "Katlyn Cerminara"
    elif new == "Azunna Anyanwu":
        new = "Zu Anyanwu"
    elif new == "Jacare Souza":
        new = "Ronaldo Souza"
    elif new == "Pingyuan Liu":
        new = "Liu Pingyuan"
    elif new == "Bibulatov Magomed":
        new = "Magomed Bibulatov"
    elif new == "Inoue Mizuki":
        new = "Mizuki Inoue"
    elif new == "Joanne Calderwood":
        new = "Joanne Wood"
    # elif new == "Weili Zhang":
        # new = "Zhang Weili"
    elif new == "Loopy Godinez":
        new = "Lupita Godinez"
    elif new == "Grigory Popov":
        new = "Grigorii Popov"
    elif new == "Aleksandra Albu":
        new = "Alexandra Albu"
    elif new == "Matt Riddle":
        new = "Matthew Riddle"
    elif new == "Kevin Souza":
        new = "Edimilson Souza"
    elif new == "Wang Sai":
        new = "Sai Wang"
    elif new == "Lipeng Zhang":
        new = "Zhang Lipeng"
    elif new == "Robbie Peralta":
        new = "Robert Peralta"
    elif new == "Rich Walsh":
        new = "Richard Walsh"
    elif new == "Marcio Alexandre Jr.":
        new = "Marcio Alexandre Junior"
    elif new == "Dave Kaplan":
        new = "David Kaplan"
    elif new == "Consta Philippou":
        new = "Constantinos Philippou"
    elif new == "John Macapa":
        new = "John Teixeira"
    elif new == "Tiago Trator":
        new = "Tiago dos Santos e Silva"
    
    return new

all_fights = pd.read_csv("final_fight_scraping_df.csv")
found_fights = pd.read_csv("found_fights.csv")
zack_fights = pd.read_csv("zack_found.csv")
ethan_fights = pd.read_csv("ethan_found.csv")

print(f"{found_fights.shape=}")
print(f"{zack_fights.shape=}")
print(f"{ethan_fights.shape=}")
print(f"{all_fights.shape=}")
print()

scraped_dfs = [zack_fights, ethan_fights]  #add ethan_fights here once he has his

for df in scraped_dfs:
    print(f"{list(found_fights.columns)=}")
    found_fights = pd.concat([found_fights, df])
    print(f"{list(found_fights.columns)=}")
    print(f"{found_fights.shape=}")
    print()
print(f"\nJOINING ALL_FIGHTS & FOUND_FIGHTS\n")

left_cols = ["Fighter_1", "Fighter_2"]
if 'Fight_ID' in all_fights.columns:
    all_fights = all_fights.drop('Fight_ID', axis=1)
# all_fights = all_fights.apply(lambda row: reorder_names(row), axis=1)

# found_fights = pd.read_csv("found_fights.csv")
found_fights['found'] = True
righ_cols = ["Fighter_1", "Fighter_2"]

for l_col, r_col in zip(left_cols, righ_cols):
    #standardize all names before joining
    if l_col != "F1_W":
        all_fights[l_col] = all_fights[l_col].str.replace("\xa0", " ").apply(lambda x: clean_names(x))
    if r_col != "F1_W":
        found_fights[r_col] = found_fights[r_col].str.replace("\xa0", " ").apply(lambda x: clean_names(x))

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

print(joined_df.loc[joined_df['found'] == False])
found_fights = joined_df.loc[joined_df['found'] == True]
found_fights = found_fights.sort_values('Date')
found_fights = found_fights.drop(labels=['F1_W_y', 
                                         'Judge-1-Name_x', 'F1_Judge-1-Score', 'F2_Judge-1-Score',
                                         'Judge-2-Name_x', 'F1_Judge-2-Score', 'F2_Judge-2-Score',
                                         'Judge-3-Name_x', 'F1_Judge-3-Score', 'F2_Judge-3-Score',
                                         'found'], axis=1)
found_fights = found_fights.rename(columns={'F1_W_x': 'F1_W',
                                            'Judge-1-Name_y': 'Judge-1-Name',
                                            'Judge-2-Name_y': 'Judge-2-Name',
                                            'Judge-3-Name_y': 'Judge-3-Name'})

found_fights['Fight_ID'] = found_fights['Fight_ID'].astype(int)
print(found_fights.info())

print()
print(f"{all_fights.shape=}")
print(f"{found_fights.shape=}")
print(f"# Fights that are still needed: {all_fights.shape[0] - found_fights.shape[0]}")
print()

for col in ['Judge-1-Name', 'Judge-2-Name', 'Judge-3-Name']:
    found_fights[col] = found_fights[col].str.replace("\xa0", " ")

found_fights.to_csv("post_scraping_all_fights.csv", index=False)