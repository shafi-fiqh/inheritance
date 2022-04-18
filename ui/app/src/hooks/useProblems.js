import _ from 'lodash';
import { useState } from 'react';

import { answerColors, levels } from '../constants';

const levelNames = ['Shares', 'Problem Base', 'Problem Base 2'];

const useProblems = (problems) => {
  const [level, setLevel] = useState(levels.ONE);
  const [problemIndex, setProblemIndex] = useState(0);
  const [showResults, setShowResults] = useState(false);

  const levelName = levelNames[level];
  const problem = problems[problemIndex];
  const inheritancePool = problem.intermediate_shares.inheritance_pool;
  const sharePools = problem.intermediate_shares.share_pool;

  const normalizeInheritor = (index, inheritorKey) => {
    return {
      key: inheritorKey,
      sharePool: inheritancePool[inheritorKey]
    };
  };

  const normalizeSharePool = (group, poolKey) => {
    return { pool: poolKey, groupSize: group.length, answer: sharePools[poolKey] };
  };

  const inheritors = _.map(problem.problem, normalizeInheritor);
  const inheritorsSortedBySharePool = _.sortBy(inheritors, 'sharePool');
  const intermediateShareGroups = _.chain(inheritors)
    .sortBy('sharePool')
    .groupBy('sharePool')
    .value();
  const sortedIntermediateShareGroups = _.map(intermediateShareGroups, normalizeSharePool);

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
      problem.basic_shares[inheritorsSortedBySharePool[i].key] === answer
        ? answerColors.CORRECT
        : answerColors.INCORRECT;
    return {
      value: answer,
      backgroundColor: showResults ? resultBackgroundColor : answerColors.NOT_ANSWERED
    };
  });

  const intermediateShareInputProps = _.map(intermediateShareAnswers, (answer, i) => {
    const resultBackgroundColor =
      sortedIntermediateShareGroups[i].answer == answer
        ? answerColors.CORRECT
        : answerColors.INCORRECT;
    return {
      value: answer,
      size: sortedIntermediateShareGroups[i].groupSize,
      backgroundColor: showResults ? resultBackgroundColor : answerColors.NOT_ANSWERED
    };
  });

  const finalShareInputProps = _.map(finalShareAnswers, (answer, i) => {
    const inheritor = inheritorsSortedBySharePool[i].key;
    const resultBackgroundColor =
      problem.final_shares[inheritor] == answer ? answerColors.CORRECT : answerColors.INCORRECT;
    return {
      value: answer,
      backgroundColor: showResults ? resultBackgroundColor : answerColors.NOT_ANSWERED
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
    if (areBasicSharesCorrect && level === levels.ONE) {
      setLevel(1);
    }

    // Move to level 1 if at level 0 and answers are correct
    if (areBasicSharesCorrect && areIntermediateSharesCorrect && level === levels.TWO) {
      setLevel(2);
    }

    // Show success
    if (
      areBasicSharesCorrect &&
      areIntermediateSharesCorrect &&
      areFinalSharesCorrect &&
      level === levels.THREE
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
