import React from 'react';
import { Box, Typography, Paper, useTheme, alpha, keyframes } from '@mui/material';
import styled from '@emotion/styled';
import PsychologyIcon from '@mui/icons-material/Psychology';
import WarningIcon from '@mui/icons-material/Warning';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import ImageIcon from '@mui/icons-material/Image';
import VideoLibraryIcon from '@mui/icons-material/VideoLibrary';

const fadeIn = keyframes`
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
`;

const pulse = keyframes`
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
  100% {
    transform: scale(1);
  }
`;

const glow = keyframes`
  0% {
    box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
  }
  50% {
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.2);
  }
  100% {
    box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
  }
`;

const StyledPaper = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(4),
  background: `linear-gradient(145deg, 
    ${alpha(theme.palette.background.paper, 0.95)} 0%, 
    ${alpha(theme.palette.background.default, 0.95)} 100%
  )`,
  backdropFilter: 'blur(16px)',
  borderRadius: theme.shape.borderRadius * 3,
  boxShadow: `0 8px 32px ${alpha(theme.palette.common.black, 0.08)}`,
  transition: 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)',
  animation: `${fadeIn} 0.6s ease-out, ${glow} 3s infinite`,
  border: `1px solid ${alpha(theme.palette.divider, 0.1)}`,
  '&:hover': {
    transform: 'translateY(-4px) scale(1.01)',
    boxShadow: `0 12px 40px ${alpha(theme.palette.common.black, 0.12)}`,
  },
}));

const ResultHeader = styled(Box)(({ theme }) => ({
  display: 'flex',
  alignItems: 'center',
  gap: theme.spacing(3),
  marginBottom: theme.spacing(4),
  paddingBottom: theme.spacing(3),
  borderBottom: `1px solid ${alpha(theme.palette.divider, 0.1)}`,
}));

const ResultContent = styled(Box)(({ theme }) => ({
  display: 'flex',
  flexDirection: 'column',
  gap: theme.spacing(3),
}));

const ConfidenceBadge = styled(Box)(({ theme }) => ({
  display: 'inline-flex',
  alignItems: 'center',
  padding: `${theme.spacing(1)} ${theme.spacing(2)}`,
  borderRadius: theme.shape.borderRadius * 3,
  background: `linear-gradient(145deg, 
    ${alpha(theme.palette.primary.main, 0.12)}, 
    ${alpha(theme.palette.secondary.main, 0.12)}
  )`,
  color: theme.palette.primary.main,
  fontSize: '0.875rem',
  fontWeight: 600,
  gap: theme.spacing(1),
  animation: `${pulse} 2s infinite`,
  border: `1px solid ${alpha(theme.palette.primary.main, 0.15)}`,
  backdropFilter: 'blur(8px)',
  '&:hover': {
    background: `linear-gradient(145deg, 
      ${alpha(theme.palette.primary.main, 0.2)}, 
      ${alpha(theme.palette.secondary.main, 0.2)}
    )`,
    transform: 'scale(1.02)',
  },
}));

const ExplanationBox = styled(Box)(({ theme }) => ({
  display: 'flex',
  alignItems: 'flex-start',
  gap: theme.spacing(2),
  padding: theme.spacing(3),
  background: `linear-gradient(145deg, 
    ${alpha(theme.palette.background.default, 0.8)} 0%, 
    ${alpha(theme.palette.background.paper, 0.9)} 100%
  )`,
  borderRadius: theme.shape.borderRadius * 3,
  border: `1px solid ${alpha(theme.palette.divider, 0.1)}`,
  transition: 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)',
  position: 'relative',
  overflow: 'hidden',
  backdropFilter: 'blur(8px)',
  '&::before': {
    content: '""',
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    height: '3px',
    background: `linear-gradient(90deg, 
      ${alpha(theme.palette.primary.main, 0.6)}, 
      ${alpha(theme.palette.secondary.main, 0.6)}
    )`,
    transform: 'scaleX(0)',
    transformOrigin: 'left',
    transition: 'transform 0.4s ease',
  },
  '&:hover': {
    transform: 'translateX(4px)',
    boxShadow: `0 4px 20px ${alpha(theme.palette.primary.main, 0.08)}`,
    '&::before': {
      transform: 'scaleX(1)',
    },
  },
}));

