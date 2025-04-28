import { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Box, Typography, Paper, Alert } from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';

interface FileUploadProps {
  onFileSelect: (file: File) => void;
}

const FileUpload = ({ onFileSelect }: FileUploadProps) => {
  const onDrop = useCallback((acceptedFiles: File[], rejectedFiles: any[]) => {
    if (acceptedFiles.length > 0) {
      onFileSelect(acceptedFiles[0]);
    }
    if (rejectedFiles.length > 0) {
      console.error('Rejected files:', rejectedFiles);
    }
  }, [onFileSelect]);

  const { getRootProps, getInputProps, isDragActive, isDragReject } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.png', '.jpg', '.jpeg'],
      'video/*': ['.mp4', '.avi']
    },
    maxFiles: 1,
    multiple: false
  });

  return (
    <Paper
      {...getRootProps()}
      sx={{
        p: 3,
        textAlign: 'center',
        cursor: 'pointer',
        backgroundColor: isDragActive ? 'action.hover' : 'background.paper',
        border: '2px dashed',
        borderColor: isDragReject ? 'error.main' : isDragActive ? 'primary.main' : 'divider',
        '&:hover': {
          backgroundColor: 'action.hover',
        }
      }}
    >
      <input {...getInputProps()} />
      <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 2 }}>
        <CloudUploadIcon sx={{ fontSize: 48, color: 'primary.main' }} />
        <Typography variant="h6">
          {isDragActive 
            ? isDragReject 
              ? 'This file type is not supported'
              : 'Drop the file here'
            : 'Drag and drop a file here, or click to select'
          }
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Supported formats: Images (PNG, JPG, JPEG) and Videos (MP4, AVI)
        </Typography>
      </Box>
    </Paper>
  );
};

export default FileUpload; 