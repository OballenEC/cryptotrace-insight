"""
Cliente de la API de Stellar (Horizon).

Consulta las transacciones y operaciones de pago de una cuenta Stellar.
"""

from stellar_sdk import Server, StrKey

# URL de Horizon para la testnet de Stellar
STELLAR_HORIZON_URL = "https://horizon-testnet.stellar.org"


class StellarError(Exception):
    """Error específico de la API de Stellar."""
    pass


def fetch_stellar_transactions(account_id: str, max_results: int = 50) -> list:
    """
    Consulta las transacciones de una cuenta Stellar.
    """
    if not StrKey.is_valid_ed25519_public_key(account_id):
        raise StellarError(
            f"Dirección Stellar inválida: {account_id}. "
            "Debe empezar con 'G' y tener 56 caracteres."
        )

    server = Server(horizon_url=STELLAR_HORIZON_URL)

    try:
        transactions = (
            server.transactions()
            .for_account(account_id)
            .order(desc=True)
            .limit(max_results)
            .call()
        )
    except Exception as e:
        raise StellarError(f"Error al consultar Stellar: {e}")

    records = transactions.get("_embedded", {}).get("records", [])
    return records


def fetch_stellar_payments(account_id: str, max_results: int = 50) -> list:
    """
    Consulta los pagos (operaciones de transferencia) de una cuenta Stellar.
    """
    if not StrKey.is_valid_ed25519_public_key(account_id):
        raise StellarError(
            f"Dirección Stellar inválida: {account_id}. "
            "Debe empezar con 'G' y tener 56 caracteres."
        )

    server = Server(horizon_url=STELLAR_HORIZON_URL)

    try:
        payments = (
            server.payments()
            .for_account(account_id)
            .order(desc=True)
            .limit(max_results)
            .call()
        )
    except Exception as e:
        raise StellarError(f"Error al consultar pagos de Stellar: {e}")

    records = payments.get("_embedded", {}).get("records", [])
    return records