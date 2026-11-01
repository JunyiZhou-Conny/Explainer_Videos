# @title
from IPython.display import Image, display, HTML
import requests
import base64

# Add HTML title above the diagram
display(HTML("""
<div style="text-align: left; margin: 20px 0;">
    <h2 style="color: #4fc3f7; font-family: 'Segoe UI', sans-serif; margin-bottom: 5px;">
        🚀 QLoRA Fine-Tuning Steps
    </h2>
</div>
"""))

mermaid_code = """
graph TD
    A[🔧 Load Base Model<br/>Qwen3-0.6B in 4-bit<br/>~0.5 GB weights] --> B[📊 Prepare Dataset<br/>Format with chat template<br/>Train: 900 Test: 100]
    B --> C[⚙️ Configure LoRA<br/>Rank r=8 Alpha=16<br/>~1.1M trainable params]
    C --> D[🎓 Train with SFTTrainer<br/>2 epochs batch_size=4<br/>Only adapters learn]
    D --> E[✅ Fine-Tuned Model<br/>Base: Frozen ❄️<br/>Adapters: ~4.6 MB]
    E --> F[💾 Save Options]
    F --> G[Adapters Only<br/>~4.6 MB file]
    F --> H[Merged Model<br/>1.2GB standalone]


    style A fill:#e3f2fd
    style C fill:#fff3e0
    style D fill:#f3e5f5
    style E fill:#e8f5e9
    style G fill:#ffe0b2
    style H fill:#ffe0b2
"""

# Encode for URL
graphbytes = mermaid_code.encode("utf8")
base64_bytes = base64.urlsafe_b64encode(graphbytes)
base64_string = base64_bytes.decode("ascii")

# # Generate image using mermaid.ink
img_url = f"https://mermaid.ink/img/{base64_string}?bgColor=black"

# # Display
display(Image(url=img_url, width=375, height=800))