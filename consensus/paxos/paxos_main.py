from leader import Leader
from replica import Replica

def main():
    replicas = [Replica() for _ in range(3)]  # Créer 3 réplicas
    leader = Leader(replicas)

    # Exemple de proposition de cible
    target = "Target A"
    if leader.propose_target(target):
        print(f"Consensus reached for target: {target}")
    else:
        print("Consensus not reached")

if __name__ == "__main__":
    main()
