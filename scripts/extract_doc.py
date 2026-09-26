import mammoth
import os

docx_path = r"d:\Dam break Work\Dam Break CCCSS\Report DBA\DBA_Dehrang_Dam_Report.pdf.docx"
output_md = r"d:\Dam break Work\Dam Break CCCSS\docs\report_content.md"

def extract_content():
    if not os.path.exists("d:\\Dam break Work\\Dam Break CCCSS\\docs"):
        os.makedirs("d:\\Dam break Work\\Dam Break CCCSS\\docs")
        
    with open(docx_path, "rb") as docx_file:
        result = mammoth.convert_to_markdown(docx_file)
        
    with open(output_md, "w", encoding="utf-8") as md_file:
        md_file.write(result.value)
        
    print(f"Extracted markdown saved to {output_md}")
    if result.messages:
        print("Messages:", result.messages)

if __name__ == "__main__":
    extract_content()
