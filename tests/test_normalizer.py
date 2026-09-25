"""
Tests para el normalizador de transacciones.
"""

from app.processing.normalizer import normalize_ethereum_transaction


def sample_raw_tx():
    """Transacción cruda de ejemplo (formato Etherscan)."""
    return {
        "hash": "0xabc123",
        "from": "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
        "to": "0x1234567890abcdef1234567890abcdef12345678",
        "value": "1000000000000000000",
        "timeStamp": "1619737472",
        "gas": "21000",
        "gasPrice": "120000000000",
    }


def test_normalize_outgoing():
    tx = normalize_ethereum_transaction(
        sample_raw_tx(), "0xd8da6bf26964af9d7eed9e03e53415d37aa96045"
    )
    assert tx is not None
    assert tx.direction == "outgoing"
    assert tx.amount == 1.0
    assert tx.asset == "ETH"
    assert tx.network == "ethereum"


def test_normalize_incoming():
    tx = normalize_ethereum_transaction(
        sample_raw_tx(), "0x1234567890abcdef1234567890abcdef12345678"
    )
    assert tx is not None
    assert tx.direction == "incoming"


def test_normalize_invalid_data():
    tx = normalize_ethereum_transaction({}, "0xabc")
    assert tx is None or tx is not None