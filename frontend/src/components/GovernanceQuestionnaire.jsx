import React, { useEffect, useMemo, useState } from 'react';
import { ArrowLeft, ArrowRight, CheckCircle2, ClipboardCheck, Save, ShieldCheck } from 'lucide-react';
import { Link } from 'react-router-dom';
import { fetchGovernanceQuestions, submitGovernanceAssessment } from '../lib/api';
import { mockGovernanceQuestions, mockGovernanceScore } from '../data/mockGovernance';
import './AssessmentPages.css';

const answerLabel = (value) => value === true ? 'Yes' : value === false ? 'No' : value;

export default function GovernanceQuestionnaire() {
  const [questions, setQuestions] = useState(mockGovernanceQuestions);
  const [answers, setAnswers] = useState(() => JSON.parse(localStorage.getItem('governance-draft') || '{}'));
  const [current, setCurrent] = useState(0);
  const [notice, setNotice] = useState('Demo questions loaded.');
  const [submitted, setSubmitted] = useState(false);
  const question = questions[current];
  const answered = questions.filter((item) => answers[item.id] !== undefined && answers[item.id] !== '').length;
  const requiredComplete = questions.filter((item) => item.required).every((item) => answers[item.id] !== undefined && answers[item.id] !== '');
  const score = submitted ? mockGovernanceScore : Math.round((answered / questions.length) * 100);

  useEffect(() => {
    fetchGovernanceQuestions().then((payload) => {
      if (Array.isArray(payload) && payload.length) {
        setQuestions(payload);
        setNotice('Connected to governance question service.');
      }
    }).catch(() => undefined);
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
      await submitGovernanceAssessment(answers);
      setNotice('Assessment submitted to the governance service.');
    } catch {
      setNotice('Assessment captured locally. Connect the governance API to submit it centrally.');
    }
    setSubmitted(true);
  };

  const options = useMemo(() => question.type === 'yes_no' ? ['Yes', 'No', 'Partially'] : question.options || [], [question]);

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
          {submitted && <section className="score-card"><div><span className="assessment-kicker">Governance Completion</span><strong>{score}%</strong><p><CheckCircle2 size={15} /> Assessment complete</p></div><div><span>Questions answered</span><strong>{answered} / {questions.length}</strong></div><div><span>Governance maturity</span><strong>Tier {mockGovernanceScore.tier}</strong><small>{mockGovernanceScore.tierName}</small></div></section>}
        </section>
      </div>
    </main>
  );
}
