import csv,os
import json
input_file = "Lidia.csv"
character_name = "lidia"
json_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "..","..","json"))
output_file = f'{json_folder}/{character_name}.json'

movelist = []

def normalize_value(value: str):


    if value.isdigit() and int(value) > 0:
        return "+" + value
    if "KND" in value:
        return "KND"
    elif "launch" in value.lower():
        return "Launch"
    return value


with open(input_file, encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    firstline = True
    for row in csv_reader:
        if firstline:
            firstline = False
            continue
        new_move = {}
        new_move['Command'] = row[1]
        '''
        if row[1]:
            aliases = []
            positions= [pos for pos, char in enumerate(row[1]) if char == "\""]

            for x in range(0, len(positions), 2):
                alias = row[1][int(positions[x] +1): int(positions[x+1])]
                aliases.append(alias)

            new_move['Alias'] = aliases'''

        new_move['Hit level'] = row[2].lower()
        new_move['Damage'] = row[7].split("/")[0]
        new_move['Start up frame'] = row[3].split(",")[0]
        new_move['Block frame'] = normalize_value(row[4])
        new_move['Hit frame'] = normalize_value(row[5])
        new_move['Counter hit frame'] = normalize_value(row[6])
        new_move['Notes'] = row[8]
        gif_data = ""
        if row[0]:
            gif_data = 'https://firebasestorage.googleapis.com/v0/b/tekken-guru.appspot.com/o/moves%2F{}%2F{}.mp4?alt=media'.format(character_name,row[0])

        new_move['Gif'] = gif_data
        for entry in new_move:
            if type(new_move[entry]) != list and (new_move[entry] is None or not new_move[entry].strip()):
                new_move[entry] = "-"

        movelist.append(new_move)
    print(movelist)


with open(output_file, 'w') as c:
    json.dump(movelist, c, sort_keys=True, indent=4, ensure_ascii=True)