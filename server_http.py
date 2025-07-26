#Esta version del server usa http para comunicarse con el agente
from fastmcp import FastMCP
from tools.generate_code_latex import register_tool
from tools.view_latex import register_tool_view_tex

mcp = FastMCP(
    name="LaTeXGenerator",
    instructions="Servidor MCP para generar documentos LaTeX usando Streamable HTTP",
    on_duplicate_tools="error"
)

register_tool(mcp)
register_tool_view_tex(mcp)

if __name__ == "__main__":
  
    mcp.run(transport="streamable-http")