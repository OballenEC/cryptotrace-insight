# CryptoTrace Insight

> Herramienta open-source en Python para explorar actividad blockchain mediante grafos de transacciones y heurísticas explicables.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Hackathon](https://img.shields.io/badge/GOYA%20HACK-2026-purple.svg)]()

---

## 🎯 ¿Qué es CryptoTrace Insight?

CryptoTrace Insight es una herramienta de exploración y análisis de actividad blockchain. Permite a cualquier persona **investigar una dirección de wallet** para visualizar el flujo de fondos, detectar patrones observables y entender por qué fueron marcados.

**No es** una wallet, no custodia fondos, no calcula impuestos y no determina criminalidad. Es una herramienta de **exploración transparente y educativa**.

---

## 🚧 Estado del proyecto

🚧 **En desarrollo activo** — Proyecto para GOYA HACK 2026 (CriptoUNAM, Facultad de Ingeniería, UNAM).

---

## 🔍 ¿Qué problema resuelve?

La actividad en blockchain es pública pero difícil de interpretar. Las herramientas empresariales de análisis forense son costosas y cerradas. CryptoTrace Insight ofrece una alternativa **open-source, accesible y visual** para entender el flujo de transacciones.

---

## 🛠️ Stack tecnológico

- **Python 3.10+**
- **Streamlit** — Interfaz web
- **Requests** — Consumo de APIs
- **NetworkX** — Análisis de grafos
- **PyVis** — Visualización interactiva
- **Etherscan API** — Datos de Ethereum

---

## 📦 Instalación

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/cryptotrace-insight.git
cd cryptotrace-insight

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual (Windows)
venv\Scripts\activate

# Activar entorno virtual (Mac/Linux)
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar API key
cp .env.example .env
# Editar .env y añadir tu ETHERSCAN_API_KEY