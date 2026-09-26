import os

mkdocs_yml = """
site_name: Dehrang Dam Breach Analysis
theme:
  name: material
  features:
    - navigation.tabs
    - navigation.sections
    - toc.integrate
plugins:
  - search
  - mkdocs-jupyter
nav:
  - Home: index.md
  - Full Report: report_content.md
  - Notebooks:
      - Dehrang Design Flood DBA: notebooks/Dehrang_DesignFloodDBA.ipynb
      - Dehrang Dam DBA: notebooks/DehrangDam_DBA.ipynb
  - Maps: maps.md
"""

def setup_mkdocs():
    with open("mkdocs.yml", "w") as f:
        f.write(mkdocs_yml.strip())
    
    docs_dir = "docs"
    os.makedirs(docs_dir, exist_ok=True)
    
    if not os.path.exists(os.path.join(docs_dir, "index.md")):
        with open(os.path.join(docs_dir, "index.md"), "w") as f:
            f.write("# Welcome to Dehrang Dam Breach Analysis\n\nThis site contains the documentation, notebooks, and interactive maps for the Dehrang Dam Breach Analysis project.")
            
    if not os.path.exists(os.path.join(docs_dir, "maps.md")):
        with open(os.path.join(docs_dir, "maps.md"), "w") as f:
            f.write("# Interactive Maps\n\nHere you can view the interactive maps generated from shapefiles.\n\n<iframe src=\"map_overview.html\" width=\"100%\" height=\"600px\"></iframe>")

if __name__ == "__main__":
    setup_mkdocs()
