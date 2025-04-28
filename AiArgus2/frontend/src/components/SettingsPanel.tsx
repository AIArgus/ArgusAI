import React, { useState } from 'react';
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
  Switch,
} from '@mui/material';
import ColorPickerWrapper from './ColorPickerWrapper';
import { ColorResult } from 'react-color';

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
  onSettingsChange: (settings: any) => void;
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
  onSettingsChange,
}) => {
  const [settings, setSettings] = useState({
    confidenceThreshold: threshold,
    showLabels: showLabels,
    boxColor: color,
    labelColor: '#ffffff',
  });

  const handleSliderChange = (event: Event, newValue: number | number[]) => {
    const updatedSettings = { ...settings, confidenceThreshold: newValue as number };
    setSettings(updatedSettings);
    onThresholdChange(newValue as number);
    onSettingsChange(updatedSettings);
  };

  const handleSwitchChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const updatedSettings = { ...settings, showLabels: event.target.checked };
    setSettings(updatedSettings);
    onShowLabelsChange(event.target.checked);
    onSettingsChange(updatedSettings);
  };

  const handleColorChange = (color: ColorResult, type: 'box' | 'label') => {
    const updatedSettings = { ...settings, [`${type}Color`]: color.hex };
    setSettings(updatedSettings);
    onColorChange(color.hex);
    onSettingsChange(updatedSettings);
  };

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
            value={settings.confidenceThreshold}
            onChange={handleSliderChange}
            min={0}
            max={1}
            step={0.01}
            valueLabelDisplay="auto"
          />
        </Grid>
        {task === 'detection' && (
          <>
            <Grid item xs={12} sm={6}>
              <FormGroup>
                <FormControlLabel
                  control={
                    <Switch
                      checked={settings.showLabels}
                      onChange={handleSwitchChange}
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
              <ColorPickerWrapper
                color={settings.boxColor}
                onChange={(color) => handleColorChange(color, 'box')}
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