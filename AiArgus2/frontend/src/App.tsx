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
  alpha,
  ThemeProvider,
  createTheme,
  CssBaseline,
  Switch,
  FormControlLabel,
} from '@mui/material';
import { styled } from '@mui/material/styles';
import FileUpload from './components/FileUpload';
import SettingsPanel from './components/SettingsPanel';
import ResultsDisplay from './components/ResultsDisplay';
import CameraAltIcon from '@mui/icons-material/CameraAlt';
import AutoAwesomeIcon from '@mui/icons-material/AutoAwesome';
import logo from '/logo/logo-argus-ai.png';
import Brightness4Icon from '@mui/icons-material/Brightness4';
import Brightness7Icon from '@mui/icons-material/Brightness7';

const StyledLogo = styled('img')(({ theme }) => ({
  height: '104px',
  marginRight: '16px',
  filter: theme.palette.mode === 'dark'
    ? 'drop-shadow(0 0 8px rgba(96, 165, 250, 0.3))'
    : 'drop-shadow(0 0 8px rgba(96, 165, 250, 0.2))',
  transition: 'transform 0.2s ease-in-out, filter 0.3s ease-in-out',
  padding: '8px 0',
  '&:hover': {
    transform: 'scale(1.05)'
  }
}));

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
  background: theme.palette.mode === 'dark' ? '#1a1c1e' : '#ffffff',
  boxShadow: theme.palette.mode === 'dark' 
    ? '0 4px 20px rgba(0, 0, 0, 0.3)' 
    : '0 4px 20px rgba(96, 165, 250, 0.1)',
  transition: 'all 0.3s ease-in-out',
  position: 'fixed',
  top: 0,
  left: 0,
  right: 0,
  zIndex: theme.zIndex.appBar,
}));

const StyledToolbar = styled(Toolbar)({
  display: 'flex',
  justifyContent: 'space-between',
  minHeight: '160px',
  padding: '0 32px',
  position: 'relative',
});

const LogoWrapper = styled(Box)({
  position: 'absolute',
  left: '50%',
  transform: 'translateX(-50%)',
  display: 'flex',
  alignItems: 'center',
  gap: '16px',
});

const ThemeToggleWrapper = styled(Box)({
  display: 'flex',
  alignItems: 'center',
  gap: '12px',
});

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
  const [mode, setMode] = useState<'light' | 'dark'>('light');
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
  const theme = createTheme({
    palette: {
      mode,
      primary: {
        main: '#0ea5e9',
      },
      secondary: {
        main: '#6366f1',
      },
      background: {
        default: mode === 'dark' ? '#0f172a' : '#f8fafc',
        paper: mode === 'dark' ? '#1e293b' : '#ffffff',
      },
    },
  });

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

  const handleThemeToggle = () => {
    setMode((prevMode) => (prevMode === 'light' ? 'dark' : 'light'));
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ 
        minHeight: '100vh', 
        bgcolor: 'background.default',
        transition: 'all 0.3s ease-in-out',
      }}>
        <GradientAppBar>
          <StyledToolbar>
            <Box sx={{ width: '200px' }} />
            <LogoWrapper>
              <StyledLogo src={logo} alt="Argus AI Logo" />
              <Typography variant="h6" component="div" sx={{ 
                fontWeight: 600,
                letterSpacing: '0.5px',
                background: 'linear-gradient(90deg, #0ea5e9 0%, #6366f1 100%)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                fontSize: '2.5rem',
                transition: 'all 0.3s ease-in-out',
              }}>
                Argus AI
              </Typography>
            </LogoWrapper>
            <ThemeToggleWrapper>
              <Box sx={{ 
                display: 'flex', 
                alignItems: 'center', 
                gap: 1,
                transition: 'all 0.3s ease-in-out',
              }}>
                <Brightness7Icon sx={{ 
                  color: theme.palette.mode === 'dark' ? 'grey.500' : '#fbbf24',
                  fontSize: '1.5rem',
                  transition: 'all 0.3s ease-in-out',
                }} />
                <Typography
                  sx={{
                    color: theme.palette.mode === 'dark' ? 'grey.500' : 'grey.700',
                    fontSize: '0.9rem',
                    fontWeight: 500,
                    transition: 'all 0.3s ease-in-out',
                  }}
                >
                  Light
                </Typography>
              </Box>
              <Switch
                checked={mode === 'dark'}
                onChange={handleThemeToggle}
                color="default"
                sx={{
                  '& .MuiSwitch-switchBase.Mui-checked': {
                    color: '#fff',
                  },
                  '& .MuiSwitch-switchBase': {
                    transition: 'all 0.3s ease-in-out',
                  },
                }}
              />
              <Box sx={{ 
                display: 'flex', 
                alignItems: 'center', 
                gap: 1,
                transition: 'all 0.3s ease-in-out',
              }}>
                <Brightness4Icon sx={{ 
                  color: theme.palette.mode === 'dark' ? '#fff' : 'grey.500',
                  fontSize: '1.5rem',
                  transition: 'all 0.3s ease-in-out',
                }} />
                <Typography
                  sx={{
                    color: theme.palette.mode === 'dark' ? '#fff' : 'grey.500',
                    fontSize: '0.9rem',
                    fontWeight: 500,
                    transition: 'all 0.3s ease-in-out',
                  }}
                >
                  Dark
                </Typography>
              </Box>
            </ThemeToggleWrapper>
          </StyledToolbar>
        </GradientAppBar>
        <Box sx={{ height: '160px' }} />

        <Container maxWidth="lg">
          <Box sx={{ 
            mt: 0,
            mb: 4,
            '& .MuiPaper-root': {
              transition: 'all 0.3s ease-in-out',
            },
          }}>
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
              sx={{ mb: 2 }}
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

                <Typography 
                  variant="subtitle1" 
                  align="center" 
                  color="text.secondary"
                  sx={{ 
                    mt: 6,
                    mb: 2,
                    opacity: 0.8,
                    fontSize: '0.9rem',
                    borderTop: '1px solid rgba(0,0,0,0.1)',
                    pt: 4
                  }}
                >
                  Created by: Igor Cwiertnia, Oskar Kubisztal, Jakub Laski, Tomasz Salwiczek
                </Typography>
              </>
            )}
          </Box>
        </Container>
      </Box>
    </ThemeProvider>
  );
}

export default App; 