const IconWrapper = styled(Box)(({ theme }) => ({
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  width: 56,
  height: 56,
  borderRadius: '50%',
  background: `linear-gradient(145deg, 
    ${alpha(theme.palette.primary.main, 0.12)}, 
    ${alpha(theme.palette.secondary.main, 0.12)}
  )`,
  animation: `${pulse} 2s infinite`,
  border: `1px solid ${alpha(theme.palette.primary.main, 0.15)}`,
  backdropFilter: 'blur(8px)',
  boxShadow: `0 4px 12px ${alpha(theme.palette.primary.main, 0.1)}`,
}));

interface ResultsDisplayProps {
  result: {
    image?: string;
    format?: string;
    message?: string;
    error?: string;
  } | null;
  task?: 'detection' | 'segmentation';
}

function ResultsDisplay({ result, task = 'detection' }: ResultsDisplayProps) {
  const theme = useTheme();

  if (!result) {
    return null;
  }

  return (
    <StyledPaper>
      <ResultHeader>
        <IconWrapper>
          <PsychologyIcon 
            sx={{ 
              fontSize: 32,
              color: theme.palette.primary.main,
              filter: 'drop-shadow(0 2px 4px rgba(0,0,0,0.1))'
            }} 
          />
        </IconWrapper>
        <Box>
          <Typography 
            variant="h4" 
            component="h2" 
            gutterBottom
            sx={{
              fontWeight: 700,
              background: `linear-gradient(45deg, ${theme.palette.primary.main}, ${theme.palette.secondary.main})`,
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              letterSpacing: '-0.5px',
            }}
          >
            {task === 'detection' ? 'Detection Results' : 'Segmentation Results'}
          </Typography>
          <ConfidenceBadge>
            <TrendingUpIcon sx={{ fontSize: 20 }} />
            Processing Complete
          </ConfidenceBadge>
        </Box>
      </ResultHeader>

      <ResultContent>
        {result.error ? (
          <ExplanationBox>
            <WarningIcon 
              sx={{ 
                fontSize: 32,
                color: theme.palette.error.main,
                filter: 'drop-shadow(0 2px 4px rgba(0,0,0,0.1))'
              }} 
            />
            <Box sx={{ width: '100%' }}>
              <Typography color="error">
                {result.error}
              </Typography>
            </Box>
          </ExplanationBox>
        ) : (
          <ExplanationBox>
            <CheckCircleIcon 
              sx={{ 
                fontSize: 32,
                color: theme.palette.success.main,
                filter: 'drop-shadow(0 2px 4px rgba(0,0,0,0.1))'
              }} 
            />
            <Box sx={{ width: '100%' }}>
              <Typography>
                {result.message}
              </Typography>
              {result.image && (
                <img
                  src={`data:image/png;base64,${btoa(result.image.match(/.{1,2}/g)!.map(byte => String.fromCharCode(parseInt(byte, 16))).join(''))}`}
                  alt="Processed result with segmentation masks"
                  style={{ 
                    maxWidth: '100%', 
                    height: 'auto',
                    borderRadius: theme.shape.borderRadius * 2,
                    boxShadow: `0 4px 20px ${alpha(theme.palette.common.black, 0.1)}`,
                    display: 'block',
                    marginTop: theme.spacing(2)
                  }}
                  onError={(e) => {
                    console.error('Error loading image:', e);
                    const target = e.target as HTMLImageElement;
                    console.error('Image source:', target.src.substring(0, 100) + '...');
                    console.error('Image data length:', result.image?.length);
                    console.error('Full response:', result);
                  }}
                />
              )}
            </Box>
          </ExplanationBox>
        )}
      </ResultContent>
    </StyledPaper>
  );
}

export default ResultsDisplay; 