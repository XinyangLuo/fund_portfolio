from prettytable import PrettyTable
import numpy as np

def tabulize_result(codes, weights, capital, code_name_dict, title):
    table = PrettyTable(['Code', 'Name', 'Weight', 'Capital'])
    capitals = np.round(capital*weights)
    for i, code in enumerate(codes):
        table.add_row([code, code_name_dict[code], weights[i], capitals[i]], divider=(i==len(codes)-1))
    table.add_row(['Sum', '-', 1, float(capital)])
    table.title = f'{title}_portfolio'
    return table