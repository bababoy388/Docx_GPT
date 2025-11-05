import math
import string
import unicodedata
from collections import Counter
from typing import TypedDict, Literal

class PasswordResult(TypedDict):
    valid: bool
    level: Literal["too_weak", "weak", "good", "very_good"]
    message: str
    entropy_bits: float

ASCII_LOWER = set(string.ascii_lowercase)
ASCII_UPPER = set(string.ascii_uppercase)
ASCII_DIGITS = set(string.digits)
ASCII_SYMBOLS = set(string.punctuation)  # ~32-33 символа

def conservative_pool_size(chars: set[str]) -> int:
    pool = 0
    if chars & ASCII_LOWER:
        pool += 26
    if chars & ASCII_UPPER:
        pool += 26
    if chars & ASCII_DIGITS:
        pool += 10
    if chars & ASCII_SYMBOLS:
        pool += len(ASCII_SYMBOLS)
    # Любой не-ASCII символ — добавим ограниченный бонус один раз,
    # чтобы не раздувать оценку экзотическими наборами.
    if any(ord(c) > 0x7F for c in chars):
        pool += 32  # скромный бонус за «униконы»
    return max(pool, 1)

def shannon_bits(password: str) -> float:
    n = len(password)
    if n == 0:
        return 0.0
    freq = Counter(password)
    h = 0.0
    for count in freq.values():
        p = count / n
        h -= p * math.log2(p)
    # Шеннон на символ (бит/символ) * длина = биты строки
    return h * n

def validate_password(password: str) -> PasswordResult:
    # Нормализация Unicode
    password = unicodedata.normalize("NFKC", password)

    if len(password) < 8:
        return {
            "valid": False,
            "level": "too_weak",
            "message": "Пароль должен содержать минимум 8 символов",
            "entropy_bits": 0.0,
        }

    # простая проверка на излишние повторы
    if len(set(password)) / len(password) < 0.3:
        return {
            "valid": False,
            "level": "too_weak",
            "message": "Слишком много повторяющихся символов",
            "entropy_bits": 0.0,
        }

    chars = set(password)
    pool = conservative_pool_size(chars)
    theoretical_bits = len(password) * math.log2(pool)
    # Шеннон может помочь слегка штрафовать однообразие; весим его очень скромно
    entropy = 0.9 * theoretical_bits + 0.1 * shannon_bits(password)

    # более строгие пороги
    if entropy < 40:
        return {"valid": False, "level": "too_weak", "message": "Слишком простой пароль", "entropy_bits": entropy}
    elif entropy < 55:
        return {"valid": False, "level": "weak", "message": "Слабый пароль — увеличьте длину и разнообразие", "entropy_bits": entropy}
    elif entropy < 75:
        return {"valid": True, "level": "good", "message": "Хороший пароль", "entropy_bits": entropy}
    else:
        return {"valid": True, "level": "very_good", "message": "Очень хороший пароль", "entropy_bits": entropy}

