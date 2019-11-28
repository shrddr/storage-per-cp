import re

import requests
import time
from bs4 import BeautifulSoup
import pickle


class HousingCache:
    def __init__(self):
        self.sess = requests.session()
        try:
            self.cache = pickle.load(open('cache.p', "rb"))
        except FileNotFoundError:
            self.cache = {}

    def store(self, k, v):
        self.cache[k] = v
        pickle.dump(self.cache, open('cache.p', "wb"))

    def get(self, k):
        if k in self.cache:
            return self.cache[k]
        time.sleep(1)
        url = f'https://bdocodex.com/tip.php?id=npc--{i}&nf=on'
        r = self.sess.get(url)
        print(url, r.status_code)
        self.store(i, r.text)
        return r.text


def parse(text):
    pattern_cp = r'^\r\nRequired Contribution Points: (\d+)$'
    pattern_loc = r'^Location: (.+)$'
    pattern_dataid = r'^npc--(\d+)$'
    pattern_slots = r"\d+ Level– Work Cost: .*? Work Time: \d+mAdds (\d+) more spaces in the Storage\."
    pattern_work = r"(\d+) Level– Work Cost: .*? Work Time: \d+m"

    soup = BeautifulSoup(text, "html.parser")
    name = soup.select_one('span.item_title > b')
    if name is None:  # empty response
        return None
    name = name.text
    # print(name)

    loc = soup.find(text=re.compile(pattern_loc))
    if loc is None:  # guild house
        return None
    loc = re.search(pattern_loc, loc).group(1)
    # print(loc)

    cp = soup.find(text=re.compile(pattern_cp))
    cp = re.search(pattern_cp, cp).group(1)
    cp = int(cp)
    # print(cp)

    reqs_el = soup.select('a.qtooltip.item_grade_0')
    reqs = []
    for req in reqs_el:
        data_id = re.search(pattern_dataid, req['data-id']).group(1)
        data_id = int(data_id)
        # print(data_id, text)
        reqs.append(data_id)

    stor = soup.find(text='Storage ')
    slots_text = stor.parent.nextSibling.text
    slots_max = 0
    for match in re.finditer(pattern_slots, slots_text, re.S):
        slots = int(match.group(1))
        slots_max = max(slots_max, slots)
    # print(slots_max)

    lodg = soup.find(text='Lodging ')
    if lodg is None:
        work_max = 0
    else:
        work_text = lodg.parent.nextSibling.text
        # print(work_text)
        work_max = 0
        for match in re.finditer(pattern_work, work_text, re.S):
            work = int(match.group(1))
            work_max = max(work_max, work)

    return loc, name, cp, slots_max, work_max, reqs

codex = {}

c = HousingCache()

for i in range(2101, 3703):
    text = c.get(i)
    data = parse(text)
    print(i, data)
    if data is not None:
        codex[i] = data

pickle.dump(codex, open('codex.p', "wb"))
