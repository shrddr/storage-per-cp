import pickle
import pandas as pd
pd.set_option('display.max_rows', 500)


codex = pickle.load(open('codex.p', "rb"))
locations = {}

for i in codex:
    loc, name, cp, storage, lodging, reqs = codex[i]
    for k in reqs:
        cp += codex[k][2]
        storage += codex[k][3]

    if loc not in locations:
        locations[loc] = {}
    locations[loc][name] = cp, storage, storage / cp


for loc in locations:
    print("\n"+loc)
    df = pd.DataFrame.from_dict(locations[loc], orient='index', columns=['cost', 'slots', 'profit'])
    # print(df.sort_values('profit'))
    with open(f"storage-{loc}.txt", 'w', encoding='utf-8') as f:
        print(df.sort_values('profit'), file=f)
