import { useState, useEffect } from 'react';
import { Container, Box, Typography, Paper, Tabs, Tab, CircularProgress, Alert } from '@mui/material';
import { styled } from '@mui/material/styles';
import FileUpload from './components/FileUpload';
import SettingsPanel from './components/SettingsPanel';
import ResultsDisplay from './components/ResultsDisplay';

const StyledPaper = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(3),
  marginTop: theme.spacing(3),
}));

function App() {
  const [task, setTask] = useState<'detection' | 'segmentation'>('detection');
  const [selectedClasses, setSelectedClasses] = useState<string[]>([]);
  const [threshold, setThreshold] = useState(0.25);
  const [showLabels, setShowLabels] = useState(true);
  const [showConfidence, setShowConfidence] = useState(true);
  const [color, setColor] = useState('#B9282B');
  const [thickness, setThickness] = useState(2);
  const [result, setResult] = useState<{ image?: string; video?: string } | null>(null);
  const [classNames, setClassNames] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchClassNames = async () => {
      try {
        setLoading(true);
        const response = await fetch('http://localhost:8000/api/class-names');
        if (!response.ok) {
          throw new Error('Failed to fetch class names');
        }
        const data = await response.json();
        setClassNames(data.class_names);
        setSelectedClasses(data.class_names);
        setError(null);
      } catch (err) {
        setError('Could not connect to the backend server. Please make sure it is running.');
        console.error('Error fetching class names:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchClassNames();
  }, []);

  const handleTaskChange = (event: React.SyntheticEvent, newValue: 'detection' | 'segmentation') => {
    setTask(newValue);
    setResult(null);
  };

  const handleProcessFile = async (file: File) => {
    try {
      setLoading(true);
      setError(null);
      setResult(null);
      
      const formData = new FormData();
      formData.append('file', file);
      formData.append('task', task);
      formData.append('selected_classes', JSON.stringify(selectedClasses));
      formData.append('threshold', threshold.toString());
      formData.append('show_labels', showLabels.toString());
      formData.append('show_confidence', showConfidence.toString());
      formData.append('color', color);
      formData.append('thickness', thickness.toString());

      console.log('Sending file:', file.name, 'Size:', file.size);

      const response = await fetch('http://localhost:8000/api/detect', {
        method: 'POST',
        body: formData,
        credentials: 'include',
        mode: 'cors'
      });

      const data = await response.json();
      
      if (data.error) {
        throw new Error(data.error);
      }

      if (!data.image && !data.video) {
        throw new Error('Server response missing image or video data');
      }

      setResult(data);
      setError(null);
    } catch (err) {
      console.error('Error processing file:', err);
      setError(err instanceof Error ? err.message : 'Error processing file. Please try again.');
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ my: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom align="center">
          Computer Vision Application
        </Typography>
        <Typography variant="subtitle1" align="center" color="text.secondary">
          Authors: Igor Cwiertnia, Oskar Kubisztal, Jakub Laski, Tomasz Salwiczek
        </Typography>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        <Tabs
          value={task}
          onChange={handleTaskChange}
          centered
          sx={{ mb: 3 }}
        >
          <Tab value="detection" label="Object Detection" />
          <Tab value="segmentation" label="Segmentation" />
        </Tabs>

        {loading ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', my: 4 }}>
            <CircularProgress />
          </Box>
        ) : (
          <>
            <StyledPaper>
              <FileUpload onFileSelect={handleProcessFile} />
            </StyledPaper>

            <StyledPaper>
              <SettingsPanel
                task={task}
                classNames={classNames}
                selectedClasses={selectedClasses}
                onSelectedClassesChange={setSelectedClasses}
                threshold={threshold}
                onThresholdChange={setThreshold}
                showLabels={showLabels}
                onShowLabelsChange={setShowLabels}
                showConfidence={showConfidence}
                onShowConfidenceChange={setShowConfidence}
                color={color}
                onColorChange={setColor}
                thickness={thickness}
                onThicknessChange={setThickness}
              />
            </StyledPaper>

            {result && (
              <StyledPaper>
                <ResultsDisplay result={result} />
              </StyledPaper>
            )}
          </>
        )}
      </Box>
    </Container>
  );
}

export default App; 