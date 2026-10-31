# @title
from IPython.display import display, HTML

my_html = """
<div style="background-color: #37474F; border-left: 6px solid #4DD0E1; padding: 20px; color: #FFFFFF; font-family: Arial, sans-serif;">
  <h3 style="margin-top: 0; color: #4DD0E1;">⚠️ Requirements</h3>
  </br>
  <ul style="list-style-type: none; padding-left: 0; line-height: 1.6;">
    <li><b>🔑 HF Token Required:</b> Please make sure to add your Hugging Face Token (click on the key icon on the left).</li>
    </br>
    <li><b>💻 GPU Required:</b> This tutorial requires a GPU (e.g., T4, A100 - Runtime - Change Runtime Type).</li>
  </ul>
</div>
"""
display(HTML(my_html))