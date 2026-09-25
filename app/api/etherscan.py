"""
Cliente de la API de Etherscan.

Consulta las transacciones normales (envíos y recepciones de ETH)
de una dirección Ethereum.
"""

import os
import requests
from dotenv import load_dotenv


# Cargar variables de entorno desde .env
load_dotenv()

ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")
ETHERSCAN_BASE_URL = "https://api.etherscan.io/api"


class EtherscanError(Exception):
    """Error específico de la API de Etherscan."""
    pass


def fetch_transactions(address: str, max_results: int = 100) -> list[dict]:
    """
    Consulta las transacciones normales de una dirección Ethereum.

    Args:
        address: Dirección Ethereum (0x...).
        max_results: Número máximo de transacciones a devolver.

    Returns:
        Lista de diccionarios con las transacciones crudas de Etherscan.

    Raises:
        EtherscanError: Si la API key no está configurada o la API responde con error.
    """
    if not ETHERSCAN_API_KEY:
        raise EtherscanError(
            "ETHERSCAN_API_KEY no está configurada. "
            "Crea un archivo .env con tu API key."
        )

    params = {
        "module": "account",
        "action": "txlist",
        "address": address,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "asc",
        "apikey": ETHERSCAN_API_KEY,
    }

    try:
        response = requests.get(ETHERSCAN_BASE_URL, params=params, timeout=15)
        response.raise_for_status()
    except requests.RequestException as e:
        raise EtherscanError(f"Error de conexión con Etherscan: {e}")

    data = response.json()

    # Etherscan devuelve status "0" con message "No transactions found" cuando no hay datos
    if data.get("status") == "0":
        message = data.get("message", "")
        if message == "No transactions found":
            return []
        raise EtherscanError(f"Error de Etherscan: {message}")

    results = data.get("result", [])
    if not isinstance(results, list):
        raise EtherscanError(f"Respuesta inesperada de Etherscan: {results}")

    return results[:max_results]