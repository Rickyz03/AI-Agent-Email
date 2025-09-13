from typing import List, Optional, Any
from utils.security import encrypt_data, decrypt_data

def _ensure_list_of_str(maybe_list: Optional[Any]) -> List[str]:
    """
    Normalize possible values into a list of strings.
    Accepts: None, list[str], comma-separated string.
    """
    if not maybe_list:
        return []
    if isinstance(maybe_list, list):
        return [str(x) for x in maybe_list]
    if isinstance(maybe_list, str):
        # split by comma if present
        parts = [p.strip() for p in maybe_list.split(",") if p.strip()]
        return parts
    # fallback
    return [str(maybe_list)]


def _encrypt_addr_list(addrs: Optional[Any]) -> Optional[List[str]]:
    """
    Return list of encrypted addresses or None if empty.
    """
    lst = _ensure_list_of_str(addrs)
    if not lst:
        return None
    return [encrypt_data(a) for a in lst]


def _decrypt_addr_list(enc_list: Optional[List[str]]) -> List[str]:
    """
    Try to decrypt each element; if decryption fails, return original element.
    """
    if not enc_list:
        return []
    out = []
    for v in enc_list:
        try:
            out.append(decrypt_data(v))
        except Exception:
            # if it's not encrypted or decryption fails, return original
            out.append(v)
    return out


def _decrypt_single(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    try:
        return decrypt_data(value)
    except Exception:
        return value