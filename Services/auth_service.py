# pylint: disable=import-error
import bcrypt
import jwt
from datetime import datetime, timedelta
from Repositories.user_repository import create_user, find_by_email
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY")



def register(email, password):
    utilisateur_existant = find_by_email(email)

    if utilisateur_existant is not None:
        return None, "Cet email est déjà utilisé"

    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    create_user(email, password_hash.decode('utf-8'))

    return email, None


def login(email, password):
    utilisateur = find_by_email(email)

    if utilisateur is None:
        return None, "Email ou mot de passe incorrect"

    password_hash_stocke = utilisateur[2]
    mot_de_passe_correct = bcrypt.checkpw(password.encode('utf-8'), password_hash_stocke.encode('utf-8'))

    if not mot_de_passe_correct:
        return None, "Email ou mot de passe incorrect"

    token = jwt.encode(
        {
            "email": email,
            "exp": datetime.utcnow() + timedelta(hours=2)
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