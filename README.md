# ArgusAI - Aplikacja do Analizy Obrazów

ArgusAI to aplikacja webowa służąca do analizy obrazów. Umożliwia wykrywanie określonych przedmiotów na zdjęciach oraz ogólną analizę zawartości obrazów.

## Funkcjonalności

- Wykrywanie określonych przedmiotów na zdjęciach
- Ogólna analiza zawartości zdjęć
- Nowoczesny interfejs użytkownika
- Obsługa plików PDF i obrazów

## Wymagania

- Java 17
- Node.js 18+
- MySQL 8.0+
- Maven

## Instalacja i Uruchomienie

### Backend

1. Przejdź do katalogu backend:
```bash
cd backend
```

2. Upewnij się, że masz uruchomiony serwer MySQL

3. Zaktualizuj dane dostępowe do bazy danych w pliku `src/main/resources/application.properties`

4. Zbuduj i uruchom aplikację:
```bash
mvn spring-boot:run
```

Backend będzie dostępny pod adresem: http://localhost:8080

### Frontend

1. Przejdź do katalogu frontend:
```bash
cd frontend
```

2. Zainstaluj zależności:
```bash
npm install
```

3. Uruchom aplikację w trybie deweloperskim:
```bash
npm run dev
```

Frontend będzie dostępny pod adresem: http://localhost:5173

## Użycie

1. Otwórz aplikację w przeglądarce
2. Wybierz zdjęcie do analizy
3. W przypadku wykrywania przedmiotu, wpisz nazwę przedmiotu
4. Wybierz typ analizy:
   - "Znajdź przedmiot" - wyszukuje określony przedmiot na zdjęciu
   - "Analizuj zdjęcie" - wykonuje ogólną analizę zawartości zdjęcia
5. Poczekaj na wyniki analizy

## Technologie

- Backend:
  - Spring Boot
  - Spring Data JPA
  - MySQL
  - Maven

- Frontend:
  - React
  - TypeScript
  - Tailwind CSS
  - shadcn/ui
  - Vite
