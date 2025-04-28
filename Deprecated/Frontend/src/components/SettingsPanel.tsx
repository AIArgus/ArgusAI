import React from 'react';
import {
  Box,
  Typography,
  Slider,
  FormGroup,
  FormControlLabel,
  Checkbox,
  TextField,
  Autocomplete,
  Grid,
} from '@mui/material';
import { SketchPicker } from 'react-color';

interface SettingsPanelProps {
  task: 'detection' | 'segmentation';
  classNames: string[];
  selectedClasses: string[];
  onSelectedClassesChange: (classes: string[]) => void;
  threshold: number;
  onThresholdChange: (value: number) => void;
  showLabels: boolean;
  onShowLabelsChange: (value: boolean) => void;
  showConfidence: boolean;
  onShowConfidenceChange: (value: boolean) => void;
  color: string;
  onColorChange: (color: string) => void;
  thickness: number;
  onThicknessChange: (value: number) => void;
}

const SettingsPanel: React.FC<SettingsPanelProps> = ({
  task,
  classNames,
  selectedClasses,
  onSelectedClassesChange,
  threshold,
  onThresholdChange,
  showLabels,
  onShowLabelsChange,
  showConfidence,
  onShowConfidenceChange,
  color,
  onColorChange,
  thickness,
  onThicknessChange,
}) => {
  return (
    <Box>
      <Typography variant="h6" gutterBottom>
        Settings
      </Typography>
      <Grid container spacing={3}>
        {task === 'detection' && (
          <Grid item xs={12}>
            <Typography gutterBottom>Select Classes to Detect</Typography>
            <Autocomplete
              multiple
              options={classNames}
              value={selectedClasses}
              onChange={(_, newValue) => onSelectedClassesChange(newValue)}
              renderInput={(params) => (
                <TextField
                  {...params}
                  variant="outlined"
                  placeholder="Select classes"
                />
              )}
            />
          </Grid>
        )}
        <Grid item xs={12}>
          <Typography gutterBottom>Confidence Threshold</Typography>
          <Slider
            value={threshold}
            onChange={(_, value) => onThresholdChange(value as number)}
            min={0.1}
            max={1}
            step={0.1}
            valueLabelDisplay="auto"
          />
        </Grid>
        {task === 'detection' && (
          <>
            <Grid item xs={12} sm={6}>
              <FormGroup>
                <FormControlLabel
                  control={
                    <Checkbox
                      checked={showLabels}
                      onChange={(e) => onShowLabelsChange(e.target.checked)}
                    />
                  }
                  label="Show Labels"
                />
              </FormGroup>
            </Grid>
            <Grid item xs={12} sm={6}>
              <FormGroup>
                <FormControlLabel
                  control={
                    <Checkbox
                      checked={showConfidence}
                      onChange={(e) => onShowConfidenceChange(e.target.checked)}
                    />
                  }
                  label="Show Confidence"
                />
              </FormGroup>
            </Grid>
            <Grid item xs={12} sm={6}>
              <Typography gutterBottom>Bounding Box Color</Typography>
              <SketchPicker
                color={color}
                onChangeComplete={(color) => onColorChange(color.hex)}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <Typography gutterBottom>Bounding Box Thickness</Typography>
              <Slider
                value={thickness}
                onChange={(_, value) => onThicknessChange(value as number)}
                min={1}
                max={5}
                step={1}
                valueLabelDisplay="auto"
              />
            </Grid>
          </>
        )}
      </Grid>
    </Box>
  );
};

export default SettingsPanel; 