import re
def clean_latex_code(content: str) -> str:
    """
    Limpia el código LaTeX removiendo marcadores de markdown y espacios extras.
    """
    content = re.sub(r'^```latex\s*\n', '', content, flags=re.MULTILINE)
    content = re.sub(r'^```\s*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'```latex', '', content)
    content = re.sub(r'```', '', content)
    
    # Limpiar espacios al inicio y final
    content = content.strip()
    
    # Asegurar que termina con una nueva línea
    if not content.endswith('\n'):
        content += '\n'
    
    return content