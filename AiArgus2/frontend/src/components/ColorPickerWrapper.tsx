import { SketchPicker } from 'react-color';
import { ColorResult } from 'react-color';

interface ColorPickerWrapperProps {
  color: string;
  onChange: (color: ColorResult) => void;
}

const ColorPickerWrapper = ({ color, onChange }: ColorPickerWrapperProps) => {
  return (
    <div>
      <SketchPicker
        color={color}
        onChange={onChange}
        disableAlpha={true}
      />
    </div>
  );
};

export default ColorPickerWrapper; 