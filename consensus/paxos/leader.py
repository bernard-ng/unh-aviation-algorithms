from .paxos_utils import generate_sequence_number, majority_vote
import time

class Leader:
    def __init__(self, replicas):
        self.sequence_number = generate_sequence_number()
        self.replicas = replicas
        print(f"Leader initialized with sequence number: {self.sequence_number}")

    def propose_target(self, target):
        print(f"Leader proposing target: {target}")
        votes = 0
        for replica in self.replicas:
            print(f"Sending proposal for target {target} to replica")
            time.sleep(2)
            if replica.vote_on_proposal(self.sequence_number, target):
                votes += 1
                print(f"Vote received for target {target}")
                time.sleep(2)
        if majority_vote(votes, len(self.replicas)):
            print(f"Target {target} accepted by majority")
            # Envoyer la confirmation aux autres noeuds et retirer la cible de la liste
            return True
        else:
            print(f"Target {target} not accepted by majority")
        return False
