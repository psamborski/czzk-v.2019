import itertools

list_ = ...

for element in list_:
    groups = [list(g) for _, g in itertools.groupby(element['tickets'], key=lambda x: x['price'])]

    if groups:
        for group in groups:
            print(element['date'], len(group), group[0]['price'], sep=' - ')
    else:
        print(element['date'], 0, None, sep=' - ')
