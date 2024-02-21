import time

def generate_sequence_number():
    # Utiliser le timestamp actuel comme numéro de séquence
    return int(time.time())

def majority_vote(votes, total_nodes):
    # Calculer si la majorité des votes est atteinte
    return votes > total_nodes // 2
