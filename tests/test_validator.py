"""
Tests para el módulo de validación de direcciones.
"""

from app.processing.validator import is_valid_ethereum_address, normalize_address


def test_valid_ethereum_address():
    assert is_valid_ethereum_address("0x742d35Cc6634C0532925a3b844Bc454e4438f44e")
    assert is_valid_ethereum_address("0x0000000000000000000000000000000000000000")


def test_invalid_ethereum_address():
    assert not is_valid_ethereum_address("0x123")
    assert not is_valid_ethereum_address("742d35Cc6634C0532925a3b844Bc454e4438f44e")
    assert not is_valid_ethereum_address("")
    assert not is_valid_ethereum_address(None)
    assert not is_valid_ethereum_address("0xZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ")


def test_normalize_address():
    result = normalize_address("  0x742D35CC6634C0532925A3B844BC454E4438F44E  ")
    assert result == "0x742d35cc6634c0532925a3b844bc454e4438f44e"


def test_normalize_address_adds_prefix():
    result = normalize_address("742d35cc6634c0532925a3b844bc454e4438f44e")
    assert result.startswith("0x")