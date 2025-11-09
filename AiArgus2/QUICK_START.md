# ArgusAI - Quick Start Guide

## 🚀 Szybki Start

### Krok 1: Uruchom Backend

```bash
# Przejdź do folderu backend
cd ArgusAI/AiArgus2/backend

# Zainstaluj zależności (jeśli jeszcze nie)
pip install -r requirements.txt

# Uruchom backend
python main.py
```

Backend będzie dostępny na: `http://localhost:8000`

### Krok 2: Uruchom Frontend

W nowym terminalu:

```bash
# Przejdź do folderu frontend
cd ArgusAI/AiArgus2/frontend

# Zainstaluj zależności (jeśli jeszcze nie)
npm install

# Uruchom frontend
npm run dev
```

Frontend będzie dostępny na: `http://localhost:5173`

### Krok 3: Test Backend (Opcjonalnie)

W trzecim terminalu:

```bash
cd ArgusAI/AiArgus2
python test_backend.py
```

## 🎯 Jak Używać

### Object Detection (Detekcja Obiektów)

1. Otwórz `http://localhost:5173` w przeglądarce
2. Wybierz zakładkę **"Object Detection"**
3. W panelu **Settings**:
   - Wybierz klasy obiektów do wykrywania (np. person, car, dog)
   - Ustaw próg pewności (Confidence Threshold)
   - Włącz/wyłącz etykiety (Show Labels)
   - Włącz/wyłącz poziom pewności (Show Confidence)
   - **Wybierz kolor bounding boxów** (Bounding Box Color)
   - Ustaw grubość linii (Bounding Box Thickness)
4. Kliknij **"Choose File"** i wybierz zdjęcie lub wideo
5. Poczekaj na wynik detekcji

**Ważne:** W trybie Detection zobaczysz TYLKO bounding boxy (prostokąty), NIE maski segmentacji.

### Segmentation (Segmentacja)

1. Wybierz zakładkę **"Segmentation"**
2. Ustaw próg pewności
3. Wgraj zdjęcie lub wideo
4. Zobacz wynik segmentacji z kolorowymi maskami

## 🔧 Rozwiązywanie Problemów

### Backend nie startuje

```bash
# Sprawdź czy port 8000 nie jest zajęty
# Windows PowerShell:
netstat -ano | findstr :8000

# Zainstaluj ponownie zależności
pip install --upgrade -r requirements.txt
```

### Frontend nie łączy się z backendem

1. Sprawdź czy backend działa: `curl http://localhost:8000/api/class-names`
2. Wyczyść cache przeglądarki: `Ctrl + F5` (Windows) lub `Cmd + Shift + R` (Mac)
3. Sprawdź konsole przeglądarki (F12) dla błędów CORS

### Kolory bounding boxów są nieprawidłowe

1. Zrestartuj backend
2. Wyczyść cache Python: `rm -rf ArgusAI/AiArgus2/backend/__pycache__`
3. Sprawdź logi backendu dla linii "Using color BGR: ..."
4. Upewnij się, że używasz właściwego pliku (`AiArgus2/backend/main.py`, NIE `Deprecated/Backend/main.py`)

### Model YOLO się nie ładuje

Sprawdź czy pliki modeli są w folderze backend:
- `yolov8n.pt` - dla detection
- `yolov8n-seg.pt` - dla segmentation

Jeśli nie ma, zostaną pobrane automatycznie przy pierwszym uruchomieniu.

## 📝 Domyślne Ustawienia

- **Confidence Threshold:** 0.25
- **Bounding Box Color:** #B9282B (czerwony)
- **Thickness:** 2
- **Show Labels:** Włączone
- **Show Confidence:** Włączone

## 🎨 Dostępne Kolory

Możesz wybrać dowolny kolor w formacie HEX:
- Czerwony: `#B9282B` (domyślny)
- Niebieski: `#0000FF`
- Zielony: `#00FF00`
- Żółty: `#FFFF00`
- Cyan: `#00FFFF`
- Różowy: `#FF00FF`
- Pomarańczowy: `#FF6600`
- Biały: `#FFFFFF`

## 📊 Dostępne Klasy Obiektów (COCO Dataset)

person, bicycle, car, motorcycle, airplane, bus, train, truck, boat, traffic light, 
fire hydrant, stop sign, parking meter, bench, bird, cat, dog, horse, sheep, cow, 
elephant, bear, zebra, giraffe, backpack, umbrella, handbag, tie, suitcase, frisbee, 
skis, snowboard, sports ball, kite, baseball bat, baseball glove, skateboard, 
surfboard, tennis racket, bottle, wine glass, cup, fork, knife, spoon, bowl, banana, 
apple, sandwich, orange, broccoli, carrot, hot dog, pizza, donut, cake, chair, couch, 
potted plant, bed, dining table, toilet, tv, laptop, mouse, remote, keyboard, 
cell phone, microwave, oven, toaster, sink, refrigerator, book, clock, vase, scissors, 
teddy bear, hair drier, toothbrush

## 📚 Więcej Informacji

- Zobacz `CHANGES.md` dla szczegółów ostatnich zmian
- Backend API: `http://localhost:8000/docs` (FastAPI Swagger UI)

