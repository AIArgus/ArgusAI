import { useState, useEffect } from 'react';
import { 
  Container, 
  Box, 
  Typography, 
  Paper, 
  Tabs, 
  Tab, 
  CircularProgress, 
  Alert,
  AppBar,
  Toolbar,
  IconButton,
  useTheme,
  alpha
} from '@mui/material';
import { styled } from '@mui/material/styles';
import FileUpload from './components/FileUpload';
import SettingsPanel from './components/SettingsPanel';
import ResultsDisplay from './components/ResultsDisplay';
import CameraAltIcon from '@mui/icons-material/CameraAlt';
import AutoAwesomeIcon from '@mui/icons-material/AutoAwesome';

const StyledPaper = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(3),
  marginTop: theme.spacing(3),
  borderRadius: theme.shape.borderRadius * 2,
  boxShadow: `0 4px 20px ${alpha(theme.palette.primary.main, 0.1)}`,
  transition: 'transform 0.2s ease-in-out',
  '&:hover': {
    transform: 'translateY(-2px)',
  },
}));

const GradientAppBar = styled(AppBar)(({ theme }) => ({
  background: `linear-gradient(45deg, ${theme.palette.primary.main} 30%, ${theme.palette.secondary.main} 90%)`,
  marginBottom: theme.spacing(4),
}));

const StyledTabs = styled(Tabs)(({ theme }) => ({
  '& .MuiTabs-indicator': {
    height: 4,
    borderRadius: 2,
  },
  '& .MuiTab-root': {
    textTransform: 'none',
    fontWeight: theme.typography.fontWeightRegular,
    fontSize: theme.typography.pxToRem(16),
    marginRight: theme.spacing(1),
    '&.Mui-selected': {
      color: theme.palette.primary.main,
      fontWeight: theme.typography.fontWeightMedium,
    },
  },
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
  const theme = useTheme();

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
    <Box sx={{ minHeight: '100vh', bgcolor: theme.palette.background.default }}>
      <GradientAppBar position="static">
        <Toolbar>
          <IconButton
            size="large"
            edge="start"
            color="inherit"
            aria-label="logo"
            sx={{ mr: 2 }}
          >
            <CameraAltIcon />
          </IconButton>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Computer Vision Application
          </Typography>
        </Toolbar>
      </GradientAppBar>

      <Container maxWidth="lg">
        <Box sx={{ my: 4 }}>
          <Typography 
            variant="h4" 
            component="h1" 
            gutterBottom 
            align="center"
            sx={{ 
              color: theme.palette.primary.main,
              fontWeight: 'bold',
              mb: 2
            }}
          >
            Computer Vision Application
          </Typography>
          <Typography 
            variant="subtitle1" 
            align="center" 
            color="text.secondary"
            sx={{ mb: 4 }}
          >
            Authors: Igor Cwiertnia, Oskar Kubisztal, Jakub Laski, Tomasz Salwiczek
          </Typography>

          {error && (
            <Alert 
              severity="error" 
              sx={{ 
                mb: 2,
                borderRadius: theme.shape.borderRadius * 2
              }}
            >
              {error}
            </Alert>
          )}

          <StyledTabs
            value={task}
            onChange={handleTaskChange}
            centered
            sx={{ mb: 3 }}
          >
            <Tab 
              value="detection" 
              label="Object Detection" 
              icon={<AutoAwesomeIcon />}
              iconPosition="start"
            />
            <Tab 
              value="segmentation" 
              label="Segmentation" 
              icon={<AutoAwesomeIcon />}
              iconPosition="start"
            />
          </StyledTabs>

          {loading ? (
            <Box sx={{ display: 'flex', justifyContent: 'center', my: 4 }}>
              <CircularProgress size={60} />
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
                  onSettingsChange={(settings) => {
                    // Update all settings at once
                    setThreshold(settings.confidenceThreshold);
                    setShowLabels(settings.showLabels);
                    setColor(settings.boxColor);
                  }}
                />
              </StyledPaper>

              {result && (
                <StyledPaper>
                  <ResultsDisplay result={result} task={task} />
                </StyledPaper>
              )}
            </>
          )}
        </Box>
      </Container>
    </Box>
  );
}

export default App; 