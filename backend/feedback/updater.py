from sqlalchemy.orm import Session
from models import Preference
from schemas import PreferenceIn, PreferenceOut


def update_preferences(db: Session, pref: PreferenceIn) -> PreferenceOut:
    """
    Update or create user preferences in DB.
    """
    obj = db.query(Preference).first()
    if not obj:
        obj = Preference()
        db.add(obj)

    if pref.tone:
        obj.tone = pref.tone
    if pref.signature is not None:
        obj.signature = pref.signature
    if pref.language:
        obj.language = pref.language

    db.flush()
    return PreferenceOut.model_validate(obj)
