from prettytable import PrettyTable

def tabulize_result(codes, weights):
    table = PrettyTable(['Code', 'Weight'])
    for i in range(len(codes)):
        table.add_row([codes[i], weights[i]])
    return table