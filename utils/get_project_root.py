from pathlib import Path
def get_project_root():
    """
    Obtiene la ruta raíz del proyecto donde se está ejecutando el script.
    """
    # Obtener la ruta del archivo actual
    current_file = Path(__file__).resolve()
    
    # Ir dos carpetas hacia arriba: tools -> mcp_latex_server
    # current_file.parent = tools/
    # current_file.parent.parent = mcp_latex_server/
    project_root = current_file.parent.parent
    
    # Validar que estamos en el directorio correcto (debe contener server.py)
    if (project_root / "server.py").exists():
        return project_root
    
    # Si no encontramos server.py, buscar en carpetas padre hasta encontrarlo
    search_path = current_file.parent
    for _ in range(5):  # Buscar hasta 5 niveles hacia arriba
        if (search_path / "server.py").exists():
            return search_path
        search_path = search_path.parent
        if search_path == search_path.parent:  # Llegamos a la raíz del sistema
            break
    
    # Fallback: usar la carpeta actual
    return current_file.parent