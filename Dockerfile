# 1. 使用 Python 3.11-slim
FROM python:3.11-slim

# 2. 設定工作目錄
WORKDIR /app

# 3. 複製需求檔案
COPY requirements.txt .

# 4. 安裝系統依賴（給 geopandas / rasterio / GDAL 用）
RUN apt-get update && apt-get install -y \
    build-essential \
    libgdal-dev \
    && rm -rf /var/lib/apt/lists/*

# 5. 安裝 Python 套件（請確保 requirements.txt 有 dash）
RUN pip install --no-cache-dir -r requirements.txt

# 6. 複製全部程式碼
COPY . .

# 7. 告訴 Hugging Face / 容器如何啟動 Dash
CMD ["python", "app.py"]
