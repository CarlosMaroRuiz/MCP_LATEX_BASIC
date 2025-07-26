from fastmcp import FastMCP
from agents import agent_latex_wrapper
from pathlib import Path
import os
from datetime import datetime
from typing import Dict, Any
import re
from utils import get_project_root, clean_latex_code, extract_latex_content



def register_tool(mcp: FastMCP):
    
    @mcp.tool
    async def generate_code_latex(prompt: str, save_to_project: bool = True) -> Dict[str, Any]:
        """
        Genera código LaTeX y lo guarda en la carpeta 'latex_documents'.
        
        Args:
            prompt: Descripción del documento LaTeX a generar
            save_to_project: Si True, guarda en el directorio del proyecto. Si False, en el directorio actual.
        
        Returns:
            dict con el código LaTeX generado y la ruta del archivo
        """
        result = None
        try:
            # Generar código LaTeX
            result = await agent_latex_wrapper(prompt)
            
            # Extraer y limpiar el contenido LaTeX
            latex_code = extract_latex_content(result)
            
            # Validar que el contenido parece ser LaTeX
            if not latex_code.strip():
                raise ValueError("El código LaTeX generado está vacío")
            
            # Verificación básica de que es LaTeX válido
            if "\\documentclass" not in latex_code:
                raise ValueError("El código generado no parece ser un documento LaTeX válido (falta \\documentclass)")
            
            # Determinar directorio base
            if save_to_project:
                base_dir = get_project_root()
            else:
                base_dir = Path.cwd()  # Directorio actual
            
            # Crear carpeta latex_documents en el directorio base
            output_dir = base_dir / "latex_documents"
            output_dir.mkdir(exist_ok=True)
            
            # Generar nombre de archivo único
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"document_{timestamp}.tex"
            filepath = output_dir / filename
            
            # Guardar archivo
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(latex_code)
            
            return {
                "success": True,
                "latex_code": latex_code,
                "file_path": str(filepath.resolve()),  # Ruta absoluta
                "relative_path": str(filepath.relative_to(base_dir)),  # Ruta relativa al proyecto
                "filename": filename,
                "project_root": str(base_dir),
                "output_directory": str(output_dir),
                "prompt": prompt,
                "saved_at": datetime.now().isoformat(),
                "file_size_bytes": len(latex_code.encode('utf-8')),
                "lines_count": len(latex_code.split('\n')),
                "cleaned": True
            }
            
        except Exception as e:
            debug_info = {
                "error_type": type(e).__name__,
                "prompt": prompt,
                "current_working_directory": str(Path.cwd()),
                "project_root": str(get_project_root())
            }
            
            if result is not None:
                debug_info.update({
                    "result_type": str(type(result)),
                    "result_preview": str(result)[:300] + "..." if len(str(result)) > 300 else str(result),
                })
            
            return {
                "success": False,
                "error": f"Error generando o guardando código LaTeX: {str(e)}",
                "latex_code": None,
                "debug_info": debug_info
            }

    @mcp.tool
    async def get_project_info() -> Dict[str, Any]:
        """
        Muestra información sobre las rutas del proyecto.
        
        Returns:
            dict con información de rutas
        """
        try:
            project_root = get_project_root()
            current_dir = Path.cwd()
            latex_dir = project_root / "latex_documents"
            
            return {
                "success": True,
                "project_root": str(project_root.resolve()),
                "current_working_directory": str(current_dir.resolve()),
                "latex_documents_directory": str(latex_dir.resolve()),
                "latex_dir_exists": latex_dir.exists(),
                "files_in_project": [f.name for f in project_root.iterdir() if f.is_file()],
                "script_location": str(Path(__file__).resolve()) if '__file__' in globals() else "Unknown"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error obteniendo información del proyecto: {str(e)}"
            }

    @mcp.tool
    async def list_latex_documents(search_in_project: bool = True) -> Dict[str, Any]:
        """
        Lista todos los documentos LaTeX generados.
        
        Args:
            search_in_project: Si True, busca en el directorio del proyecto. Si False, en el directorio actual.
        
        Returns:
            dict con la lista de archivos LaTeX
        """
        try:
            if search_in_project:
                base_dir = get_project_root()
            else:
                base_dir = Path.cwd()
                
            output_dir = base_dir / "latex_documents"
            
            if not output_dir.exists():
                return {
                    "success": True,
                    "documents": [],
                    "search_directory": str(output_dir.resolve()),
                    "message": f"La carpeta latex_documents no existe en {base_dir}"
                }
            
            tex_files = list(output_dir.glob("*.tex"))
            documents = []
            
            for file_path in tex_files:
                stat = file_path.stat()
                
                # Verificar si el archivo tiene marcadores markdown
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        has_markdown = '```latex' in content or content.startswith('```')
                except:
                    has_markdown = False
                
                documents.append({
                    "filename": file_path.name,
                    "absolute_path": str(file_path.resolve()),
                    "relative_path": str(file_path.relative_to(base_dir)),
                    "size_bytes": stat.st_size,
                    "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    "has_markdown_markers": has_markdown,
                    "needs_cleaning": has_markdown
                })
            
           
            documents.sort(key=lambda x: x["created"], reverse=True)
            
            return {
                "success": True,
                "documents": documents,
                "total_count": len(documents),
                "search_directory": str(output_dir.resolve()),
                "base_directory": str(base_dir.resolve()),
                "files_needing_cleanup": sum(1 for doc in documents if doc["needs_cleaning"])
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error listando documentos LaTeX: {str(e)}",
                "documents": []
            }

    @mcp.tool
    async def clean_existing_latex_file(filename: str, search_in_project: bool = True) -> Dict[str, Any]:
        """
        Limpia un archivo LaTeX existente removiendo marcadores de markdown.
        
        Args:
            filename: Nombre del archivo a limpiar (ej: document_20250725_212912.tex)
            search_in_project: Si True, busca en el directorio del proyecto. Si False, en el directorio actual.
        
        Returns:
            dict con el resultado de la operación
        """
        try:
            if search_in_project:
                base_dir = get_project_root()
            else:
                base_dir = Path.cwd()
                
            filepath = base_dir / "latex_documents" / filename
            
            if not filepath.exists():
                return {
                    "success": False,
                    "error": f"El archivo {filename} no existe en {filepath.parent}",
                    "searched_path": str(filepath.resolve())
                }
            
            # Leer archivo original
            with open(filepath, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            # Limpiar contenido
            cleaned_content = clean_latex_code(original_content)
            
            # Crear backup del original
            backup_path = filepath.with_suffix('.tex.backup')
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(original_content)
            
            # Guardar versión limpia
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)
            
            return {
                "success": True,
                "filename": filename,
                "file_path": str(filepath.resolve()),
                "backup_path": str(backup_path.resolve()),
                "original_size": len(original_content),
                "cleaned_size": len(cleaned_content),
                "bytes_removed": len(original_content) - len(cleaned_content),
                "message": "Archivo limpiado exitosamente. Se creó un backup del original."
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error limpiando archivo LaTeX: {str(e)}"
            }