FROM python:3.10-slim
WORKDIR /app
# 👉 核心修复：将旧的 libgl1-mesa-glx 替换为新系统支持的 libgl1 和 libglib2.0-0
RUN apt-get update && apt-get install -y tesseract-ocr tesseract-ocr-chi-sim libgl1 libglib2.0-0
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
