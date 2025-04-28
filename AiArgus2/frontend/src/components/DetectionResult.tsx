import React from 'react';
import { Box, Typography, Paper, List, ListItem, ListItemText, Chip } from '@mui/material';

interface DetectionResultProps {
  imageUrl: string;
  detections: Array<{
    class: string;
    confidence: number;
    bbox: [number, number, number, number];
  }>;
}

const DetectionResult: React.FC<DetectionResultProps> = ({ imageUrl, detections }) => {
  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
      <Paper elevation={3} sx={{ p: 2 }}>
        <img 
          src={imageUrl} 
          alt="Detection result" 
          style={{ 
            maxWidth: '100%', 
            height: 'auto',
            display: 'block',
            margin: '0 auto'
          }} 
        />
      </Paper>

      {detections.length > 0 ? (
        <Paper elevation={3} sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>
            Detected Objects
          </Typography>
          <List>
            {detections.map((detection, index) => (
              <ListItem key={index}>
                <ListItemText
                  primary={
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <Typography variant="body1">
                        {detection.class}
                      </Typography>
                      <Chip 
                        label={`${(detection.confidence * 100).toFixed(1)}%`}
                        color="primary"
                        size="small"
                      />
                    </Box>
                  }
                  secondary={`Bounding Box: [${detection.bbox.join(', ')}]`}
                />
              </ListItem>
            ))}
          </List>
        </Paper>
      ) : (
        <Paper elevation={3} sx={{ p: 2 }}>
          <Typography variant="body1" color="text.secondary">
            No objects detected
          </Typography>
        </Paper>
      )}
    </Box>
  );
};

export default DetectionResult; 