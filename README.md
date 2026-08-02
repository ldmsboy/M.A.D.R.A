# 🕸️ M.A.D.R.A. — Motor de Análisis de Dependencia y Ruta de Ataque

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-yellow?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.x-black?style=for-the-badge&logo=flask)
![JavaScript](https://img.shields.io/badge/Vis.js-Network-blue?style=for-the-badge)
![Cybersecurity](https://img.shields.io/badge/Domain-Cybersecurity-red?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-brightgreen?style=for-the-badge)

Plataforma de ciberseguridad que modela la infraestructura de activos como un **grafo dirigido ponderado** y calcula la ruta de explotación de menor costo (*Attack Path*) utilizando el **Algoritmo de Dijkstra**.

<br>
<a href="https://www.linkedin.com/in/ldmsboy"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"></a>
<a href="https://peerlist.io/ldmsboy"><img src="https://img.shields.io/badge/Peerlist-00CA51?style=for-the-badge&logo=peerlist&logoColor=white" alt="Peerlist"></a>
<a href="https://x.com/LuisDaniel38815"><img src="https://img.shields.io/badge/X-000000?style=for-the-badge&logo=x&logoColor=white" alt="X"></a>

</div>

---

## 🎯 Descripción y Enfoque

M.A.D.R.A. permite a los analistas de seguridad y Blue Teams evaluar el riesgo acumulado en redes corporativas. En lugar de evaluar vulnerabilidades de forma aislada, modela la interconexión entre sistemas (Workstations, Servidores Web, Bases de Datos) y calcula el camino óptimo que seguiría un atacante para comprometer un activo crítico.

```
[ Workstation1 ] ──(Costo: 2)──> [ Web_Server ] ──(Costo: 5)──> [ DB_Finanzas ]
```

---

## 🏗️ Estructura del Repositorio

- `app.py` — Servidor API REST en Flask.
- `graph_analyzer.py` — Implementación limpia de la clase `GraphAnalyzer` con el Algoritmo de Dijkstra.
- `network_data.json` — Definición de nodos (activos) y aristas (vectores de ataque con peso).
- `static/` — Frontend interactivo (`index.html`, `main.js`, `styles.css`, visualización de grafos con `vis-network`).
- `requirements.txt` — Dependencias de Python.

---

## 🚀 Requisitos e Instalación

### Prerrequisitos
* Python 3.8 o superior

### Instrucciones de Ejecución

1. **Crear entorno virtual e instalar dependencias:**
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

2. **Iniciar servidor Flask (Windows PowerShell):**
   ```powershell
   $env:FLASK_APP="app.py"
   flask run
   ```

3. **Abrir en navegador:**
   Navega a `http://127.0.0.1:5000/`

---

## 📡 API Endpoints

- `GET /data`: Retorna la topología completa del grafo cargada desde `network_data.json`.
- `POST /analyze`: Recibe `{"start": "Workstation1", "end": "DB_Finanzas"}` y calcula la ruta crítica, costo total y aristas involucradas.

### Ejemplo de consulta con `curl` (PowerShell):
```powershell
curl -Method POST -Body (@{start='Workstation1';end='DB_Finanzas'} | ConvertTo-Json) -ContentType 'application/json' http://127.0.0.1:5000/analyze
```

---

## 📄 Licencia
Licencia **MIT**.

---
<div align="center">
Desarrollado por <b>Luis Mendez</b> (@ldmsboy)
</div>
