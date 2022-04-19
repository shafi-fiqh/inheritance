import { levels } from '../constants';

const FinalShareInput = ({ index, bgColor, onChange, level, value }) => {
  const isDisabled = level !== levels.THREE;
  return (
    <div className="final-share-input" style={{ backgroundColor: bgColor }}>
      <input
        disabled={isDisabled}
        type="number"
        value={value}
        onChange={(e) => onChange(index, e.target.value)}
      />
    </div>
  );
};

export default FinalShareInput;
