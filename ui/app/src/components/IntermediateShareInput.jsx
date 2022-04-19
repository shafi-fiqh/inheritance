import { levels } from '../constants';

const IntermediateShareInput = ({ index, size, bgColor, onChange, value, level }) => {
  const style = {
    backgroundColor: bgColor,
    height: `${size * 40}.px`,
    paddingTop: `${size * 10}.px`,
    paddingBottom: `${size * 10}.px`
  };

  const isDisabled = level < levels.TWO;

  return (
    <div key={index} className="intermediate-share-input" style={style}>
      <input
        disabled={isDisabled}
        type="number"
        value={value}
        onChange={(e) => onChange(index, e.target.value)}
      />
    </div>
  );
};

export default IntermediateShareInput;
