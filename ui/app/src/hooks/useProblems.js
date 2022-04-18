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
  const intermediateShareGroups = _.groupBy(inheritorsSortedBySharePool, 'sharePool');
  const sortedIntermediateShareGroups = _.map(intermediateShareGroups, (g, k) => {
    return { pool: k, groupSize: g.length, answer: sharePools[k] };
  });

  const emptyBasicShareAnswers = new Array(inheritors.length).fill(null);
  const emptyIntermediateShareAnswers = new Array(_.size(intermediateShareGroups)).fill('');
  const emptyFinalShareAnswers = new Array(inheritors.length).fill('');

  const [basicShareAnswers, setBasicShareAnswers] = useState(emptyBasicShareAnswers);
  const [intermediateShareAnswers, setIntermediateShareAnswers] = useState(
    emptyIntermediateShareAnswers
  );
  const [finalShareAnswers, setFinalShareAnswers] = useState(emptyFinalShareAnswers);

  const basicShareInputProps = _.map(basicShareAnswers, (answer, i) => {
    const resultBackgroundColor =
      problem.basic_shares[inheritorsSortedBySharePool[i].key] === answer ? '#CFE5C9' : '#ECB9B1';
    return {
      value: answer,
      backgroundColor: showResults ? resultBackgroundColor : '#F5FBFA'
    };
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

  const finalShareInputProps = _.map(finalShareAnswers, (answer, i) => {
    const inheritor = inheritorsSortedBySharePool[i].key;
    const resultBackgroundColor = problem.final_shares[inheritor] == answer ? '#CFE5C9' : '#ECB9B1';
    return {
      value: answer,
      backgroundColor: showResults ? resultBackgroundColor : '#F5FBFA'
    };
  });

  const checkAnswers = () => {
    //   TODO: Show loading
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
    const areFinalSharesCorrect = _.every(
      _.map(
        finalShareAnswers,
        (answer, i) => problem.final_shares[inheritorsSortedBySharePool[i].key] == answer
      )
    );

    // Move to level 1 if at level 0 and answers are correct
    if (areBasicSharesCorrect && level === 0) {
      setLevel(1);
    }

    // Move to level 1 if at level 0 and answers are correct
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

    //   TODO: Hide loading
    setShowResults(true);
  };

  const updateBasicShareAnswers = (answers) => {
    setShowResults(false);
    setBasicShareAnswers(answers);
  };

  const updateIntermediateShareAnswers = (answers) => {
    setShowResults(false);
    setIntermediateShareAnswers(answers);
  };

  const updateFinalShareAnswers = (answers) => {
    setShowResults(false);
    setFinalShareAnswers(answers);
  };

  return {
    inheritors: inheritorsSortedBySharePool,
    problem: problemIndex,
    level: levelName,
    basicShareInputProps,
    updateBasicShareAnswers,
    intermediateShareInputProps,
    updateIntermediateShareAnswers,
    finalShareInputProps,
    updateFinalShareAnswers,
    checkAnswers
  };
};

export default useProblems;
