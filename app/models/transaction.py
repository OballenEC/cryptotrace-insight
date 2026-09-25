"""
Modelo normalizado de transacción blockchain.

Independiente de la red de origen (Ethereum, Stellar, etc.).
Todas las capas del sistema (API, processing, graph, heuristics)
trabajan con este modelo común.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Transaction:
    """
    Representa una transacción blockchain normalizada.

    Attributes:
        sender: Dirección que envía los fondos (en minúsculas).
        receiver: Dirección que recibe los fondos (en minúsculas).
        amount: Cantidad transferida (en unidades del activo, no en wei).
        timestamp: Fecha y hora de la transacción (UTC).
        tx_hash: Hash único de la transacción en la blockchain.
        asset: Símbolo del activo (ETH, XLM, USDC, etc.).
        network: Red de origen (ethereum, stellar, etc.).
        direction: Relativo a la dirección analizada ("incoming" o "outgoing").
        raw_data: Diccionario original de la API, para evidencia.
    """

    sender: str
    receiver: str
    amount: float
    timestamp: datetime
    tx_hash: str
    asset: str
    network: str
    direction: str
    raw_data: Optional[dict] = field(default=None, repr=False)

    def is_outgoing(self) -> bool:
        """True si la dirección analizada envió los fondos."""
        return self.direction == "outgoing"

    def is_incoming(self) -> bool:
        """True si la dirección analizada recibió los fondos."""
        return self.direction == "incoming"

    def summary(self) -> str:
        """Resumen legible de la transacción."""
        return (
            f"[{self.direction.upper()}] "
            f"{self.amount:.6f} {self.asset} | "
            f"{self.timestamp.isoformat()} | "
            f"{self.tx_hash[:10]}..."
        )