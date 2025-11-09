# Zmiany w ArgusAI - Object Detection i Kolory

## Data: 2025-11-09

### Wprowadzone Poprawki

#### 1. Object Detection - Tylko Bounding Boxes
- ✅ **Object Detection** teraz używa TYLKO modelu detection (`yolov8n.pt`)
- ✅ **NIE używa** modelu segmentacji w trybie detection
- ✅ Wyświetlane są tylko bounding boxy (prostokąty), bez masek segmentacji
- ✅ Model segmentacji (`yolov8n-seg.pt`) jest używany TYLKO w trybie segmentation

#### 2. Kolory Bounding Boxów
- ✅ Kolory bounding boxów są teraz zgodne z kolorami ustawionymi w panelu Settings
- ✅ Domyślny kolor: `#B9282B` (czerwony)
- ✅ Użytkownik może zmienić kolor w sekcji "Bounding Box Color"
- ✅ Konwersja kolorów HEX → BGR jest spójna w całym kodzie

#### 3. Inne Poprawki
- ✅ Naprawiono konwersję kolorów dla wideo
- ✅ Naprawiono brakującą definicję `color_bgr` w segmentacji wideo
- ✅ Dodano wyraźne komunikaty logowania dla łatwiejszego debugowania
- ✅ Używany jest model `yolov8n.pt` zamiast `yolov8l.pt` dla wideo (szybszy)

### Jak Przetestować

1. **Zrestartuj Backend:**
   ```bash
   cd ArgusAI/AiArgus2/backend
   # Zatrzymaj poprzedni proces (Ctrl+C)
   python main.py
   ```

2. **Wyczyść Cache Przeglądarki i Odśwież Frontend:**
   - Naciśnij `Ctrl + F5` (Windows) lub `Cmd + Shift + R` (Mac)
   - Lub otwórz DevTools (F12) → kliknij prawym na refresh → "Empty Cache and Hard Reload"

3. **Test Detection:**
   - Wybierz zakładkę "Object Detection"
   - Wgraj zdjęcie (np. zdjęcie z ludźmi)
   - W Settings ustaw wybrany kolor (np. czerwony, niebieski)
   - Sprawdź czy bounding boxy mają wybrany kolor
   - Sprawdź czy NIE MA masek segmentacji (tylko prostokąty)

4. **Test Segmentation:**
   - Wybierz zakładkę "Segmentation"
   - Wgraj zdjęcie
   - Sprawdź czy są maski segmentacji (kolorowe wypełnienia)

### Backend Logs

Po uruchomieniu backendu, w konsoli zobaczysz:

```
============================================================
TASK: OBJECT DETECTION (Bounding Boxes Only)
============================================================
Loading YOLO detection model...
Detection model loaded successfully
Running object detection with bounding boxes...
Received color HEX: #B9282B
Using color BGR: (43, 40, 185) (R:185, G:40, B:43)
```

To potwierdza, że:
- Używany jest model detection
- Kolory są poprawnie konwertowane

### W Razie Problemów

Jeśli kolory nadal są cyan (turkusowe) zamiast wybranego koloru:

1. **Sprawdź czy backend jest uruchomiony:**
   ```bash
   # Powinien być dostępny na http://localhost:8000
   curl http://localhost:8000/api/class-names
   ```

2. **Sprawdź logi backendu:**
   - Poszukaj linii "Received color HEX: ..."
   - Sprawdź czy kolor jest przekazywany z frontendu

3. **Sprawdź czy używasz właściwej wersji:**
   - Upewnij się, że edytujesz plik `ArgusAI/AiArgus2/backend/main.py`
   - Nie używaj pliku z folderu `Deprecated`

4. **Wyczyść cache Python:**
   ```bash
   cd ArgusAI/AiArgus2/backend
   rm -rf __pycache__
   ```

### Zmiany w Kodzie

#### Backend (`main.py`)
- Linie 109-120: Detection używa `yolov8n.pt`
- Linie 125-135: Konwersja kolorów HEX → BGR
- Linie 167, 175, 184: Użycie `color_bgr` do rysowania
- Linie 316-333: Detection dla wideo używa `yolov8n.pt` i właściwych kolorów
- Linie 389-406: Segmentacja wideo ma poprawnie zdefiniowane kolory

#### Frontend (`App.tsx`)
- Linia 116: Domyślny kolor `#B9282B` (czerwony)
- Linia 179: Kolor jest przekazywany do backendu

---

**Autor:** AI Assistant  
**Data:** 2025-11-09

