from fastmcp import FastMCP
from pathlib import Path


def register_tool_view_tex(mcp: FastMCP):
    @mcp.tool
    def view_file_tex(name_file: str) -> dict:
        """
        Busca y lee el contenido de un archivo .tex en la carpeta latex_documents.
        Args:
            name_file: Nombre del archivo (ejemplo: document_20240101_120000.tex)
        Returns:
            dict con el contenido del archivo o mensaje de error
        """
        try:
            # Validar extensión
            if not name_file.lower().endswith('.tex'):
                return {
                    "success": False,
                    "error": "El archivo debe tener extensión .tex"
                }

            # Determinar ruta del archivo
            base_dir = Path(__file__).parent.parent  # Asume estructura estándar
            latex_dir = base_dir / "latex_documents"
            file_path = latex_dir / name_file

            if not file_path.exists():
                return {
                    "success": False,
                    "error": f"El archivo {name_file} no existe en {latex_dir}"
                }

            # Leer contenido
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            return {
                "success": True,
                "filename": name_file,
                "file_path": str(file_path.resolve()),
                "content": content,
                "size_bytes": len(content.encode('utf-8')),
                "lines_count": len(content.splitlines())
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error leyendo el archivo: {str(e)}"
            }