import _ from 'lodash';

import { useState } from 'react';

import './App.css';

import { Problem } from './components/components';
import { levels } from './constants';

import problemSet from './problems.json';

// Ready to work on:
// TODO: Take param and only show upto a certain level - i.e. implement functionality around requiredLevels

function App() {
  const [currentProblem, setCurrentProblem] = useState(0);
  const [solvedProblems, setSolvedProblems] = useState({});

  const onProblemSolved = (problemIndex) => {
    setSolvedProblems({ ...solvedProblems, [problemIndex]: true });
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
        <Problem
          problem={problem}
          requiredLevels={levels.THREE}
          onProblemSolved={() => onProblemSolved(i)}
        />
      </div>
    );
  });

  return (
    <div className="App">
      <h2>Problem: {currentProblem}</h2>
      {problems}
      <input type="button" value="Prev" onClick={goToPrevProblem} disabled={currentProblem === 0} />
      <input
        type="button"
        value="Next"
        onClick={goToNextProblem}
        disabled={currentProblem === problemSet.length - 1 || !solvedProblems[currentProblem]}
      />
    </div>
  );
}

export default App;
