const BasicShareSelect = ({ index, value, bgColor, onSelect }) => {
  return (
    <div className="basic-share-select" style={{ backgroundColor: bgColor }}>
      <select
        value={value !== null ? value : '-'}
        onChange={(e) => onSelect(index, e.target.value)}
      >
        <option value="-">-</option>
        <option value="1/2">1/2</option>
        <option value="1/3">1/3</option>
        <option value="1/4">1/4</option>
        <option value="1/6">1/6</option>
        <option value="1/8">1/8</option>
        <option value="2/3">2/3</option>
        <option value="U">U</option>
      </select>
    </div>
  );
};

export default BasicShareSelect;