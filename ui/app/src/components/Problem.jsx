import _ from 'lodash';
import { useEffect } from 'react';
import { Inheritor, BasicShareSelect, IntermediateShareInput, FinalShareInput } from './components';
import useProblem from '../hooks/useProblem';

const Problem = ({ problem, onProblemSolved }) => {
  const {
    isProblemSolved,
    inheritors,
    level,
    basicShareInputProps,
    intermediateShareInputProps,
    finalShareInputProps,
    updateBasicShareAnswers,
    updateIntermediateShareAnswers,
    updateFinalShareAnswers,
    checkAnswers
  } = useProblem(problem);

  useEffect(() => {
    if (isProblemSolved) {
      onProblemSolved();
    }
  }, [onProblemSolved, isProblemSolved]);

  const inheritorsDisplay = _.map(inheritors, (inheritor, i) => (
    <Inheritor key={inheritor.key} inheritor={inheritor} />
  ));

  const onBasicSharesChange = (changedIndex, value) => {
    const answers = _.map(basicShareInputProps, 'value');
    answers[changedIndex] = value;
    updateBasicShareAnswers(answers);
  };

  const basicShareSelects = _.map(basicShareInputProps, (input, i) => {
    return (
      <BasicShareSelect
        key={i}
        index={i}
        value={input.value}
        bgColor={input.backgroundColor}
        onSelect={onBasicSharesChange}
      />
    );
  });

  const onIntermediateSharesChange = (changedIndex, value) => {
    const answers = _.map(intermediateShareInputProps, 'value');
    answers[changedIndex] = value;
    updateIntermediateShareAnswers(answers);
  };

  const intermediateShareInputs = _.map(intermediateShareInputProps, (input, i) => {
    return (
      <IntermediateShareInput
        key={i}
        index={i}
        bgColor={input.backgroundColor}
        size={input.size}
        level={level}
        value={input.value}
        onChange={onIntermediateSharesChange}
      />
    );
  });

  const onFinalSharesChange = (changedIndex, value) => {
    const answers = _.map(finalShareInputProps, 'value');
    answers[changedIndex] = value;
    updateFinalShareAnswers(answers);
  };

  const finalShareInputs = _.map(finalShareInputProps, (input, i) => {
    return (
      <FinalShareInput
        key={i}
        index={i}
        level={level}
        value={input.value}
        bgColor={input.backgroundColor}
        onChange={onFinalSharesChange}
      />
    );
  });

  return (
    <>
      <div className="problem-container">
        <div className="column">{inheritorsDisplay}</div>
        <div className="column">{basicShareSelects}</div>
        <div className="column">{intermediateShareInputs}</div>
        <div className="column">{finalShareInputs}</div>
      </div>
      <input type="button" value="Check Answer" onClick={checkAnswers} />
    </>
  );
};

export default Problem;
