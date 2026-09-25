# CryptoTrace Insight — Development Log

Bitácora de desarrollo del proyecto para GOYA HACK 2026.

---

## 📋 Información del proyecto

- **Proyecto**: CryptoTrace Insight
- **Evento**: GOYA HACK 2026 (CriptoUNAM — Facultad de Ingeniería, UNAM)
- **Autor**: Oscar Ballen
- **Repositorio**: [GitHub](https://github.com/tu-usuario/cryptotrace-insight)
- **Stack**: Python, Streamlit, NetworkX, PyVis, Etherscan API
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
- Repositorio Git inicializado con commits iniciales

**Decisiones importantes**:
- Arquitectura modular por capas
- Uso de dataclasses para modelos
- Codificación UTF-8 para todos los archivos

---

### ✅ P1 — Ethereum API + Normalization
**Estado**: Completado

**Implementado**:
- `app/models/transaction.py`: Modelo `Transaction` normalizado con dataclass
- `app/processing/validator.py`: Validación de direcciones Ethereum con regex
- `app/api/etherscan.py`: Cliente de Etherscan API V2 con manejo de errores
- `app/processing/normalizer.py`: Conversión de transacciones crudas a `Transaction`

**Decisiones importantes**:
- Migración a Etherscan API V2 (requiere `chainid` obligatorio)
- Conversión de `value` de wei a ETH (`/ 1e18`)
- Determinación de `direction` (incoming/outgoing) según dirección analizada
- Manejo específico de errores: rate limit, API key inválida, sin transacciones

**Aprendizajes**:
- La API V1 de Etherscan fue deprecada; ahora es obligatorio usar V2 con `chainid`
- Python 3.14 funciona correctamente con el stack elegido
- Las direcciones de exchanges tienen miles de transacciones (JSON gigante)

**Evidencia**:
- Consulta exitosa a dirección de Vitalik Buterin: 10 transacciones normalizadas
- Outgoing: 9, Incoming: 1

---

### ✅ P2 — Transaction Graph Builder
**Estado**: Completado

**Implementado**:
- `app/graph/builder.py`: Construcción de grafo dirigido con NetworkX
- `graph_summary()`: Resumen con nodos, aristas y transacciones totales
- Aristas acumulativas: si hay múltiples transacciones entre mismas direcciones, se acumulan montos y se guardan todos los hashes

**Decisiones importantes**:
- Grafo dirigido (`nx.DiGraph`) porque las transacciones tienen dirección
- Cada arista guarda: `total_amount`, `tx_count`, `tx_hashes`, `timestamps`
- Los hashes y timestamps se conservan para evidencia

**Evidencia**:
- Consulta a Vitalik: 10 transacciones → 4 nodos, 3 aristas
- Ejemplo: `0xd8da... → 0x7e2d...` (6 transacciones, 0.00037 ETH)

---

### ✅ P3 — Heuristic: Fan-out Pattern
**Estado**: Completado

**Implementado**:
- `app/models/finding.py`: Modelo `Finding` para representar hallazgos
- `app/heuristics/base.py`: Interfaz abstracta `Heuristic`
- `app/heuristics/fanout.py`: Detección de direcciones que envían a ≥5 destinatarios únicos

**Decisiones importantes**:
- Umbral configurable: `FANOUT_THRESHOLD = 5`
- Los hallazgos incluyen: explicación, limitación, evidencia (hashes)
- Lenguaje cuidadoso: "patrón observado", nunca "fraude detectado"

**Aprendizajes**:
- El paginador de Git (`less`) atrapa al usuario; usar `git --no-pager log` o `git config --global core.pager ""`
- La carpeta se llamaba `huristics` (typo); corregido a `heuristics`

**Evidencia**:
- Dirección de Vitalik: 0 hallazgos (no tiene fan-out)
- Heurística funcional y probada

---

### ✅ P4 — Heuristic: High Velocity Pattern
**Estado**: Completado

**Implementado**:
- `app/heuristics/velocity.py`: Detección de ráfagas de transacciones
- Umbrales: `VELOCITY_THRESHOLD_COUNT = 5`, `VELOCITY_THRESHOLD_MINUTES = 10`
- Algoritmo de ventana deslizante sobre timestamps ordenados
- Análisis tanto de transacciones entrantes como salientes

**Decisiones importantes**:
- Se analizan tanto in-edges como out-edges de la dirección analizada
- Se identifica el intervalo con mayor concentración de transacciones
- Se reporta el período exacto (start → end)

**Aprendizajes**:
- Ventana deslizante es más eficiente que revisar todas las combinaciones
- Los timestamps deben ordenarse antes del análisis

---

### ✅ P5 — Heuristic: Similar Amounts Pattern
**Estado**: Completado

**Implementado**:
- `app/heuristics/similar_amounts.py`: Detección de montos similares
- Umbral: ≥4 transferencias con diferencia ≤5%
- Algoritmo de agrupación por similitud

---

### ✅ P6 — Streamlit UI
**Estado**: Completado

**Implementado**:
- `app/main.py`: Interfaz web completa
- Formulario de entrada: dirección + red
- Validación de dirección en tiempo real
- Visualización de resumen con 4 métricas
- Sección de hallazgos con tarjetas expandibles
- Manejo de errores (dirección inválida, rate limit, sin transacciones)

**Evidencia**:
- Vitalik: 100 transacciones, 17 direcciones únicas, 17 relaciones, 2 hallazgos
- Binance: 100 transacciones, 15 direcciones únicas, 14 relaciones, 2 hallazgos

**Aprendizajes**:
- Streamlit bloquea la terminal mientras corre (usar segunda terminal para Git)
- `sys.path.insert` necesario para imports absolutos en Streamlit
- Codificación UTF-8 crítica para caracteres especiales

---

### ⏳ P7 — Graph Visualization
**Estado**: Pendiente

---

### ⏳ P8 — Error Handling + Tests
**Estado**: Pendiente

---

### ⏳ P9 — Stellar Integration (opcional)
**Estado**: Pendiente

---

### ⏳ P10 — Documentation + Demo
**Estado**: Pendiente

---

## 🧠 Aprendizajes y notas

- **PowerShell**: no pegar código Python en la terminal. Solo comandos.
- **VS Code**: aquí va el código Python.
- **Git**: usar `--no-pager` para evitar el paginador `less`.
- **Etherscan V2**: requiere `chainid`. Ethereum Mainnet = 1.
- **Python 3.14**: funciona con el stack actual.
- **UTF-8**: configurar VS Code para evitar problemas con acentos.

---

## 📚 Referencias

- [Etherscan API Docs](https://docs.etherscan.io/)
- [NetworkX Docs](https://networkx.org/documentation/stable/)
- [Streamlit Docs](https://docs.streamlit.io/)
- [PyVis Docs](https://pyvis.readthedocs.io/)
- [Stellar Horizon API Docs](https://developers.stellar.org/docs/data/apis/horizon)