import _ from 'lodash';

import useProblems from './hooks/useProblems';
import './App.css';

import problemSet from './problems.json';

function App() {
  const {
    inheritors,
    problem,
    level,
    basicShareInputProps,
    updateBasicShareAnswers,
    checkAnswers,
    intermediateShareInputProps,
    updateIntermediateShareAnswers
  } = useProblems(problemSet);

  const inheritorsDisplay = _.map(inheritors, (inheritor, i) => (
    <div key={i} className="inheritor">
      <h3> {inheritor.key}</h3>
    </div>
  ));

  const onBasicSharesChange = (changedIndex, value) => {
    const answers = _.map(basicShareInputProps, 'value');
    answers[changedIndex] = value;
    updateBasicShareAnswers(answers);
  };

  const basicShareDropdowns = _.map(basicShareInputProps, (input, i) => {
    const style = {
      backgroundColor: input.backgroundColor
    };
    return (
      <div key={i} className="basic-share-select" style={style}>
        <select
          value={input.value !== null ? input.value : '-'}
          onChange={(e) => onBasicSharesChange(i, e.target.value)}
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
  });

  const onIntermediateSharesChange = (changedIndex, value) => {
    const answers = _.map(intermediateShareInputProps, 'value');
    answers[changedIndex] = value;
    updateIntermediateShareAnswers(answers);
  };

  const intermediateShareInputs = _.map(intermediateShareInputProps, (input, i) => {
    const style = {
      backgroundColor: input.backgroundColor,
      height: `${input.size * 40}.px`,
      paddingTop: `${input.size * 10}.px`,
      paddingBottom: `${input.size * 10}.px`
    };
    return (
      <div key={i} className="intermediate-share-input" style={style}>
        <input
          type="number"
          value={input.value}
          onChange={(e) => onIntermediateSharesChange(i, e.target.value)}
        />
      </div>
    );
  });

  return (
    <div className="App">
      <h2>Problem: {problem}</h2>
      <h2>Level: {level}</h2>
      <div className="problem-container">
        <div className="column">{inheritorsDisplay}</div>
        <div className="column">{basicShareDropdowns}</div>
        <div className="column">{intermediateShareInputs}</div>
      </div>
      <input type="button" value="Check Answer" onClick={checkAnswers} />
    </div>
  );
}

export default App;
