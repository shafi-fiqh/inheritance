import { useState } from 'react';
import _ from 'lodash';

import './App.css';

import problemSet from './problems.json';
const levelNames = ['Shares', 'Problem Base', 'Problem Base 2'];

const useProblems = (problems) => {
  const [level, setLevel] = useState(0);
  const [problemIndex, setProblemIndex] = useState(0);
  const [showResults, setShowResults] = useState(false);

  const levelName = levelNames[level];
  const problem = problemSet[problemIndex];
  const inheritancePool = problem.intermediate_shares.inheritance_pool;
  const sharePools = problem.intermediate_shares.share_pool;

  const inheritors = _.map(problem.problem, (i, inheritorKey) => {
    return {
      key: inheritorKey,
      sharePool: problem.intermediate_shares.inheritance_pool[inheritorKey]
    };
  });

  const inheritorsSortedBySharePool = _.sortBy(inheritors, 'sharePool');

  const [basicShareAnswers, setBasicShareAnswers] = useState(_.map(inheritors, () => null));
  const basicShareInputProps = _.map(basicShareAnswers, (answer, i) => {
    const resultBackgroundColor =
      problem.basic_shares[inheritorsSortedBySharePool[i].key] === answer ? '#CFE5C9' : '#ECB9B1';
    return {
      value: answer,
      backgroundColor: showResults ? resultBackgroundColor : '#F5FBFA'
    };
  });

  const intermediateShareGroups = _.groupBy(inheritorsSortedBySharePool, 'sharePool');
  const [intermediateShareAnswers, setIntermediateShareAnswers] = useState(
    _.map(intermediateShareGroups, () => '')
  );
  const sortedIntermediateShareGroups = _.map(intermediateShareGroups, (g, k) => {
    return { pool: k, groupSize: g.length, answer: problem.intermediate_shares.share_pool[k] };
  });
  const intermediateShareInputProps = _.map(intermediateShareAnswers, (answer, i) => {
    const resultBackgroundColor =
      sortedIntermediateShareGroups[i].answer == answer ? '#CFE5C9' : '#ECB9B1';
    return {
      value: answer,
      size: sortedIntermediateShareGroups[i].groupSize,
      backgroundColor: showResults ? resultBackgroundColor : '#F5FBFA'
    };
  });

  const checkAnswers = () => {
    setShowResults(true);
    const areBasicSharesCorrect = _.every(
      _.map(
        basicShareAnswers,
        (answer, i) => problem.basic_shares[inheritorsSortedBySharePool[i].key] === answer
      )
    );

    const areIntermediateSharesCorrect = _.every(
      _.map(
        intermediateShareAnswers,
        (answer, i) => sortedIntermediateShareGroups[i].answer == answer
      )
    );
    const areFinalSharesCorrect = false;

    // Move to level 1 if at level 0 and answers are correct
    if (areBasicSharesCorrect && level === 0) {
      setLevel(1);
    }

    // Move to level 1 if at level 0 and answers are correct
    console.log(areBasicSharesCorrect, areIntermediateSharesCorrect);
    if (areBasicSharesCorrect && areIntermediateSharesCorrect && level === 1) {
      setLevel(2);
    }

    // Show success
    if (
      areBasicSharesCorrect &&
      areIntermediateSharesCorrect &&
      areFinalSharesCorrect &&
      level === 2
    ) {
      alert('Success');
    }
  };

  const updateBasicShareAnswers = (answers) => {
    setShowResults(false);
    setBasicShareAnswers(answers);
  };

  const updateIntermediateShareAnswers = (answers) => {
    setShowResults(false);
    setIntermediateShareAnswers(answers);
  };

  return {
    inheritors: inheritorsSortedBySharePool,
    problem: problemIndex,
    level: levelName,
    basicShareInputProps,
    updateBasicShareAnswers,
    intermediateShareInputProps,
    updateIntermediateShareAnswers,
    checkAnswers
  };
};

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

  const inheritorsDisplay = _.map(inheritors, (inheritor, i) => <h3 key={i}> {inheritor.key}</h3>);

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
      height: `${input.size * 40}.px`
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
      {inheritorsDisplay}
      {basicShareDropdowns}
      {intermediateShareInputs}
      <input type="button" value="Check Answer" onClick={checkAnswers} />
    </div>
  );
}

export default App;
