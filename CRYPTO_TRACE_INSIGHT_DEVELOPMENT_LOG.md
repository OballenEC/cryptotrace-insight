# CryptoTrace Insight — Development Log

Bitácora de desarrollo del proyecto para GOYA HACK 2026.

---

## 📋 Información del proyecto

- **Proyecto**: CryptoTrace Insight
- **Evento**: GOYA HACK 2026 (CriptoUNAM — Facultad de Ingeniería, UNAM)
- **Autor**: Oscar Ballen
- **Repositorio**: [GitHub](https://github.com/tu-usuario/cryptotrace-insight)
- **Stack**: Python, Streamlit, NetworkX, PyVis, Etherscan API, Stellar SDK
- **Duración del sprint**: ~12 horas

---

## 🎯 Objetivo

Desarrollar una herramienta open-source en Python para explorar actividad blockchain mediante datos transaccionales, grafos y heurísticas explicables, con arquitectura extensible a múltiples redes (Ethereum, Stellar).

---

## 📅 Milestones

### ✅ P0 — Project Setup
**Estado**: Completado

**Implementado**:
- Estructura de carpetas: `app/`, `tests/`, `data/`
- Archivos `__init__.py` en todos los paquetes
- `.gitignore`, `.env`, `requirements.txt`
- `README.md` inicial
- Entorno virtual con dependencias (streamlit, requests, networkx, pyvis, python-dotenv, pytest)
- Repositorio Git inicializado

**Decisiones importantes**:
- Arquitectura modular por capas
- Uso de dataclasses para modelos
- Codificación UTF-8 para todos los archivos

---

### ✅ P1 — Ethereum API + Normalization
**Estado**: Completado

**Implementado**:
- `app/models/transaction.py`: Modelo `Transaction` normalizado
- `app/processing/validator.py`: Validación de direcciones Ethereum
- `app/api/etherscan.py`: Cliente de Etherscan API V2
- `app/processing/normalizer.py`: Conversión de transacciones crudas a `Transaction`

**Decisiones importantes**:
- Migración a Etherscan API V2 (requiere `chainid`)
- Conversión de `value` de wei a ETH (`/ 1e18`)
- Determinación de `direction` según dirección analizada
- Manejo específico de errores

**Evidencia**:
- Consulta a Vitalik Buterin: 10 transacciones normalizadas

---

### ✅ P2 — Transaction Graph Builder
**Estado**: Completado

**Implementado**:
- `app/graph/builder.py`: Grafo dirigido con NetworkX
- `graph_summary()`: Resumen con nodos, aristas y transacciones

**Decisiones importantes**:
- Grafo dirigido (`nx.DiGraph`)
- Aristas acumulativas con hashes y timestamps para evidencia

---

### ✅ P3 — Heuristic: Fan-out Pattern
**Estado**: Completado

**Implementado**:
- `app/models/finding.py`: Modelo `Finding`
- `app/heuristics/base.py`: Interfaz abstracta
- `app/heuristics/fanout.py`: Umbral ≥5 destinatarios únicos

**Decisiones importantes**:
- Lenguaje cuidadoso: "patrón observado", nunca "fraude detectado"
- Hallazgos incluyen explicación y limitación

---

### ✅ P4 — Heuristic: High Velocity Pattern
**Estado**: Completado

**Implementado**:
- `app/heuristics/velocity.py`: Ráfagas de transacciones
- Umbrales: ≥5 transacciones en ≤10 minutos
- Ventana deslizante sobre timestamps ordenados

---

### ✅ P5 — Heuristic: Similar Amounts Pattern
**Estado**: Completado

**Implementado**:
- `app/heuristics/similar_amounts.py`: Montos similares
- Umbral: ≥4 transferencias con diferencia ≤5%
- Algoritmo de agrupación por similitud

---

### ✅ P6 — Streamlit UI
**Estado**: Completado

**Implementado**:
- `app/main.py`: Interfaz web completa
- Formulario de entrada: dirección + red
- Visualización de resumen con 4 métricas
- Sección de hallazgos con tarjetas expandibles

**Evidencia**:
- Vitalik: 100 transacciones, 17 direcciones, 2 hallazgos
- Binance: 100 transacciones, 15 direcciones, 2 hallazgos

**Aprendizajes**:
- `sys.path.insert` necesario para imports absolutos en Streamlit
- Streamlit bloquea la terminal mientras corre (usar segunda terminal para Git)

---

### ✅ P7 — Graph Visualization (PyVis)
**Estado**: Completado

**Implementado**:
- `app/visualization/graph_view.py`: Renderizado interactivo
- Nodos coloreados: rojo (analizada), naranja (top 3), azul (resto)
- Grosor de aristas proporcional al volumen

**Evidencia**:
- Grafo interactivo funcional con zoom y hover

---

### ✅ P8 — Tests + Error Handling
**Estado**: Completado

**Implementado**:
- `tests/test_validator.py`: 4 tests
- `tests/test_normalizer.py`: 3 tests
- `tests/test_heuristics.py`: 6 tests
- Total: **13 tests unitarios pasando en 0.28s**

---

### ✅ P9 — Offline Dataset
**Estado**: Completado

**Implementado**:
- `data/sample_ethereum_transactions.json` con 50 transacciones
- 63 KB de datos reales guardados como respaldo

---

### ✅ P10 — Documentation
**Estado**: Completado

**Implementado**:
- `README.md` completo
- `.env.example` como plantilla pública
- Development Log completo

---

### ✅ P11 — Stellar Integration
**Estado**: Completado

**Implementado**:
- `app/api/stellar.py`: Cliente de Horizon (transacciones y pagos)
- `normalize_stellar_payment()` en `app/processing/normalizer.py`
- `is_valid_stellar_address()` en `app/processing/validator.py`
- Selector de red en la UI (Ethereum / Stellar)
- Lógica condicional en `app/main.py`

**Decisiones importantes**:
- Uso de Horizon por practicidad en hackathon (documentado que migrará a Stellar RPC)
- Endpoint `payments()` en lugar de `transactions()` porque devuelve from/to/amount directamente
- Validación de formato: G + 55 caracteres
- El modelo `Transaction` y el grafo son **agnósticos a la red**

**Evidencia**:
- Cuenta de prueba: GASOCN...EDW
- 2 pagos normalizados y mostrados en la UI
- Grafo interactivo funcional con datos de Stellar

**Aprendizajes**:
- El SDK `stellar-sdk` usa Builder pattern (`.for_account().limit().call()`)
- Horizon devuelve `_embedded.records` con los datos
- Stellar usa ISO timestamps con `Z` al final (UTC)

---

### ✅ P12 — Offline Demo Mode
**Estado**: Completado

**Implementado**:
- Checkbox "Usar datos offline (modo demo)" en la UI
- Carga de `data/sample_ethereum_transactions.json` en lugar de consultar la API
- Timeout de Etherscan reducido de 15s a 8s
- Script `test_debug_eth.py` para diagnóstico offline

**Decisión estratégica**:
- La demo del hackathon usará modo offline para garantizar reproducibilidad
- En producción, la app consulta Etherscan en tiempo real

**Aprendizajes**:
- Etherscan puede tardar mucho o bloquear la IP temporalmente por rate limit
- Un modo offline es esencial para demos en vivo sin depender de la red
- Timeout agresivo evita que la UI se quede colgada

---

### ⚠️ P13 — Network Issue with Etherscan API
**Estado**: Documentado (no bloqueante)

**Problema**:
- A partir del 24/09/2026, la conexión a `api.etherscan.io` desde la red local comenzó a dar timeout
- El error es `ConnectTimeoutError`, no relacionado con la API key ni con el código
- El DNS resuelve correctamente (varias IPs), pero la conexión TCP no se completa
- Posible causa: rate limit por IP o bloqueo del ISP/router

**Mitigación implementada**:
- Modo offline con dataset previamente consultado
- Timeout reducido a 8 segundos para evitar bloqueos largos
- La demo del hackathon usará modo offline

**Aprendizaje**:
- Depender de APIs externas en una demo en vivo es riesgoso
- Un modo offline es esencial para hackathons
- Documentar limitaciones conocidas es parte del profesionalismo

---

## 🧠 Aprendizajes y notas

- **PowerShell**: no pegar código Python en la terminal. Solo comandos.
- **VS Code**: aquí va el código Python.
- **Git**: usar `--no-pager` para evitar el paginador `less`.
- **Etherscan V2**: requiere `chainid`. Ethereum Mainnet = 1.
- **Python 3.14**: funciona con el stack actual.
- **UTF-8**: configurar VS Code para evitar problemas con acentos.
- **Multi-chain**: el modelo `Transaction` y el grafo son agnósticos a la red.

---

## 📚 Referencias

- [Etherscan API Docs](https://docs.etherscan.io/)
- [NetworkX Docs](https://networkx.org/documentation/stable/)
- [Streamlit Docs](https://docs.streamlit.io/)
- [PyVis Docs](https://pyvis.readthedocs.io/)
- [Stellar Horizon API Docs](https://developers.stellar.org/docs/data/apis/horizon)