"""
Script de prueba para normalización de Stellar.
"""

from app.api.stellar import fetch_stellar_payments
from app.processing.normalizer import normalize_stellar_payments


def main():
    account = "GASOCNHNNLYFNMDJYQ3XFMI7BYHIOCFW3GJEOWRPEGK2TDPGTG2E5EDW"

    print(f"Consultando pagos de: {account}")
    raw = fetch_stellar_payments(account, max_results=10)
    print(f"Pagos crudos: {len(raw)}")

    txs = normalize_stellar_payments(raw, account)
    print(f"Pagos normalizados: {len(txs)}")
    print()

    for tx in txs[:5]:
        print(f"  {tx.summary()}")


if __name__ == "__main__":
    main()