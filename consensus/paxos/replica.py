import time 

class Replica:
    def __init__(self):
        self.last_sequence_number = None

    def vote_on_proposal(self, sequence_number, target):
        print(f"Replica received proposal for target {target} with sequence number {sequence_number}")
        time.sleep(2)  # Attendre 2 secondes avant de voter
        if self.last_sequence_number is None or sequence_number > self.last_sequence_number:
            self.last_sequence_number = sequence_number
            print(f"Replica voting for target: {target}")
            return True
        else:
            print(f"Replica refusing to vote for target {target} due to older sequence number")
        return False
