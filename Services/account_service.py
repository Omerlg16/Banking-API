from Repositories.account_repository import find_by_user_id, update_balance

def _montant_invalide(amount):
    if not isinstance(amount, (int, float)) or isinstance(amount, bool):
        return "Montant invalide"
    if amount <= 0:
        return "Le montant doit être positif"
    return None

def balance(user_id):
    compte = find_by_user_id(user_id)          # tuple (id, user_id, client, solde)

    if compte is None:
        return None, "Compte introuvable"

    return compte[3], None

def withdraw(user_id, amount):
    erreur = _montant_invalide(amount)
    if erreur:
        return None, erreur

    compte = find_by_user_id(user_id)

    if compte is None:
        return None, "Compte introuvable"

    account_id = compte[0]
    solde_actuel = compte[3]

    if amount > solde_actuel:
        return None, "Solde Insuffisant"

    nouveau_solde = solde_actuel - amount

    update_balance(account_id, nouveau_solde)  # applique le changement via le repository

    return nouveau_solde, None

def deposit(user_id, amount):
    erreur = _montant_invalide(amount)
    if erreur:
        return None, erreur

    compte = find_by_user_id(user_id)

    if compte is None:
        return None, "Compte introuvable"

    account_id = compte[0]
    solde_actuel = compte[3]
    nouveau_solde = solde_actuel + amount

    update_balance(account_id, nouveau_solde)
    return nouveau_solde, None

if __name__ == "__main__":
    resultat, erreur = deposit(1, 100000)  # 1 = user_id (et non plus account_id)
    if erreur:
        print("Erreur :", erreur)
    else:
        print("Nouveau solde :", resultat)
