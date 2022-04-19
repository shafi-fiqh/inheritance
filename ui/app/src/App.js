import _ from 'lodash';

import { useState } from 'react';

import './App.css';

import { Problem } from './components/components';

import problemSet from './problems.json';

// TODO: Is total shares for the last level an input? How will they know what to put there

function App() {
  const [currentProblem, setCurrentProblem] = useState(0);
  const [solvedProblems, setSolvedProblems] = useState({});

  const onProblemSolved = (problemIndex) => {
    setSolvedProblems(_.assign(solvedProblems, { [problemIndex]: true }));
  };

  const goToPrevProblem = () => {
    if (currentProblem > 0) {
      setCurrentProblem(currentProblem - 1);
    }
  };

  const goToNextProblem = () => {
    if (solvedProblems[currentProblem] && currentProblem + 1 < problemSet.length) {
      setCurrentProblem(currentProblem + 1);
    }
  };

  const problems = _.map(problemSet, (problem, i) => {
    return (
      <div key={i} style={{ display: currentProblem == i ? 'block' : 'none' }}>
        <Problem problem={problem} onProblemSolved={() => onProblemSolved(0)} />
      </div>
    );
  });

  return (
    <div className="App">
      {/* <h2>Problem: {problem}</h2> */}
      {/* <h2>Level: {level}</h2> */}
      {problems}
      {/* TODO: Disable on first problem */}
      <input type="button" value="Prev" onClick={goToPrevProblem} />
      {/* TODO: Disable if no more problems or havent solved the next one */}
      <input type="button" value="Next" onClick={goToNextProblem} />
    </div>
  );
}

export default App;
