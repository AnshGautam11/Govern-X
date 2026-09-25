import React, { useEffect, useMemo, useState } from 'react';
import { ArrowLeft, ArrowRight, CheckCircle2, ClipboardCheck, Save, ShieldCheck } from 'lucide-react';
import { Link } from 'react-router-dom';
import { fetchGovernanceQuestions, fetchGovernanceScore, fetchGovernanceResponses, submitGovernanceAssessment } from '../lib/api';
import './AssessmentPages.css';

const answerLabel = (value) => value === true ? 'Yes' : value === false ? 'No' : value;

function readGovernanceDraft() {
  try {
    const draft = JSON.parse(localStorage.getItem('governance-draft') || '{}');
    return draft && typeof draft === 'object' && !Array.isArray(draft) ? draft : {};
  } catch {
    return {};
  }
}

export default function GovernanceQuestionnaire() {
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState(readGovernanceDraft);
  const [current, setCurrent] = useState(0);
  const [notice, setNotice] = useState('Loading governance questions...');
  const [submitted, setSubmitted] = useState(false);
  const [score, setScore] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const question = questions[current];
  const answered = questions.filter((item) => answers[item.id] !== undefined && answers[item.id] !== '').length;
  const requiredComplete = questions.filter((item) => item.required).every((item) => answers[item.id] !== undefined && answers[item.id] !== '');

  useEffect(() => {
    let active = true;
    Promise.all([fetchGovernanceQuestions(), fetchGovernanceResponses(), fetchGovernanceScore()])
      .then(([questionPayload, responsePayload, scorePayload]) => {
        if (!active) return;
        const storedAnswers = Object.fromEntries(
          (responsePayload?.responses || []).map((response) => [response.question_key, response.answer ? 'Yes' : 'No'])
        );
        const activeQuestions = Array.isArray(questionPayload) ? questionPayload : [];
        const activeIds = new Set(activeQuestions.map((item) => item.id));
        setQuestions(activeQuestions);
        setAnswers((draft) => ({
          ...Object.fromEntries(Object.entries(storedAnswers).filter(([key]) => activeIds.has(key))),
          ...Object.fromEntries(Object.entries(draft).filter(([key]) => activeIds.has(key))),
        }));
        setScore(scorePayload);
        setNotice('Governance data loaded from the backend.');
        setError('');
      })
      .catch((loadError) => {
        if (active) {
          setError(loadError.message || 'Unable to load governance data.');
          setNotice('Governance data is unavailable. Retry to reconnect.');
        }
      })
      .finally(() => {
        if (active) setLoading(false);
      });
    return () => { active = false; };
  }, []);

  const updateAnswer = (value) => setAnswers((previous) => ({ ...previous, [question.id]: value }));
  const saveDraft = () => {
    localStorage.setItem('governance-draft', JSON.stringify(answers));
    setNotice('Draft saved locally.');
  };
  const goNext = () => {
    if (question.required && (answers[question.id] === undefined || answers[question.id] === '')) {
      setNotice('Please answer this required question before continuing.');
      return;
    }
    setNotice('');
    setCurrent((value) => Math.min(value + 1, questions.length - 1));
  };
  const submit = async () => {
    if (!requiredComplete) {
      setNotice('Complete all required questions before submitting.');
      return;
    }
    try {
      const persistedAnswers = Object.fromEntries(
        questions
          .filter((item) => answers[item.id] !== undefined && answers[item.id] !== '')
          .map((item) => [item.id, answerLabel(answers[item.id]) === 'Yes'])
      );
      await submitGovernanceAssessment(persistedAnswers);
      const [scorePayload, questionPayload] = await Promise.all([fetchGovernanceScore(), fetchGovernanceQuestions()]);
      setScore(scorePayload);
      setQuestions(Array.isArray(questionPayload) ? questionPayload : questions);
      localStorage.removeItem('governance-draft');
      setNotice('Assessment submitted and saved to the governance service.');
      setError('');
    } catch (submitError) {
      setNotice('Assessment was not saved. Retry after the governance service is available.');
      setError(submitError.message || 'Unable to submit the governance assessment.');
      return;
    }
    setSubmitted(true);
  };

  const options = useMemo(() => question?.type === 'yes_no' ? ['Yes', 'No'] : question?.options || [], [question]);

  if (loading) return <main className="assessment-page"><div className="risk-status-panel" role="status">Loading governance questionnaire...</div></main>;
  if (error && questions.length === 0) return <main className="assessment-page"><div className="risk-status-panel risk-error"><h1>Governance data unavailable</h1><p>{error}</p><button type="button" className="risk-retry" onClick={() => window.location.reload()}>Retry</button></div></main>;
  if (!question) return <main className="assessment-page"><div className="risk-status-panel"><p>No governance questions are configured.</p></div></main>;

  return (
    <main className="assessment-page">
      <header className="assessment-topbar">
        <Link to="/" className="assessment-back"><ArrowLeft size={16} /> Universe</Link>
        <div className="assessment-brand"><ShieldCheck size={18} /> GOVERN-X / GOVERNANCE</div>
        <Link to="/financial-risk" className="assessment-link">Financial risk</Link>
      </header>
      <div className="assessment-layout">
        <aside className="assessment-sidebar">
          <span className="assessment-kicker">Governance Assessment</span>
          <h1>Governance Assessment</h1>
          <p>Evaluate organizational governance controls and cybersecurity governance maturity.</p>
          <div className="assessment-progress-copy"><strong>{answered} of {questions.length}</strong> questions completed</div>
          <div className="assessment-progress"><span style={{ width: `${(answered / questions.length) * 100}%` }} /></div>
          <nav className="question-index" aria-label="Question navigation">
            {questions.map((item, index) => <button type="button" key={item.id} className={index === current ? 'current' : answers[item.id] !== undefined ? 'complete' : ''} onClick={() => setCurrent(index)}>{index + 1}<span>{item.id}</span></button>)}
          </nav>
        </aside>
        <section className="assessment-main">
          <div className="assessment-heading"><div><span className="assessment-kicker">Question {String(current + 1).padStart(2, '0')} / {String(questions.length).padStart(2, '0')}</span><h2>{question.question}</h2></div><span className="question-code">{question.id}</span></div>
          <div className="question-card">
            {question.required && <span className="required-label">Required</span>}
            {question.type === 'text' ? <label className="field-label" htmlFor="question-notes">Optional notes<textarea id="question-notes" value={answers[question.id] || ''} onChange={(event) => updateAnswer(event.target.value)} placeholder="Add evidence or context" /></label> : <fieldset className="answer-options"><legend>Select one response</legend>{options.map((option) => <label className={`answer-option ${answerLabel(answers[question.id]) === option ? 'selected' : ''}`} key={option}><input type="radio" name={question.id} checked={answerLabel(answers[question.id]) === option} onChange={() => updateAnswer(option)} /> <span>{option}</span></label>)}</fieldset>}
            <div className="question-actions"><button type="button" className="secondary-action" onClick={() => setCurrent((value) => Math.max(0, value - 1))} disabled={current === 0}><ArrowLeft size={15} /> Previous</button><button type="button" className="secondary-action" onClick={saveDraft}><Save size={15} /> Save</button>{current < questions.length - 1 ? <button type="button" className="primary-action" onClick={goNext}>Save & continue <ArrowRight size={15} /></button> : <button type="button" className="primary-action" onClick={submit} disabled={submitted}><ClipboardCheck size={15} /> Submit assessment</button>}</div>
            {notice && <p className="assessment-notice" role="status">{notice}</p>}
          </div>
          {error && <p className="assessment-notice" role="alert">{error}</p>}
          {submitted && score && <section className="score-card"><div><span className="assessment-kicker">Governance Completion</span><strong>{score.completion_percentage}%</strong><p><CheckCircle2 size={15} /> Assessment complete</p></div><div><span>Questions answered</span><strong>{score.answered} / {score.total}</strong></div><div><span>Governance score</span><strong>{score.score}%</strong><small>Calculated from saved responses</small></div></section>}
        </section>
      </div>
    </main>
  );
}
