import { useState } from 'react'
import { Button } from './components/ui/button'
import { Upload, Search, Image as ImageIcon } from 'lucide-react'

interface AnalysisResult {
  fileName: string;
  result: string;
}

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [targetObject, setTargetObject] = useState('');
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setResult(null);
    }
  };

  const handleObjectDetection = async () => {
    if (!file || !targetObject) return;

    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);
    formData.append('targetObject', targetObject);

    try {
      const response = await fetch('http://localhost:8080/api/analysis/detect-object', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleGeneralAnalysis = async () => {
    if (!file) return;

    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:8080/api/analysis/general-analysis', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 py-8 px-4">
      <div className="max-w-2xl mx-auto">
        <h1 className="text-3xl font-bold text-center mb-8">ArgusAI - Analiza Obrazów</h1>
        
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <div className="flex flex-col items-center space-y-4">
            <div className="w-full max-w-md">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Wybierz zdjęcie
              </label>
              <div className="flex items-center justify-center w-full">
                <label className="flex flex-col items-center justify-center w-full h-64 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50 hover:bg-gray-100">
                  <div className="flex flex-col items-center justify-center pt-5 pb-6">
                    <Upload className="w-8 h-8 mb-2 text-gray-500" />
                    <p className="mb-2 text-sm text-gray-500">
                      <span className="font-semibold">Kliknij aby przesłać</span> lub przeciągnij i upuść
                    </p>
                    <p className="text-xs text-gray-500">PNG, JPG lub PDF (MAX. 10MB)</p>
                  </div>
                  <input
                    type="file"
                    className="hidden"
                    accept="image/*,.pdf"
                    onChange={handleFileChange}
                  />
                </label>
              </div>
              {file && (
                <p className="mt-2 text-sm text-gray-600">
                  Wybrany plik: {file.name}
                </p>
              )}
            </div>

            <div className="w-full max-w-md">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Szukany przedmiot (opcjonalnie)
              </label>
              <input
                type="text"
                value={targetObject}
                onChange={(e) => setTargetObject(e.target.value)}
                placeholder="np. telefon, laptop, książka"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div className="flex space-x-4">
              <Button
                onClick={handleObjectDetection}
                disabled={!file || !targetObject || loading}
                className="flex items-center"
              >
                <Search className="w-4 h-4 mr-2" />
                Znajdź przedmiot
              </Button>
              <Button
                onClick={handleGeneralAnalysis}
                disabled={!file || loading}
                variant="secondary"
                className="flex items-center"
              >
                <ImageIcon className="w-4 h-4 mr-2" />
                Analizuj zdjęcie
              </Button>
            </div>
          </div>
        </div>

        {loading && (
          <div className="text-center text-gray-600">
            Analizowanie...
          </div>
        )}

        {result && (
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold mb-4">Wynik analizy</h2>
            <div className="whitespace-pre-wrap text-gray-700">
              {result.result}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default App
