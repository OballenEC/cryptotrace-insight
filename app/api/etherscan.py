"""
Cliente de la API de Etherscan V2.

Consulta las transacciones normales (envíos y recepciones de ETH)
de una dirección Ethereum.
"""

import os
import requests
from dotenv import load_dotenv


# Cargar variables de entorno desde .env
load_dotenv()

ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")
# URL base de la API V2
ETHERSCAN_BASE_URL = "https://api.etherscan.io/v2/api"
# Chain ID de Ethereum Mainnet
ETHEREUM_CHAIN_ID = 1


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
        "chainid": ETHEREUM_CHAIN_ID,
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

    if data.get("status") == "0":
        message = data.get("message", "")
        result = data.get("result", "")

        if message == "No transactions found":
            return []

        if "rate limit" in str(result).lower():
            raise EtherscanError(
                "Rate limit alcanzado. Espera unos segundos y vuelve a intentar."
            )

        if "invalid api key" in str(result).lower():
            raise EtherscanError(
                "API Key inválida. Verifica tu clave en .env."
            )

        raise EtherscanError(f"Error de Etherscan: {message} - {result}")

    results = data.get("result", [])
    if not isinstance(results, list):
        raise EtherscanError(f"Respuesta inesperada de Etherscan: {results}")

    return results[:max_results]