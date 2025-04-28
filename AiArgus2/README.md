# Computer Vision Application

This application provides object detection and segmentation capabilities using YOLOv8 models.

## Project Structure

- `backend/`: Python FastAPI backend
- `frontend/`: React frontend application

## Setup and Running

### Backend

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the backend server:
   ```bash
   uvicorn main:app --reload
   ```

### Frontend

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the development server:
   ```bash
   npm run dev
   ```

4. Open your browser and navigate to `http://localhost:5173`

## Features

- Object Detection
  - Upload images or videos
  - Select specific classes to detect
  - Adjust confidence threshold
  - Customize bounding box appearance
  - Show/hide labels and confidence scores

- Segmentation
  - Upload images or videos
  - Adjust confidence threshold
  - View segmentation masks
