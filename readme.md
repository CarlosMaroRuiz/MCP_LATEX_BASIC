# MCP LaTeX Generator

Un servidor MCP (Model Context Protocol) para generar documentos LaTeX usando modelos de lenguaje de gran escala. Permite la creación, visualización y gestión de documentos LaTeX a través de una interfaz web o mediante comunicación directa con el servidor MCP.

## Descripción

Este proyecto implementa un servidor FastMCP que expone herramientas para generar código LaTeX a partir de descripciones en lenguaje natural. El sistema utiliza modelos de lenguaje como Deepseek para crear documentos LaTeX completos y listos para ser compilados.

## Características

- 🧰 **Servidor MCP**: Implementado con FastMCP para exponer herramientas de generación LaTeX
- 📝 **Generación de código LaTeX**: Creación de documentos completos desde descripciones en lenguaje natural
- 🌐 **Interfaz web**: Cliente web para interactuar con el servidor de forma amigable
- 📂 **Gestión de archivos**: Herramientas para listar, visualizar y limpiar documentos generados
- 🔄 **Soporte para múltiples transportes**: Comunicación vía STDIO o HTTP Streamable

## Estructura del Proyecto

```
mcp_latex_server/
├── agents/                     # Agentes de IA para generación LaTeX
│   └── agent_latex/            # Agente especializado en LaTeX
├── client/                     # Cliente web Flask
│   ├── static/                 # Recursos estáticos (CSS, JS)
│   └── templates/              # Plantillas HTML
├── latex_documents/            # Documentos LaTeX generados (creado automáticamente)
├── tools/                      # Herramientas MCP
│   ├── generate_code_latex.py  # Herramienta para generar LaTeX
│   └── view_latex.py           # Herramienta para visualizar archivos LaTeX
├── utils/                      # Utilidades compartidas
├── server.py                   # Servidor MCP (STDIO)
└── server_http.py              # Servidor MCP (HTTP)
```

## Componentes

### Servidor MCP

El servidor implementa las siguientes herramientas:

- `generate_code_latex`: Genera código LaTeX a partir de una descripción y lo guarda en la carpeta `latex_documents`
- `get_project_info`: Muestra información sobre las rutas del proyecto
- `list_latex_documents`: Lista todos los documentos LaTeX generados
- `clean_existing_latex_file`: Limpia un archivo LaTeX existente removiendo marcadores de markdown
- `view_file_tex`: Busca y lee el contenido de un archivo .tex en la carpeta latex_documents

### Cliente Web

El cliente web proporciona una interfaz amigable para:

- Ingresar descripciones para la generación de documentos LaTeX
- Visualizar el código generado
- Descargar archivos .tex
- Copiar el código al portapapeles

### Agente LaTeX

El agente LaTeX es responsable de convertir las descripciones en lenguaje natural en código LaTeX completo. Utiliza un modelo de lenguaje con un prompt especializado que garantiza que el código generado:

- Sea 100% compilable en pdflatex/Overleaf
- Incluya todos los paquetes necesarios
- Siga una estructura profesional
- Adapte el contenido según el tipo de documento solicitado

## Uso

### Iniciar el Servidor MCP

Para iniciar el servidor en modo STDIO (por defecto):

```bash
python server.py
```

Para iniciar el servidor en modo HTTP Streamable:

```bash
python server_http.py
```

### Utilizar el Cliente Web

Para iniciar el cliente web:

```bash
python client/app.py
```

Luego, accede a `http://localhost:5000` en tu navegador.

### Comunicación Directa con el Servidor MCP

Puedes comunicarte directamente con el servidor MCP utilizando un cliente MCP compatible:

```python
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStreamableHTTP
import asyncio

server = MCPServerStreamableHTTP('http://localhost:8000/mcp')  
agent = Agent('deepseek:deepseek-chat', toolsets=[server])  

async def main():
    async with agent:  
        result = await agent.run('realiza un codigo latex para un documento de 2 paginas')
    print(result.output)

asyncio.run(main())
```

## Herramientas Disponibles

### Generación de LaTeX

```python
await agent.run('Genera un documento LaTeX para un artículo académico sobre inteligencia artificial')
```

### Listar Documentos Generados

```python
await agent.run('Lista todos los documentos LaTeX que has generado')
```

### Ver Contenido de un Documento

```python
await agent.run('Muestra el contenido del archivo document_20250725_212912.tex')
```

## Tipos de Documentos Soportados

El sistema puede generar diversos tipos de documentos LaTeX:

- Artículos académicos
- Reportes técnicos
- Presentaciones (Beamer)
- Cartas formales
- CV/Resume
- Ensayos
- Manuales/Tutoriales

## Tecnologías Utilizadas

- **FastMCP**: Para implementar el servidor MCP
- **pydantic-ai**: Para la integración con modelos de lenguaje
- **Flask**: Para el cliente web
- **Deepseek**: Como modelo de lenguaje para la generación de LaTeX