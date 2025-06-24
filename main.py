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
                "metadata": pdf.metadata if pdf.metadata else {},
            }

            # Add page dimensions from first page
            if pdf.pages:
                first_page = pdf.pages[0]
                info["page_dimensions"] = {
                    "width": first_page.width,
                    "height": first_page.height,
                }

            return info

    except Exception as e:
        return {"error": f"Error reading PDF: {str(e)}"}


@mcp.tool()
def extract_tables(file_path: str, page_number: int | None = None) -> list:
    """Extract tables from a PDF file.
    
    Args:
        file_path: Path to the PDF file
        page_number: Optional specific page number (1-indexed). If not provided, extracts from all pages.
        
    Returns:
        List of tables, where each table is a list of rows (each row is a list of cell values)
    """
    try:
        if not os.path.exists(file_path):
            return [{"error": f"File not found: {file_path}"}]
            
        with pdfplumber.open(file_path) as pdf:
            tables = []
            
            if page_number is not None:
                # Convert to 0-indexed
                page_idx = page_number - 1
                if page_idx < 0 or page_idx >= len(pdf.pages):
                    return [{"error": f"Page {page_number} not found. PDF has {len(pdf.pages)} pages."}]
                
                page_tables = pdf.pages[page_idx].extract_tables()
                if page_tables:
                    for table in page_tables:
                        tables.append({
                            "page": page_number,
                            "data": table
                        })
            else:
                # Extract from all pages
                for i, page in enumerate(pdf.pages):
                    page_tables = page.extract_tables()
                    if page_tables:
                        for table in page_tables:
                            tables.append({
                                "page": i + 1,
                                "data": table
                            })
            
            if not tables:
                return [{"message": "No tables found in the PDF"}]
                
            return tables
            
    except Exception as e:
        return [{"error": f"Error reading PDF: {str(e)}"}]


def main():
    # Run the server using stdio transport
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
