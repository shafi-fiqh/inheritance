import _ from 'lodash';

import './App.css';

import useProblems from './hooks/useProblems';
import { Problem } from './components/components';

import problemSet from './problems.json';

// TODO: Is total shares for the last level an input? How will they know what to put there

function App() {
  const {
    inheritors,
    problem,
    level,
    basicShareInputProps,
    finalShareInputProps,
    intermediateShareInputProps,
    checkAnswers,
    updateBasicShareAnswers,
    updateIntermediateShareAnswers,
    updateFinalShareAnswers,
    goToPrevProblem,
    goToNextProblem
  } = useProblems(problemSet);

  const probelmProps = {
    inheritors,
    level,
    basicShareInputProps,
    intermediateShareInputProps,
    finalShareInputProps,
    updateBasicShareAnswers,
    updateIntermediateShareAnswers,
    updateFinalShareAnswers
  };

  return (
    <div className="App">
      <h2>Problem: {problem}</h2>
      <h2>Level: {level}</h2>
      {<Problem {...probelmProps} />}
      {/* TODO: Disable on first problem */}
      <input type="button" value="Prev" onClick={goToPrevProblem} />
      <input type="button" value="Check Answer" onClick={checkAnswers} />
      {/* TODO: Disable if no more problems or havent solved the next one */}
      <input type="button" value="Next" onClick={goToNextProblem} />
    </div>
  );
}

export default App;
