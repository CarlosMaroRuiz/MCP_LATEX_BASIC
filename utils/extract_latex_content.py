from .clean_latex_code import clean_latex_code

def extract_latex_content(result) -> str:
    """
    Extrae el contenido LaTeX del resultado del agente.
    """
    # Lista de atributos comunes que podrían contener el texto
    text_attributes = ['data', 'content', 'text', 'output', 'message', 'result', 'response']
    
    content = None
    
    for attr in text_attributes:
        if hasattr(result, attr):
            value = getattr(result, attr)
            if isinstance(value, str) and value.strip():
                content = value
                break
    
    # Si es un diccionario, buscar claves comunes
    if content is None and isinstance(result, dict):
        for key in text_attributes:
            if key in result and isinstance(result[key], str):
                content = result[key]
                break
    
    # Como último recurso, convertir a string
    if content is None:
        content = str(result)
    
    if not content or content == "None":
        raise ValueError(f"No se pudo extraer contenido de texto del resultado: {type(result)}")
    
    # Limpiar el código LaTeX
    return clean_latex_code(content)