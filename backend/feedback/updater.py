from sqlalchemy.orm import Session
from models import Preference


def update_preferences(db: Session, user_id: str, updates: dict):
    prefs = db.query(Preference).filter(Preference.user_id == user_id).first()
    if not prefs:
        prefs = Preference(user_id=user_id)
        db.add(prefs)

    for key, value in updates.items():
        if hasattr(prefs, key):
            setattr(prefs, key, value)

    db.commit()
    db.refresh(prefs)
    return prefs
