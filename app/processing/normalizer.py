"""
Normalizador de transacciones blockchain.

Convierte los datos crudos de las APIs (Etherscan, Stellar, etc.)
a nuestro modelo `Transaction` normalizado.
"""

from datetime import datetime
from typing import Optional

from app.models.transaction import Transaction


# ============================================================
# Ethereum
# ============================================================

def normalize_ethereum_transaction(
    raw_tx: dict, analyzed_address: str
) -> Optional[Transaction]:
    """
    Convierte una transacción cruda de Etherscan a nuestro modelo normalizado.
    """
    try:
        sender = raw_tx.get("from", "").lower()
        receiver = raw_tx.get("to", "").lower()
        analyzed = analyzed_address.lower()

        if sender == analyzed:
            direction = "outgoing"
        elif receiver == analyzed:
            direction = "incoming"
        else:
            direction = "unknown"

        value_wei = int(raw_tx.get("value", 0))
        amount_eth = value_wei / 1e18

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
    raw_transactions: list, analyzed_address: str
) -> list:
    """
    Normaliza una lista de transacciones crudas de Etherscan.
    """
    normalized = []
    for raw_tx in raw_transactions:
        tx = normalize_ethereum_transaction(raw_tx, analyzed_address)
        if tx is not None:
            normalized.append(tx)
    return normalized


# ============================================================
# Stellar
# ============================================================

def normalize_stellar_payment(
    raw_payment: dict, analyzed_address: str
) -> Optional[Transaction]:
    """
    Convierte un pago crudo de Stellar a nuestro modelo Transaction.
    """
    try:
        sender = raw_payment.get("from", "")
        receiver = raw_payment.get("to", "")

        if sender == analyzed_address:
            direction = "outgoing"
        elif receiver == analyzed_address:
            direction = "incoming"
        else:
            direction = "unknown"

        amount = float(raw_payment.get("amount", 0))
        asset = raw_payment.get("asset_code", "XLM")

        created_at = raw_payment.get("created_at", "")
        timestamp = datetime.fromisoformat(created_at.replace("Z", "+00:00"))

        return Transaction(
            sender=sender,
            receiver=receiver,
            amount=amount,
            timestamp=timestamp,
            tx_hash=raw_payment.get("transaction_hash", ""),
            asset=asset,
            network="stellar",
            direction=direction,
            raw_data=raw_payment,
        )
    except (ValueError, TypeError, KeyError):
        return None


def normalize_stellar_payments(raw_payments: list, analyzed_address: str) -> list:
    """
    Normaliza una lista de pagos crudos de Stellar.
    """
    normalized = []
    for raw in raw_payments:
        tx = normalize_stellar_payment(raw, analyzed_address)
        if tx is not None:
            normalized.append(tx)
    return normalized