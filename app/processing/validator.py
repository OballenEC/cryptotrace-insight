"""
Validación y normalización de direcciones blockchain.

Actualmente soporta direcciones Ethereum (0x + 40 hex).
En el futuro se pueden añadir validadores para otras redes (Stellar, etc.).
"""

import re


# Patrón de dirección Ethereum: 0x seguido de 40 caracteres hexadecimales
ETHEREUM_ADDRESS_PATTERN = re.compile(r"^0x[a-fA-F0-9]{40}$")


def is_valid_ethereum_address(address: str) -> bool:
    """
    Verifica si una cadena tiene el formato de una dirección Ethereum válida.

    IMPORTANTE: Esto valida el FORMATO, no que la dirección exista
    en la blockchain. Una dirección con formato válido puede no tener
    transacciones.

    Args:
        address: Cadena a validar.

    Returns:
        True si el formato es válido, False en caso contrario.
    """
    if not isinstance(address, str):
        return False
    return bool(ETHEREUM_ADDRESS_PATTERN.match(address.strip()))


def normalize_address(address: str) -> str:
    """
    Limpia y normaliza una dirección Ethereum.

    - Elimina espacios al inicio y al final.
    - Asegura que empiece con '0x'.
    - Devuelve en minúsculas (los hashes no distinguen mayúsculas).

    Args:
        address: Cadena con la dirección.

    Returns:
        Dirección normalizada.
    """
    address = address.strip()
    if not address.startswith("0x"):
        address = "0x" + address
    return address.lower()

def is_valid_stellar_address(address: str) -> bool:
    """
    Verifica si una cadena tiene el formato de una cuenta Stellar válida.

    Las cuentas Stellar empiezan con 'G' y tienen 56 caracteres.
    """
    if not isinstance(address, str):
        return False
    address = address.strip()
    return len(address) == 56 and address.startswith("G")