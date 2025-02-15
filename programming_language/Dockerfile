FROM python:3.12.9

RUN apt-get update && apt-get install -y \
    libx11-6 \
    libxcb1 \
    libxext6 \
    libxrender1 \
    xvfb \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-render-util0 \
    libxcb-xinerama0 \
    libglib2.0-0 \
    libxkbcommon-x11-0 \
    libxcb-util1 \
    libxcb-xfixes0 \
    libxcb-shape0 \
    libfontconfig1 \
    libdbus-1-3 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DISPLAY=:0

CMD ["python", "main.py"]

