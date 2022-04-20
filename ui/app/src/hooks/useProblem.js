import _ from 'lodash';
import { useState, useEffect } from 'react';

import { answerColors, levels } from '../constants';

const useProblem = (problem) => {
  const [level, setLevel] = useState(levels.ONE);
  const [showResults, setShowResults] = useState(false);
  const [isProblemSolved, setIsProblemSolved] = useState(false);

  const [basicShareAnswers, setBasicShareAnswers] = useState(null);
  const [basicShareInputProps, setBasicShareInputProps] = useState(null);
  const [areBasicSharesCorrect, setAreBasicSharesCorrect] = useState(false);

  const [intermediateShareAnswers, setIntermediateShareAnswers] = useState(null);
  const [intermediateShareInputProps, setIntermediateShareInputProps] = useState(null);
  const [areIntermediateSharesCorrect, setAreIntermediateSharesCorrect] = useState(null);

  const [finalShareAnswers, setFinalShareAnswers] = useState(null);
  const [finalShareInputProps, setFinalShareInputProps] = useState(null);
  const [areFinalSharesCorrect, setAreFinalSharesCorrect] = useState(null);

  const [problemData, setProblemData] = useState({});

  useEffect(() => {
    const normalizeInheritor = (i, inheritorKey) => {
      return {
        key: inheritorKey,
        sharePool: inheritancePool[inheritorKey]
      };
    };

    const inheritancePool = problem.intermediate_shares.inheritance_pool;
    const sharePools = problem.intermediate_shares.share_pool;

    const normalizeSharePool = (group, poolKey) => {
      return { pool: poolKey, groupSize: group.length };
    };

    const inheritors = _.map(problem.problem, normalizeInheritor);
    const inheritorsSortedBySharePool = _.sortBy(inheritors, 'sharePool');
    const sortedIntermediateShareGroups = _.chain(inheritors)
      .sortBy('sharePool')
      .groupBy('sharePool')
      .map(normalizeSharePool)
      .value();

    setBasicShareAnswers(new Array(inheritors?.length).fill(null));
    setIntermediateShareAnswers(new Array(sortedIntermediateShareGroups?.length + 2).fill(''));
    setFinalShareAnswers(new Array(inheritors?.length + 2).fill(''));

    const totalSharesPool = problem.intermediate_shares.inheritance_pool.total_shares;
    const totalShares = problem.intermediate_shares.share_pool[totalSharesPool];

    const expectedBasicShareAnswers = _.map(
      inheritorsSortedBySharePool,
      (inheritor) => problem.basic_shares[inheritor.key]
    );

    const expectedIntermediateShareAnswers = _.map(
      sortedIntermediateShareGroups,
      (group) => sharePools[group.pool]
    );
    const expectedIntermediateAnswers = [
      totalShares,
      ...expectedIntermediateShareAnswers,
      totalShares - _.sum(expectedIntermediateShareAnswers) // Remainder
    ];

    const expectedFinalShareAnswers = _.map(
      inheritorsSortedBySharePool,
      (inheritor) => problem.final_shares[inheritor.key]
    );
    const expectedFinalAnswers = [
      problem.final_shares.total_shares,
      ...expectedFinalShareAnswers,
      problem.final_shares.remainder
    ];

    setProblemData({
      inheritorsSortedBySharePool,
      sortedIntermediateShareGroups,
      answers: {
        basic: expectedBasicShareAnswers,
        intermediate: expectedIntermediateAnswers,
        final: expectedFinalAnswers
      }
    });
  }, [problem]);

  // TODO: isDisabled should be part of the input props
  useEffect(() => {
    const inputProps = _.map(basicShareAnswers, (answer, i) => {
      const isCorrectAnswer = problemData.answers.basic[i] === answer;
      const resultBackgroundColor = isCorrectAnswer ? answerColors.CORRECT : answerColors.INCORRECT;
      return {
        value: answer,
        backgroundColor:
          showResults && answer !== null ? resultBackgroundColor : answerColors.NOT_ANSWERED
      };
    });
    setBasicShareInputProps(inputProps);
  }, [problemData, basicShareAnswers, showResults]);

  useEffect(() => {
    const inputProps = _.map(intermediateShareAnswers, (answer, i) => {
      const isCorrectAnswer = problemData.answers.intermediate[i] == answer;
      const resultBackgroundColor = isCorrectAnswer ? answerColors.CORRECT : answerColors.INCORRECT;
      let size = 1;
      if (i >= 1 && i < problemData.inheritorsSortedBySharePool.length - 1) {
        size = problemData.sortedIntermediateShareGroups[i].groupSize;
      }
      return {
        value: answer,
        size: size,
        backgroundColor:
          showResults && level >= levels.TWO && answer !== ''
            ? resultBackgroundColor
            : answerColors.NOT_ANSWERED
      };
    });
    setIntermediateShareInputProps(inputProps);
  }, [problemData, intermediateShareAnswers, level, showResults]);

  useEffect(() => {
    const inputProps = _.map(finalShareAnswers, (answer, i) => {
      const isCorrectAnswer = problemData.answers.final[i] == answer;
      const resultBackgroundColor = isCorrectAnswer ? answerColors.CORRECT : answerColors.INCORRECT;
      return {
        value: answer,
        backgroundColor:
          showResults && level === levels.THREE && answer !== ''
            ? resultBackgroundColor
            : answerColors.NOT_ANSWERED
      };
    });
    setFinalShareInputProps(inputProps);
  }, [finalShareAnswers, problemData, showResults, level]);

  useEffect(() => {
    const areCorrect = _.every(
      _.map(basicShareAnswers, (answer, i) => problemData.answers.basic[i] === answer)
    );
    setAreBasicSharesCorrect(areCorrect);
  }, [basicShareAnswers, problemData]);

  useEffect(() => {
    const areCorrect = _.every(
      _.map(intermediateShareAnswers, (answer, i) => problemData.answers.intermediate[i] == answer)
    );
    setAreIntermediateSharesCorrect(areCorrect);
  }, [intermediateShareAnswers, problemData]);

  useEffect(() => {
    const areCorrect = _.every(
      _.map(finalShareAnswers, (answer, i) => problemData.answers.final[i] == answer)
    );
    setAreFinalSharesCorrect(areCorrect);
  }, [finalShareAnswers, problemData]);

  const checkAnswers = () => {
    if (areBasicSharesCorrect && level === levels.ONE) {
      setLevel(levels.TWO);
    } else if (areBasicSharesCorrect && areIntermediateSharesCorrect && level === levels.TWO) {
      setLevel(levels.THREE);
    } else if (
      areBasicSharesCorrect &&
      areIntermediateSharesCorrect &&
      areFinalSharesCorrect &&
      level === levels.THREE
    ) {
      setIsProblemSolved(true);
      // setSolvedProblems(_.assign(solvedProblems, { [problemIndex]: true }));
      alert('Success');
    }
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
    isProblemSolved,
    inheritors: problemData?.inheritorsSortedBySharePool,
    level,
    basicShareInputProps,
    intermediateShareInputProps,
    finalShareInputProps,
    updateBasicShareAnswers,
    updateIntermediateShareAnswers,
    updateFinalShareAnswers,
    checkAnswers
  };
};

export default useProblem;
