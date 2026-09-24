# CryptoTrace Insight — Development Log

Bitácora de desarrollo del proyecto para GOYA HACK 2026.

---

## 📋 Información del proyecto

- **Proyecto**: CryptoTrace Insight
- **Evento**: GOYA HACK 2026 (CriptoUNAM — Facultad de Ingeniería, UNAM)
- **Autor**: Oscar
- **Repositorio**: [GitHub](https://github.com/tu-usuario/cryptotrace-insight)
- **Stack**: Python, Streamlit, NetworkX, PyVis, Etherscan API
- **Duración del sprint**: ~12 horas

---

## 🎯 Objetivo

Desarrollar una herramienta open-source en Python para explorar actividad blockchain mediante datos transaccionales, grafos y heurísticas explicables, con arquitectura extensible a múltiples redes (Ethereum, Stellar).

---

## 📅 Milestones

### ✅ P0 — Project Setup
**Fecha**: 2026-09-24
**Objetivo**: Crear estructura base, configurar Git y entorno virtual.

**Implementado**:
- Estructura de carpetas: `app/`, `tests/`, `data/`
- Archivos `__init__.py` en todos los paquetes
- `.gitignore` configurado
- `requirements.txt` con dependencias iniciales
- `README.md` inicial
- `.env` configurado (no trackeado por Git)
- Development Log inicial

**Decisiones importantes**:
- Arquitectura modular por capas (api, models, processing, graph, heuristics, visualization)
- Modelo `Transaction` normalizado como contrato entre capas
- Uso de dataclasses para modelos

**Git commit**: `8c7a39f`

**Próximo paso**: Crear venv, instalar dependencias, inicializar Git.

---

### ⏳ P1 — Ethereum API + Normalization
**Estado**: Pendiente

---

### ⏳ P2 — Transaction Processing
**Estado**: Pendiente

---

### ⏳ P3 — Graph Builder
**Estado**: Pendiente

---

### ⏳ P4 — Heuristic: Fan-out
**Estado**: Pendiente

---

### ⏳ P5 — Heuristic: Velocity
**Estado**: Pendiente

---

### ⏳ P6 — Heuristic: Similar Amounts
**Estado**: Pendiente

---

### ⏳ P7 — Streamlit UI
**Estado**: Pendiente

---

### ⏳ P8 — Graph Visualization
**Estado**: Pendiente

---

### ⏳ P9 — Error Handling + Tests
**Estado**: Pendiente

---

### ⏳ P10 — Stellar Integration (opcional)
**Estado**: Pendiente

---

### ⏳ P11 — Documentation + Demo
**Estado**: Pendiente

---

## 🧠 Aprendizajes y notas

(Espacio para registrar problemas resueltos, decisiones técnicas y hallazgos durante el desarrollo.)

---

## 📚 Referencias

- [Etherscan API Docs](https://docs.etherscan.io/)
- [Stellar Horizon API Docs](https://developers.stellar.org/docs/data/apis/horizon)
- [NetworkX Docs](https://networkx.org/documentation/stable/)
- [Streamlit Docs](https://docs.streamlit.io/)
- [PyVis Docs](https://pyvis.readthedocs.io/)