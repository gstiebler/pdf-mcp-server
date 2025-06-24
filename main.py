import pdfplumber
from mcp.server.fastmcp import FastMCP
import os

# Initialize the MCP server
mcp = FastMCP("pdf-reader")

@mcp.tool()
def extract_text(file_path: str) -> str:
    """Extract all text content from a PDF file.
    
    Args:
        file_path: Path to the PDF file
        
    Returns:
        Complete text content from all pages
    """
    try:
        if not os.path.exists(file_path):
            return f"Error: File not found: {file_path}"
            
        with pdfplumber.open(file_path) as pdf:
            all_text = []
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    all_text.append(text)
            
            if not all_text:
                return "No text content found in the PDF"
                
            return "\n\n".join(all_text)
            
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

@mcp.tool()
def get_pdf_info(file_path: str) -> dict:
    """Get basic information about a PDF file.
    
    Args:
        file_path: Path to the PDF file
        
    Returns:
        Dictionary containing page count and metadata
    """
    try:
        if not os.path.exists(file_path):
            return {"error": f"File not found: {file_path}"}
            
        with pdfplumber.open(file_path) as pdf:
            info = {
                "page_count": len(pdf.pages),
                "metadata": pdf.metadata if pdf.metadata else {}
            }
            
            # Add page dimensions from first page
            if pdf.pages:
                first_page = pdf.pages[0]
                info["page_dimensions"] = {
                    "width": first_page.width,
                    "height": first_page.height
                }
                
            return info
            
    except Exception as e:
        return {"error": f"Error reading PDF: {str(e)}"}

def main():
    # Run the server using stdio transport
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
