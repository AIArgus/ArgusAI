# 🔄 INSTRUKCJA: Wyczyść Cache Przeglądarki

## ⚠️ WAŻNE!

Nowy backend jest uruchomiony, ale **musisz wyczyścić cache przeglądarki** żeby zobaczyć zmiany!

## 🌐 Jak Wyczyścić Cache:

### Google Chrome / Microsoft Edge:
1. Otwórz stronę `http://localhost:5173`
2. Naciśnij **Ctrl + Shift + Delete**
3. Wybierz "Cached images and files" (Obrazy i pliki w pamięci cache)
4. Kliknij "Clear data" (Wyczyść dane)
5. **LUB** po prostu naciśnij **Ctrl + F5** (Hard Refresh)

### Firefox:
1. Otwórz stronę `http://localhost:5173`
2. Naciśnij **Ctrl + Shift + Delete**
3. Wybierz "Cache"
4. Kliknij "Clear Now"
5. **LUB** po prostu naciśnij **Ctrl + Shift + R** (Hard Refresh)

### Najprostszy sposób (wszystkie przeglądarki):
```
1. Naciśnij F12 (otwórz DevTools)
2. Kliknij PRAWYM przyciskiem na ikonę odświeżenia (⟳)
3. Wybierz "Empty Cache and Hard Reload"
```

## 🧪 Test po Wyczyszczeniu Cache:

1. **Odśwież stronę** (Ctrl + F5)
2. **Wybierz zakładkę "Object Detection"**
3. **W Settings:**
   - Zmień kolor na **niebieski** (#0000FF) lub **zielony** (#00FF00)
   - Sprawdź czy kolor się zmienił w color pickerze
4. **Wgraj zdjęcie** (np. z ludźmi)
5. **Sprawdź wynik:**
   - ✅ Powinny być TYLKO prostokątne bounding boxy
   - ✅ NIE powinno być kolorowych masek segmentacji
   - ✅ Bounding boxy powinny mieć wybrany kolor (niebieski/zielony)

## 🔍 Co Powinieneś Zobaczyć:

### ✅ POPRAWNIE (Object Detection):
```
┌─────────────────┐
│   person 0.95   │  ← Prostokątne boxy w wybranym kolorze
│                 │
│                 │
└─────────────────┘
```

### ❌ NIEPOPRAWNIE (To był błąd - maski segmentacji):
```
🟦🟦🟦🟦🟦🟦🟦
🟦🟦🟦👤🟦🟦🟦  ← Kolorowe wypełnienie (to NIE powinno być)
🟦🟦🟦🟦🟦🟦🟦
```

## 📋 Checklist:

- [ ] Backend uruchomiony (✅ Już jest!)
- [ ] Cache wyczyszczony (Ctrl + F5)
- [ ] Strona odświeżona
- [ ] Kolor zmieniony w Settings
- [ ] Zdjęcie wgrane
- [ ] Sprawdzone że są tylko bounding boxy
- [ ] Sprawdzone że kolory się zgadzają

## 🆘 Jeśli Nadal Nie Działa:

1. **Zamknij całkowicie przeglądarkę** i otwórz ponownie
2. **Sprawdź konsolę przeglądarki** (F12 → Console) - czy są błędy?
3. **Sprawdź Network tab** (F12 → Network):
   - Wgraj zdjęcie
   - Znajdź request do `/api/detect`
   - Sprawdź czy "color" w Request Payload pokazuje wybrany kolor
4. **Sprawdź czy frontend jest uruchomiony**:
   ```
   cd ArgusAI\AiArgus2\frontend
   npm run dev
   ```

---

**Backend jest gotowy i czeka! 🚀**  
**Teraz tylko wyczyść cache i przetestuj!** 🧹

