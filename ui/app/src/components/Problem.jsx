import _ from 'lodash';
import { useEffect } from 'react';
import { Inheritor, BasicShareSelect, IntermediateShareInput, FinalShareInput } from './components';
import useProblem from '../hooks/useProblem';
import { levels } from '../constants';

const Problem = ({ problem, requiredLevels, onProblemSolved }) => {
  const {
    isProblemSolved,
    inheritors,
    level,
    basicShareInputProps,
    intermediateShareInputProps,
    finalShareInputProps,
    areFinalSharesRequired,
    updateBasicShareAnswers,
    updateIntermediateShareAnswers,
    updateFinalShareAnswers,
    checkAnswers,
    showAnswers,
  } = useProblem(problem, requiredLevels);

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

  const levelTwoAndThreePlaceholder = _.chain(inheritors.length + 3)
    .range()
    .map((i) => <div key={i} className="neutral"></div>)
    .value();

  const levelTwoContent =
    level === levels.TWO || level === levels.THREE ? (
      <>
        <h3>Problem Base</h3>
        {intermediateShareInputs}
      </>
    ) : (
      levelTwoAndThreePlaceholder
    );

  const levelThreeContent =
    level === levels.TWO || level === levels.THREE ? (
      <>
        <h3>Problem Base</h3>
        {finalShareInputs}
      </>
    ) : (
      levelTwoAndThreePlaceholder
    );

  return (
    <>
      <div className="problem-container">
        <div className="column">
          <h3>Heir</h3>
          <div className="neutral"></div>
          {inheritorsDisplay}
          <div className='neutral'><h3>Remainder</h3></div>
        </div>
        <div className="column">
          <h3>Shares</h3>
          <div className="neutral"></div>
          {basicShareSelects}
          <div className="neutral"></div>
        </div>
        <div className="column">{levelTwoContent}</div>
        <div className="column" style={{ display: areFinalSharesRequired ? 'block' : 'none' }}>
          {levelThreeContent}
        </div>
      </div>
      <input type="button" value="Check Answer" onClick={checkAnswers} />
      <input type="button" value="Show Answer" onClick={showAnswers} />
    </>
  );
};

export default Problem;
