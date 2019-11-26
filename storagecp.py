import pandas as pd

# city_quarter_house_floor = cost, slots, requirement

calf_workshop_1_1 = (1, 3, None)
calf_workshop_1_2_U = (1, 3, calf_workshop_1_1)
calf_workshop_1_3 = (2, 5, calf_workshop_1_2_U)
calf_workshop_1_4_1F = (3, 8, calf_workshop_1_3)
calf_workshop_1_4_2F = (1, 8, calf_workshop_1_4_1F)

calf_merchant_2_2_1F = (1, 3, None)
calf_merchant_2_9_1F = (2, 5, calf_merchant_2_2_1F)
calf_merchant_2_8 = (2, 8, calf_merchant_2_9_1F)
calf_merchant_2_7_1F = (1, 8, calf_merchant_2_8)
calf_merchant_2_7_2F = (2, 8, calf_merchant_2_7_1F)
calf_merchant_2_7_3F = (2, 12, calf_merchant_2_7_2F)


def traverse(house):
    cost, slots = (0, 0)
    while house is not None:
        c, s, house = house
        cost += c
        slots += s
    return cost, slots, slots / cost


calf = {name: traverse(val) for name, val in locals().items() if 'calf_' in name}

df = pd.DataFrame.from_dict(calf, orient='index', columns=['cost', 'slots', 'profit'])
print(df.sort_values('profit'))
