# 🚀 FastAPI-CV

API construida con FastAPI para procesar CVs (PDF) y generar career path con información estructurada utilizando modelos de IA de Gemini y uso de LlamaIndex para el parseo de los documentos.

---

## 📦 Requisitos

Antes de iniciar, asegúrate de tener instalado:

- Python 3.11+ (recomendado)
- pip
- virtualenv (opcional pero recomendado)

---

## ⚙️ Configuración del Proyecto

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/FastAPI-CV.git
cd FastAPI-CV
```

### 2. Crear entorno virtual (venv)
```bash
python -m venv venv
```

Activar el entorno:

# Mac / Linux
```bash
source venv/bin/activate
```

# Windows
```bash
venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Variables de entorno (.env)
Crea un archivo .env en la raíz del proyecto:
```bash
touch .env
```

Agrega las siguientes variables:
```bash
GEMINI_API_KEY=tu_api_key_de_gemini
LLAMAINDEX_API_KEY=tu_api_key_de_llamaindex
```

### ▶️ Ejecutar el proyecto
```bash
uvicorn main:app --reload
```

La API estará disponible en:
👉 http://127.0.0.1:8000

### 📚 Documentación automática
FastAPI genera documentación automáticamente:
Swagger UI: http://127.0.0.1:8000/docs
ReDoc: http://127.0.0.1:8000/redoc

### 📁 Estructura del proyecto
```bash
FastAPI-CV/
│
├── services/          # Lógica de integración con IA (Gemini, LlamaIndex, etc.)
├── main.py            # Entry point de la API
├── utils.py           # Funciones auxiliares
├── requirements.txt   # Dependencias
├── runtime.txt        # Configuración de runtime (deploy)
└── .gitignore
```

### 🧠 Tecnologías utilizadas
FastAPI
Python
Gemini API (Google)
LlamaIndex
Uvicorn
