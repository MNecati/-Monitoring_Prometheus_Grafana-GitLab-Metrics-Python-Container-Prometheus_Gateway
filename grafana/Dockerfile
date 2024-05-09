# Python resmi base image'ını kullan
FROM python:3.9-slim

# Çalışma dizini ayarla
WORKDIR /app

# Bağımlılıkları içeren requirements.txt dosyasını kopyala
COPY requirements.txt .

# requirements.txt dosyasındaki paketleri yükle
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama dosyalarını kopyala
COPY . .

# Konteyner başlatıldığında çalışacak komut
CMD ["python", "yeni.py"]
# Python resmi base image'ını kullan
FROM python:3.9-slim

# Çalışma dizini ayarla
WORKDIR /app

# Bağımlılıkları içeren requirements.txt dosyasını kopyala
COPY requirements.txt .

# requirements.txt dosyasındaki paketleri yükle
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama dosyasını kopyala
COPY yeni.py .

# Konteyner başlatıldığında çalışacak komut
CMD ["python", "yeni.py"]
