import _ from 'lodash';
import { useState } from 'react';

const levelNames = ['Shares', 'Problem Base', 'Problem Base 2'];

const useProblems = (problems) => {
  const [level, setLevel] = useState(0);
  const [problemIndex, setProblemIndex] = useState(0);
  const [showResults, setShowResults] = useState(false);

  const levelName = levelNames[level];
  const problem = problems[problemIndex];
  const inheritancePool = problem.intermediate_shares.inheritance_pool;
  const sharePools = problem.intermediate_shares.share_pool;

  const inheritors = _.map(problem.problem, (i, inheritorKey) => {
    return {
      key: inheritorKey,
      sharePool: inheritancePool[inheritorKey]
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
    return { pool: k, groupSize: g.length, answer: sharePools[k] };
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

export default useProblems;
