import { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { 
  Box, 
  Typography, 
  Button, 
  useTheme,
  alpha,
  Paper
} from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import ImageIcon from '@mui/icons-material/Image';
import VideoLibraryIcon from '@mui/icons-material/VideoLibrary';
import styled from '@emotion/styled';

interface FileUploadProps {
  onFileSelect: (file: File) => void;
}

const StyledDropzone = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(4),
  textAlign: 'center',
  cursor: 'pointer',
  border: `2px dashed ${alpha(theme.palette.primary.main, 0.3)}`,
  backgroundColor: alpha(theme.palette.background.paper, 0.5),
  transition: 'all 0.3s ease',
  '&:hover': {
    borderColor: theme.palette.primary.main,
    backgroundColor: alpha(theme.palette.primary.main, 0.05),
  },
  '&.active': {
    borderColor: theme.palette.success.main,
    backgroundColor: alpha(theme.palette.success.main, 0.05),
  },
}));

const UploadIcon = styled(CloudUploadIcon)(({ theme }) => ({
  fontSize: 48,
  color: theme.palette.primary.main,
  marginBottom: theme.spacing(2),
}));

const FileInfo = styled(Box)(({ theme }) => ({
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  gap: theme.spacing(2),
  marginTop: theme.spacing(2),
  padding: theme.spacing(2),
  backgroundColor: alpha(theme.palette.primary.main, 0.1),
  borderRadius: theme.shape.borderRadius,
}));

function FileUpload({ onFileSelect }: FileUploadProps) {
  const [file, setFile] = useState<File | null>(null);
  const theme = useTheme();

  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      const selectedFile = acceptedFiles[0];
      setFile(selectedFile);
      onFileSelect(selectedFile);
    }
  }, [onFileSelect]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.png', '.jpg', '.jpeg'],
      'video/*': ['.mp4', '.avi']
    },
    maxFiles: 1
  });

  return (
    <Box>
      <Typography 
        variant="h6" 
        gutterBottom 
        sx={{ 
          color: theme.palette.text.primary,
          fontWeight: 'medium',
          mb: 2
        }}
      >
        Upload Media
      </Typography>
      
      <StyledDropzone 
        {...getRootProps()} 
        className={isDragActive ? 'active' : ''}
      >
        <input {...getInputProps()} />
        <UploadIcon />
        <Typography variant="body1" color="text.secondary" gutterBottom>
          {isDragActive ? (
            "Drop the file here..."
          ) : (
            "Drag and drop a file here, or click to select"
          )}
        </Typography>
        <Typography variant="caption" color="text.secondary">
          Supported formats: Images (PNG, JPG, JPEG) and Videos (MP4, AVI)
        </Typography>
        
        {file && (
          <FileInfo>
            {file.type.startsWith('image/') ? (
              <ImageIcon color="primary" />
            ) : (
              <VideoLibraryIcon color="primary" />
            )}
            <Typography variant="body2">
              {file.name} ({(file.size / 1024 / 1024).toFixed(2)} MB)
            </Typography>
          </FileInfo>
        )}
      </StyledDropzone>
    </Box>
  );
}

export default FileUpload; 