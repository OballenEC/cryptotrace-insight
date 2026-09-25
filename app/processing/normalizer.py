"""
Normalizador de transacciones blockchain.

Convierte los datos crudos de las APIs (Etherscan, Stellar, etc.)
a nuestro modelo `Transaction` normalizado.
"""

from datetime import datetime
from typing import Optional

from app.models.transaction import Transaction


def normalize_ethereum_transaction(
    raw_tx: dict, analyzed_address: str
) -> Optional[Transaction]:
    """
    Convierte una transacción cruda de Etherscan a nuestro modelo normalizado.

    Args:
        raw_tx: Diccionario con la transacción cruda de Etherscan.
        analyzed_address: Dirección que estamos analizando (para determinar direction).

    Returns:
        Transaction normalizada, o None si los datos son inválidos.
    """
    try:
        sender = raw_tx.get("from", "").lower()
        receiver = raw_tx.get("to", "").lower()
        analyzed = analyzed_address.lower()

        # Determinar dirección relativa a la dirección analizada
        if sender == analyzed:
            direction = "outgoing"
        elif receiver == analyzed:
            direction = "incoming"
        else:
            direction = "unknown"  # No debería pasar si filtramos por dirección

        # El valor viene en wei (1 ETH = 10^18 wei)
        value_wei = int(raw_tx.get("value", 0))
        amount_eth = value_wei / 1e18

        # Timestamp viene como string Unix
        timestamp = datetime.fromtimestamp(int(raw_tx.get("timeStamp", 0)))

        return Transaction(
            sender=sender,
            receiver=receiver,
            amount=amount_eth,
            timestamp=timestamp,
            tx_hash=raw_tx.get("hash", ""),
            asset="ETH",
            network="ethereum",
            direction=direction,
            raw_data=raw_tx,
        )
    except (ValueError, TypeError, KeyError):
        return None


def normalize_ethereum_transactions(
    raw_transactions: list[dict], analyzed_address: str
) -> list[Transaction]:
    """
    Normaliza una lista de transacciones crudas de Etherscan.
    Descarta las que no se pueden normalizar.

    Args:
        raw_transactions: Lista de transacciones crudas de Etherscan.
        analyzed_address: Dirección que estamos analizando.

    Returns:
        Lista de Transaction normalizadas.
    """
    normalized = []
    for raw_tx in raw_transactions:
        tx = normalize_ethereum_transaction(raw_tx, analyzed_address)
        if tx is not None:
            normalized.append(tx)
    return normalized