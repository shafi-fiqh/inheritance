import _ from 'lodash';
import { useState, useEffect } from 'react';

import { answerColors, levels } from '../constants';

const useProblems = (problems) => {
  const [level, setLevel] = useState(levels.ONE);
  const [problemIndex, setProblemIndex] = useState(0);
  const [showResults, setShowResults] = useState(false);
  const [problem, setProblem] = useState(problems[problemIndex]);

  const [intermediateShareAnswers, setIntermediateShareAnswers] = useState(null);
  const [basicShareAnswers, setBasicShareAnswers] = useState(null);
  const [basicShareInputProps, setBasicShareInputProps] = useState(null);
  const [areBasicSharesCorrect, setAreBasicSharesCorrect] = useState(false);

  const [intermediateShareInputProps, setIntermediateShareInputProps] = useState(null);
  const [areIntermediateSharesCorrect, setAreIntermediateSharesCorrect] = useState(null);

  const [finalShareAnswers, setFinalShareAnswers] = useState(null);
  const [finalShareInputProps, setFinalShareInputProps] = useState(null);
  const [areFinalSharesCorrect, setAreFinalSharesCorrect] = useState(null);
  const [problemData, setProblemData] = useState({});

  useEffect(() => {
    setProblem(problems[problemIndex]);
  }, [problems, problemIndex]);

  useEffect(() => {
    const normalizeInheritor = (index, inheritorKey) => {
      return {
        key: inheritorKey,
        sharePool: inheritancePool[inheritorKey]
      };
    };

    const inheritancePool = problem.intermediate_shares.inheritance_pool;
    const sharePools = problem.intermediate_shares.share_pool;

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
    setProblemData({
      inheritors,
      inheritancePool,
      sharePools,
      inheritorsSortedBySharePool,
      intermediateShareGroups,
      sortedIntermediateShareGroups
    });
  }, [problem]);

  useEffect(() => {
    setIntermediateShareAnswers(new Array(_.size(problemData.intermediateShareGroups)).fill(''));
  }, [problemData]);

  useEffect(() => {
    setBasicShareAnswers(new Array(problemData?.inheritors?.length).fill(null));
  }, [problemData]);
  useEffect(() => {
    setFinalShareAnswers(new Array(problemData?.inheritors?.length).fill(''));
  }, [problemData]);

  // TODO: isDisabled should be part of the input props
  useEffect(() => {
    const inputProps = _.map(basicShareAnswers, (answer, i) => {
      const resultBackgroundColor =
        problem.basic_shares[problemData?.inheritorsSortedBySharePool[i].key] === answer
          ? answerColors.CORRECT
          : answerColors.INCORRECT;
      return {
        value: answer,
        backgroundColor:
          showResults && answer !== null ? resultBackgroundColor : answerColors.NOT_ANSWERED
      };
    });
    setBasicShareInputProps(inputProps);
  }, [problem.basic_shares, problemData, basicShareAnswers, showResults]);

  useEffect(() => {
    const inputProps = _.map(intermediateShareAnswers, (answer, i) => {
      const resultBackgroundColor =
        problemData.sortedIntermediateShareGroups[i].answer == answer
          ? answerColors.CORRECT
          : answerColors.INCORRECT;
      return {
        value: answer,
        size: problemData.sortedIntermediateShareGroups[i].groupSize,
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
      const inheritor = problemData?.inheritorsSortedBySharePool[i].key;
      const resultBackgroundColor =
        problem.final_shares[inheritor] == answer ? answerColors.CORRECT : answerColors.INCORRECT;
      return {
        value: answer,
        backgroundColor:
          showResults && level === levels.THREE && answer !== ''
            ? resultBackgroundColor
            : answerColors.NOT_ANSWERED
      };
    });
    setFinalShareInputProps(inputProps);
  }, [finalShareAnswers, problem, problemData, showResults, level]);

  useEffect(() => {
    const areCorrect = _.every(
      _.map(
        basicShareAnswers,
        (answer, i) =>
          problem.basic_shares[problemData?.inheritorsSortedBySharePool[i].key] === answer
      )
    );
    setAreBasicSharesCorrect(areCorrect);
  }, [basicShareAnswers, problem, problemData]);

  useEffect(() => {
    const areCorrect = _.every(
      _.map(
        intermediateShareAnswers,
        (answer, i) => problemData.sortedIntermediateShareGroups[i].answer == answer
      )
    );
    setAreIntermediateSharesCorrect(areCorrect);
  }, [intermediateShareAnswers, problemData]);

  useEffect(() => {
    const areCorrect = _.every(
      _.map(
        finalShareAnswers,
        (answer, i) =>
          problem.final_shares[problemData?.inheritorsSortedBySharePool[i].key] == answer
      )
    );
    setAreFinalSharesCorrect(areCorrect);
  }, [finalShareAnswers, problem, problemData]);

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
      alert('Success');
      // setShowResults(false)
      // setProblemIndex(problemIndex + 1)
      // setLevel(levels.ONE)
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
    inheritors: problemData?.inheritorsSortedBySharePool,
    problem: problemIndex,
    level,
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
