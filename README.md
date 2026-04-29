# M.A.D.R.A. — Motor de Análisis de Dependencia y Ruta de Ataque

<br>
<a href="https://www.linkedin.com/in/ldmsboy"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"></a>
<a href="https://peerlist.io/ldmsboy"><img src="https://img.shields.io/badge/Peerlist-00CA51?style=for-the-badge&logo=peerlist&logoColor=white" alt="Peerlist"></a>
<a href="https://x.com/LuisDaniel38815"><img src="https://img.shields.io/badge/X-000000?style=for-the-badge&logo=x&logoColor=white" alt="X"></a>
<a href="https://www.instagram.com/ldmsboy/"><img src="https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white" alt="Instagram"></a>
<a href="https://www.facebook.com/ldmsboy/"><img src="https://img.shields.io/badge/Facebook-1877F2?style=for-the-badge&logo=facebook&logoColor=white" alt="Facebook"></a>
<br><br>

Proyecto de ejemplo que modela una red de activos de ciberseguridad como un grafo dirigido ponderado y encuentra la ruta de explotación de menor costo usando Dijkstra.

Estructura minimal:

- `app.py` — Flask backend y API.
- `graph_analyzer.py` — Implementación de la clase GraphAnalyzer con Dijkstra.
- `network_data.json` — Datos de ejemplo del grafo.
- `static/` — Archivos estáticos: `index.html`, `main.js`, `styles.css`, `vis-network.min.js` (CDN used in HTML).
- `requirements.txt` — Dependencias.

Requisitos:

- Python 3.8+
- Instalar dependencias: pip install -r requirements.txt


Cómo ejecutar:

1. Crear un entorno virtual e instalar dependencias:

```powershell
python -m venv .venv; .venv\Scripts\Activate.ps1; pip install -r requirements.txt
```

1. Exportar variable y ejecutar Flask (Windows PowerShell):

```powershell
set FLASK_APP=app.py; flask run
```

1. Abrir <http://127.0.0.1:5000/>

API endpoints:

- `GET /data` — Devuelve el grafo cargado desde `network_data.json`.
- `POST /analyze` — JSON body: {"start": "NodoA", "end": "NodoB"}. Devuelve ruta, costo y aristas críticas.

Ejemplo de uso con curl (PowerShell):

```powershell
curl -Method POST -Body (@{start='Workstation1';end='DB_Finanzas'} | ConvertTo-Json) -ContentType 'application/json' http://127.0.0.1:5000/analyze
```


Notas:

- Implementación limpia y comentada del Algoritmo de Dijkstra en `graph_analyzer.py`.
