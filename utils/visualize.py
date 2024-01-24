from prettytable import PrettyTable
import numpy as np

def tabulize_result(codes, weights, capital, code_name_dict, title):
    table = PrettyTable(['Code', 'Name', 'Weight', 'Capital'])
    capitals = np.around(capital*weights / 10) * 10
    for i, code in enumerate(codes):
        table.add_row([code, code_name_dict[code], f'{weights[i]:.3f}', f'{capitals[i]:.1f}'], divider=(i==len(codes)-1))
    table.add_row(['Sum', '-', f'{sum(weights):.2f}', f'{sum(capitals):.1f}'])
    table.title = f'{title}_portfolio'
    return table