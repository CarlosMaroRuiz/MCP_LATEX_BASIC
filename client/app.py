from flask import Flask, render_template, request, jsonify, send_file
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStreamableHTTP
from dotenv import load_dotenv
import asyncio
import os
from pathlib import Path
import json
from datetime import datetime
import nest_asyncio

# Aplicar nest_asyncio para permitir bucles de eventos anidados
nest_asyncio.apply()

load_dotenv()

app = Flask(__name__)

MCP_SERVER_URL = os.getenv('MCP_SERVER_URL', 'http://localhost:8000/mcp')

# Crear un bucle de eventos global
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

class LaTeXGenerator:
    def __init__(self):
        self.server = MCPServerStreamableHTTP(MCP_SERVER_URL)
        self.agent = Agent('deepseek:deepseek-chat', toolsets=[self.server])
    
    async def generate_latex(self, prompt: str):
        try:
            async with self.agent:
                result = await self.agent.run(prompt)
                return {
                    "success": True,
                    "output": result.output,
                    "timestamp": datetime.now().isoformat()
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

# Instancia global del generador
latex_generator = LaTeXGenerator()

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_latex():
    """Endpoint para generar LaTeX"""
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        
        if not prompt:
            return jsonify({
                "success": False,
                "error": "El prompt no puede estar vacío"
            }), 400
        
        # Usar el bucle de eventos global para ejecutar la corrutina
        result = loop.run_until_complete(latex_generator.generate_latex(prompt))
        return jsonify(result)
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Error en el servidor: {str(e)}"
        }), 500

@app.route('/health')
def health_check():
    """Endpoint de salud del servidor"""
    return jsonify({
        "status": "healthy",
        "mcp_server_url": MCP_SERVER_URL,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/download/<filename>')
def download_file(filename):
    try:
        project_root = Path(__file__).parent.parent
        file_path = project_root / "latex_documents" / filename
        
        if file_path.exists():
            return send_file(
                file_path,
                as_attachment=True,
                download_name=filename
            )
        else:
            return jsonify({"error": "Archivo no encontrado"}), 404
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    finally:
        # Cerrar el bucle de eventos cuando la aplicación se detenga
        loop.close()