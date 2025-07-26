from fastmcp import FastMCP
from tools.generate_code_latex import register_tool

mcp = FastMCP(name="LaTeXGenerator")

register_tool(mcp)

if __name__ == "__main__":
   
    mcp.run()