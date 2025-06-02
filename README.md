# Anomaly Detection MCP Server

Este proyecto implementa un servidor MCP (Machine-assisted Conversational Protocol) especializado en la detección de anomalías en datos de sensores. El servidor proporciona herramientas que pueden ser utilizadas por modelos de lenguaje (LLMs) para analizar datos de sensores, detectar anomalías y sugerir acciones correctivas.

## Visión General

El servidor MCP actúa como un punto centralizado para la detección de anomalías, permitiendo que múltiples aplicaciones cliente (a través de LLMs) accedan a estas capacidades sin necesidad de implementar su propia lógica de análisis.

### Características Principales

- Recuperación de datos de sensores de diversas fuentes
- Preprocesamiento flexible de datos
- Detección de anomalías mediante diversos algoritmos
- Generación de visualizaciones de anomalías
- Ejecución de comandos correctivos (simulados o reales)

## Arquitectura

El servidor MCP proporciona tres tipos principales de capacidades:
1. **Herramientas (Tools)**: Funciones que los LLMs pueden invocar
2. **Recursos (Resources)**: Datos estructurados para apoyar el análisis
3. **Plantillas (Prompts)**: Instrucciones predefinidas para tareas específicas

### Flujo de Trabajo

1. Usuario pregunta al LLM (por ejemplo, "¿Hay anomalías en la temperatura?")
2. LLM consulta herramientas disponibles en el servidor MCP
3. LLM utiliza herramientas para obtener datos, analizarlos y detectar anomalías
4. LLM sugiere acciones correctivas si se detectan anomalías
5. LLM presenta resultados al usuario en lenguaje natural

### Componentes Clave

- **FastMCP Server**: Núcleo del servidor que expone las capacidades
- **Data Access Layer**: Interfaces con diversas fuentes de datos
- **Processing Pipeline**: Preprocesamiento y análisis de datos
- **Command Execution Module**: Ejecución de acciones correctivas
- **Visualization Engine**: Generación de gráficos e informes visuales

## Instalación

### Requisitos

```
Python 3.9+
PostgreSQL
```

### Dependencias

```
fastmcp
pandas
scikit-learn
matplotlib
plotly
httpx
sqlalchemy
```

### Configuración

1. Clonar el repositorio
2. Instalar dependencias: `pip install -r requirements.txt`
3. Configurar conexión a bases de datos en `config.yaml`
4. Iniciar el servidor: `python anomaly_detection_server.py`

## Uso

### Conexión de Cliente LLM

Los LLMs pueden conectarse al servidor MCP a través de la interfaz proporcionada. El servidor expone herramientas para:

- Recuperar datos de sensores
- Preprocesar datos para análisis
- Detectar anomalías usando varios algoritmos
- Generar visualizaciones
- Ejecutar comandos correctivos

### Ejemplo de Flujo

1. Usuario: "Comprueba si hay anomalías en la temperatura del edificio"
2. LLM (usando el servidor MCP):
   - Recupera datos de temperatura recientes
   - Preprocesa los datos para normalización
   - Ejecuta algoritmo OneClassSVM para detectar anomalías
   - Genera visualización de anomalías
   - Sugiere acciones correctivas
3. Usuario: "Ejecuta la acción recomendada"
4. LLM:
   - Ejecuta comando correctivo
   - Confirma la ejecución exitosa

## Extensibilidad

El servidor está diseñado para ser extensible en múltiples dimensiones:

- **Fuentes de datos**: Fácil adición de nuevas fuentes de datos
- **Algoritmos**: Implementación de nuevos algoritmos de detección
- **Comandos**: Extensión de capacidades de acción correctiva

## Desarrollo

Este proyecto es un prototipo de nivel 5 (prueba de laboratorio) diseñado para demostrar la factibilidad de un servidor MCP centralizado para detección de anomalías. 
No está destinado a uso en producción inmediato.