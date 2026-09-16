# pylint: disable=import-error
import os
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from dotenv import load_dotenv

from Repositories.user_repository import create_user_with_account, find_by_email

load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("La variable d'environnement SECRET_KEY n'est pas définie")



def register(email, password):
    if not email or not password:
        return None, "Email et mot de passe requis"

    utilisateur_existant = find_by_email(email)

    if utilisateur_existant is not None:
        return None, "Cet email est déjà utilisé"

    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    create_user_with_account(email, password_hash.decode('utf-8'))

    return email, None


def login(email, password):
    if not email or not password:
        return None, "Email et mot de passe requis"

    utilisateur = find_by_email(email)

    if utilisateur is None:
        return None, "Email ou mot de passe incorrect"

    password_hash_stocke = utilisateur[2]
    mot_de_passe_correct = bcrypt.checkpw(password.encode('utf-8'), password_hash_stocke.encode('utf-8'))

    if not mot_de_passe_correct:
        return None, "Email ou mot de passe incorrect"

    token = jwt.encode(
        {
            "user_id": utilisateur[0],
            "email": email,
            "exp": datetime.now(timezone.utc) + timedelta(hours=2)
        },
        SECRET_KEY,
        algorithm="HS256"
    )

    return token, None


def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload, None
    except jwt.ExpiredSignatureError:
        return None, "Token expiré"
    except jwt.InvalidTokenError:
        return None, "Token invalide"


if __name__ == "__main__":
    resultat, erreur = login("omer@test.com", "motdepasse123")
    print(resultat, erreur)