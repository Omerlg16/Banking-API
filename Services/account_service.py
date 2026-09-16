from Repositories.account_repository import find_by_id, update_balance

def _montant_invalide(amount):
    if not isinstance(amount, (int, float)) or isinstance(amount, bool):
        return "Montant invalide"
    if amount <= 0:
        return "Le montant doit être positif"
    return None

def balance(account_id):
    compte = find_by_id(account_id)

    if compte is None:
        return None, "Compte introuvable"

    return compte[2], None

def withdraw(account_id, amount):
    erreur = _montant_invalide(amount)
    if erreur:
        return None, erreur

    compte = find_by_id(account_id)          # récupère le compte via le repository

    if compte is None:
        return None, "Compte introuvable"

    solde_actuel = compte[2]                  # rappel : find_by_id renvoie un tuple (id, client, solde)
                                                # donc l'index 2 correspond au solde

    if amount > solde_actuel:
        return None, "Solde Insuffisant"

    nouveau_solde = solde_actuel - amount

    update_balance(account_id, nouveau_solde)  # applique le changement via le repository

    return nouveau_solde, None
def deposit(account_id, amount):
    erreur = _montant_invalide(amount)
    if erreur:
        return None, erreur

    compte = find_by_id(account_id)

    if compte is None:
        return None, "Compte introuvable"
    solde_actuel = compte[2]
    nouveau_solde = solde_actuel + amount

    update_balance(account_id, nouveau_solde)
    return nouveau_solde, None

if __name__ == "__main__":
    resultat, erreur = deposit(1, 100000)
    if erreur:
        print("Erreur :", erreur)
    else:
        print("Nouveau solde :", resultat)
