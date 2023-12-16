from prettytable import PrettyTable
import numpy as np

def tabulize_result(codes, weights, capital):
    table = PrettyTable(['Code', 'Weight', 'Capital'])
    capital = np.round(capital*weights)
    for i in range(len(codes)):
        table.add_row([codes[i], weights[i], capital[i]])
    return table