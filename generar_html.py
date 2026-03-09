import markdown
import sys

def main():
    with open("Informe_Red_Universitaria.md", "r", encoding="utf-8") as f:
        md_text = f.read()
    
    # Simple conversion
    html_content = markdown.markdown(md_text, extensions=['extra'])
    
    # Wrapper HTML with Mathjax for equations
    html_template = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Informe: Ubicación Óptima de Servidores</title>
<script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
<style>
body {{
    font-family: Arial, sans-serif;
    line-height: 1.6;
    margin: 40px auto;
    max-width: 800px;
    padding: 20px;
    color: #333;
}}
h1, h2, h3 {{
    color: #2c3e50;
}}
code {{
    background-color: #f4f4f4;
    padding: 2px 4px;
    border-radius: 4px;
}}
</style>
<script>
MathJax = {{
  tex: {{
    inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
    displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']]
  }}
}};
</script>
</head>
<body>
{html_content}
</body>
</html>
"""
    
    with open("Informe_Red_Universitaria.html", "w", encoding="utf-8") as f:
        f.write(html_template)
    
if __name__ == "__main__":
    main()
