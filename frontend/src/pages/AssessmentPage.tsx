import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import {
  sessionsApi,
  StartSessionResponse,
  SanitizedQuestionItem,
  ActiveSessionStatusResponse,
} from '../api/sessions';
import { codingApi, CodingExecutionResponse } from '../api/coding';
import { curriculumApi, TopicSummary } from '../api/curriculum';
import { Domain } from '../types';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { ErrorBanner } from '../components/ErrorBanner';
import {
  CheckCircle2,
  XCircle,
  Clock,
  Target,
  HelpCircle,
  ArrowRight,
  Sparkles,
  Info,
  Award,
  Code,
  Play,
  RotateCcw,
  Terminal,
  ShieldCheck,
  AlertCircle,
  Layers,
  ChevronRight,
  RefreshCw,
} from 'lucide-react';

const SESSION_STORAGE_KEY = 'ml_active_session_id';

export const AssessmentPage: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const [domains, setDomains] = useState<Domain[]>([]);
  const [topics, setTopics] = useState<TopicSummary[]>([]);
  const [selectedDomainId, setSelectedDomainId] = useState<string>(
    (location.state as any)?.domainId || ''
  );
  const [selectedTopicId, setSelectedTopicId] = useState<string>(
    (location.state as any)?.topicId || ''
  );
  const [sessionKind, setSessionKind] = useState<'ADAPTIVE' | 'DIAGNOSTIC'>('ADAPTIVE');
  const [isStarting, setIsStarting] = useState(false);
  const [isLoadingActiveSession, setIsLoadingActiveSession] = useState(true);

  // Active Test State
  const [activeSession, setActiveSession] = useState<StartSessionResponse | null>(null);
  const [sessionMeta, setSessionMeta] = useState<{
    domain_name?: string;
    topic_name?: string;
    total_questions_estimated: number;
    warning?: string;
  }>({ total_questions_estimated: 15 });
  const [currentItem, setCurrentItem] = useState<SanitizedQuestionItem | null>(null);
  const [selectedOption, setSelectedOption] = useState<string>('');
  const [confidence, setConfidence] = useState<number>(2); // 1 = low, 2 = medium, 3 = high
  const [startTime, setStartTime] = useState<number>(Date.now());
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showRationale, setShowRationale] = useState(false);

  // Coding Sandbox State
  const [codeContent, setCodeContent] = useState<string>('');
  const [isRunningCode, setIsRunningCode] = useState<boolean>(false);
  const [sandboxResult, setSandboxResult] = useState<CodingExecutionResponse | null>(null);

  // Immediate feedback modal
  const [feedback, setFeedback] = useState<{
    isCorrect: boolean;
    explanation: string;
    misconception?: string;
    updatedTheta: number;
  } | null>(null);

  // Session Completed State
  const [completionSummary, setCompletionSummary] = useState<{
    sessionId: string;
    totalQuestions: number;
    finalTheta: number;
    domainName?: string;
    topicName?: string;
  } | null>(null);

  // Load Curriculum Domains and Topics
  useEffect(() => {
    const loadCurriculum = async () => {
      try {
        const [domainsData, topicsData] = await Promise.all([
          curriculumApi.getDomains(),
          curriculumApi.getTopics(),
        ]);
        setDomains(domainsData);
        setTopics(topicsData);

        // If topicId was passed via location.state, ensure its domain is selected
        const stateTopicId = (location.state as any)?.topicId;
        if (stateTopicId) {
          const match = topicsData.find((t) => t.id === stateTopicId);
          if (match && !selectedDomainId) {
            setSelectedDomainId(match.domain_id);
          }
        }
      } catch (err) {
        console.warn('Could not load curriculum data:', err);
      }
    };
    loadCurriculum();
  }, [location.state]);

  // Session Resumption on Page Refresh / Re-entry
  useEffect(() => {
    const resumeSavedSession = async () => {
      const savedSessionId = sessionStorage.getItem(SESSION_STORAGE_KEY);
      if (!savedSessionId) {
        setIsLoadingActiveSession(false);
        return;
      }

      try {
        const status: ActiveSessionStatusResponse = await sessionsApi.getCurrentSession(savedSessionId);
        if (status.is_completed) {
          sessionStorage.removeItem(SESSION_STORAGE_KEY);
          setIsLoadingActiveSession(false);
        } else if (status.current_item) {
          setActiveSession({
            session_id: status.session_id,
            kind: status.kind,
            first_item: status.current_item,
            started_at: '',
            domain_name: status.domain_name,
            topic_name: status.topic_name,
            total_questions_estimated: status.total_questions_estimated,
            warning: status.warning,
          });
          setSessionMeta({
            domain_name: status.domain_name,
            topic_name: status.topic_name,
            total_questions_estimated: status.total_questions_estimated || 15,
            warning: status.warning,
          });
          setCurrentItem(status.current_item);
          setStartTime(Date.now());
          setCodeContent(status.current_item.code_template || '# Write your solution here\n');
        }
      } catch (err) {
        console.warn('Could not resume existing session:', err);
        sessionStorage.removeItem(SESSION_STORAGE_KEY);
      } finally {
        setIsLoadingActiveSession(false);
      }
    };

    resumeSavedSession();
  }, []);

  // Filter topics by selected domain if one is chosen
  const filteredTopics = selectedDomainId
    ? topics.filter((t) => t.domain_id === selectedDomainId)
    : topics;

  const handleStartSession = async () => {
    try {
      setIsStarting(true);
      setError(null);
      const res = await sessionsApi.startSession({
        domain_id: selectedDomainId || undefined,
        topic_id: selectedTopicId || undefined,
        kind: sessionKind,
      });

      sessionStorage.setItem(SESSION_STORAGE_KEY, res.session_id);
      setActiveSession(res);
      setSessionMeta({
        domain_name: res.domain_name,
        topic_name: res.topic_name,
        total_questions_estimated: res.total_questions_estimated || 15,
        warning: res.warning,
      });
      setCurrentItem(res.first_item);
      setStartTime(Date.now());
      setSelectedOption('');
      setCodeContent(res.first_item?.code_template || '# Write your solution here\n');
      setSandboxResult(null);
      setFeedback(null);
      setCompletionSummary(null);
    } catch (err: any) {
      setError(err.message || 'Failed to start adaptive session.');
    } finally {
      setIsStarting(false);
    }
  };

  const handleRunCodeInSandbox = async () => {
    if (!currentItem) return;
    if (!codeContent.trim()) {
      setError('Please write some Python code before executing in the sandbox.');
      return;
    }

    try {
      setIsRunningCode(true);
      setError(null);
      const result = await codingApi.executeCode({
        code: codeContent,
        language: 'python',
        item_id: currentItem.id,
        test_cases: currentItem.visible_test_cases,
      });
      setSandboxResult(result);
    } catch (err: any) {
      setError(err.message || 'Error executing sandboxed code.');
    } finally {
      setIsRunningCode(false);
    }
  };

  const handleKeyDownInEditor = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Tab') {
      e.preventDefault();
      const textarea = e.currentTarget;
      const start = textarea.selectionStart;
      const end = textarea.selectionEnd;
      const updatedCode = codeContent.substring(0, start) + '    ' + codeContent.substring(end);
      setCodeContent(updatedCode);
      setTimeout(() => {
        textarea.selectionStart = textarea.selectionEnd = start + 4;
      }, 0);
    }
  };

  const handleSubmitAnswer = async () => {
    if (!activeSession || !currentItem) return;

    const isCoding = currentItem.item_type === 'CODING';
    const responsePayload = isCoding ? codeContent.trim() : selectedOption;

    if (!responsePayload) {
      setError(
        isCoding
          ? 'Please write your code solution before submitting.'
          : 'Please select an answer choice before submitting.'
      );
      return;
    }

    const latencyMs = Date.now() - startTime;

    try {
      setIsSubmitting(true);
      setError(null);

      const res = await sessionsApi.submitResponse(activeSession.session_id, {
        item_id: currentItem.id,
        response_value: responsePayload,
        latency_ms: latencyMs,
        confidence_rating: confidence,
      });

      // Show immediate feedback
      setFeedback({
        isCorrect: res.is_correct,
        explanation: res.explanation,
        misconception: res.misconception_feedback,
        updatedTheta: res.updated_theta,
      });

      if (res.is_completed) {
        sessionStorage.removeItem(SESSION_STORAGE_KEY);
        setTimeout(() => {
          setCompletionSummary({
            sessionId: activeSession.session_id,
            totalQuestions: currentItem.question_number,
            finalTheta: res.updated_theta,
            domainName: sessionMeta.domain_name,
            topicName: sessionMeta.topic_name,
          });
          setActiveSession(null);
          setCurrentItem(null);
        }, 1200);
      } else if (res.next_item) {
        setTimeout(() => {
          const nextItem = res.next_item!;
          setCurrentItem(nextItem);
          setSelectedOption('');
          setCodeContent(nextItem.code_template || '# Write your solution here\n');
          setSandboxResult(null);
          setStartTime(Date.now());
          setFeedback(null);
          setShowRationale(false);
        }, 1100);
      }
    } catch (err: any) {
      setError(err.message || 'Error recording answer submission.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleAbandonSession = () => {
    if (window.confirm('Are you sure you want to exit this assessment? Your current responses have been saved.')) {
      sessionStorage.removeItem(SESSION_STORAGE_KEY);
      setActiveSession(null);
      setCurrentItem(null);
      navigate('/');
    }
  };

  if (isLoadingActiveSession) {
    return (
      <div className="max-w-3xl mx-auto px-4 py-16 text-center">
        <LoadingSpinner message="Checking active session status..." />
      </div>
    );
  }

  // Completion Summary Screen
  if (completionSummary) {
    return (
      <div className="max-w-2xl mx-auto px-4 py-12 space-y-6">
        <div className="bg-white p-8 rounded-2xl border border-slate-200 shadow-sm text-center space-y-6">
          <div className="w-16 h-16 bg-emerald-50 text-emerald-600 rounded-full flex items-center justify-center mx-auto border border-emerald-100">
            <CheckCircle2 className="w-8 h-8" />
          </div>

          <div>
            <span className="text-xs font-bold text-emerald-600 uppercase tracking-wider">
              Assessment Completed
            </span>
            <h1 className="text-2xl font-bold text-slate-900 mt-1">
              Diagnostic Calibration Finalized
            </h1>
            <p className="text-sm text-slate-500 mt-1">
              All responses recorded and psychometric parameters calibrated.
            </p>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 p-4 bg-slate-50 rounded-xl border border-slate-200 text-left">
            <div>
              <div className="text-[11px] text-slate-400 font-semibold uppercase">Topic</div>
              <div className="text-xs font-bold text-slate-800 truncate mt-0.5">
                {completionSummary.topicName || 'Full Placement'}
              </div>
            </div>
            <div>
              <div className="text-[11px] text-slate-400 font-semibold uppercase">Questions Answered</div>
              <div className="text-xs font-bold text-indigo-600 mt-0.5">
                {completionSummary.totalQuestions} Questions
              </div>
            </div>
            <div>
              <div className="text-[11px] text-slate-400 font-semibold uppercase">Final Ability ($\hat\theta$)</div>
              <div className="text-xs font-bold text-emerald-600 mt-0.5">
                {completionSummary.finalTheta.toFixed(2)}
              </div>
            </div>
          </div>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-3 pt-2">
            <button
              onClick={() => navigate(`/report/${completionSummary.sessionId}`)}
              className="w-full sm:w-auto inline-flex items-center justify-center px-6 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-sm rounded-lg transition shadow-sm"
            >
              <Award className="w-4 h-4 mr-2" />
              View Comprehensive Report
            </button>
            <button
              onClick={() => {
                setCompletionSummary(null);
                setSelectedTopicId('');
              }}
              className="w-full sm:w-auto inline-flex items-center justify-center px-5 py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold text-sm rounded-lg transition"
            >
              Start Another Topic
            </button>
          </div>
        </div>
      </div>
    );
  }

  // Pre-test configuration view
  if (!activeSession) {
    const selectedTopicObj = topics.find((t) => t.id === selectedTopicId);

    return (
      <div className="max-w-3xl mx-auto px-4 py-12 space-y-8">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 tracking-tight">Adaptive Assessment Center</h1>
          <p className="text-sm text-slate-500 mt-1">
            Psychometric 2-Parameter Logistic (2PL) Computerized Adaptive Testing with Bayesian IRT
          </p>
        </div>

        {error && <ErrorBanner message={error} />}

        <div className="bg-white p-8 rounded-2xl border border-slate-200 shadow-sm space-y-6">
          <div className="flex items-center space-x-3 text-indigo-600 bg-indigo-50/50 p-4 rounded-xl border border-indigo-100">
            <Info className="w-5 h-5 flex-shrink-0" />
            <p className="text-xs text-indigo-900 leading-relaxed">
              Our Item Response Theory (IRT) engine dynamically selects items maximizing Fisher Information
              around your latent ability estimate ($\theta$). Every topic assessment features 15 calibrated
              questions strictly bounded to your chosen topic.
            </p>
          </div>

          <div className="space-y-4">
            {/* Domain Selection */}
            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-slate-600 mb-1.5">
                Target Domain (Optional Filter)
              </label>
              <select
                value={selectedDomainId}
                onChange={(e) => {
                  setSelectedDomainId(e.target.value);
                  // Reset topic if selected topic doesn't belong to this domain
                  if (e.target.value) {
                    const match = topics.find(
                      (t) => t.id === selectedTopicId && t.domain_id === e.target.value
                    );
                    if (!match) setSelectedTopicId('');
                  }
                }}
                className="w-full px-3.5 py-2.5 border border-slate-200 rounded-lg text-sm bg-white text-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-600"
              >
                <option value="">All Domains (Select Any Topic Below)</option>
                {domains.map((dom) => (
                  <option key={dom.id} value={dom.id}>
                    {dom.name} ({dom.code})
                  </option>
                ))}
              </select>
            </div>

            {/* Topic Selection */}
            <div>
              <div className="flex items-center justify-between mb-1.5">
                <label className="block text-xs font-semibold uppercase tracking-wider text-slate-600">
                  Target Topic (Strict Boundary)
                </label>
                {selectedTopicObj && (
                  <span className="text-[11px] font-semibold text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
                    {selectedTopicObj.question_count} Calibrated Questions Available
                  </span>
                )}
              </div>
              <select
                value={selectedTopicId}
                onChange={(e) => {
                  setSelectedTopicId(e.target.value);
                  if (e.target.value) {
                    const topic = topics.find((t) => t.id === e.target.value);
                    if (topic) setSelectedDomainId(topic.domain_id);
                  }
                }}
                className="w-full px-3.5 py-2.5 border border-slate-200 rounded-lg text-sm bg-white text-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-600"
              >
                <option value="">Full Domain Assessment (Multi-Topic Sampling)</option>
                {filteredTopics.map((top) => (
                  <option key={top.id} value={top.id}>
                    {top.name} — {top.domain_name} ({top.question_count} questions)
                  </option>
                ))}
              </select>
              <p className="text-[11px] text-slate-400 mt-1">
                Selecting a specific topic guarantees that all questions in the test belong exclusively to that topic.
              </p>
            </div>

            {/* Assessment Protocol */}
            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-slate-600 mb-1.5">
                Assessment Protocol
              </label>
              <div className="grid grid-cols-2 gap-3">
                <button
                  type="button"
                  onClick={() => setSessionKind('ADAPTIVE')}
                  className={`p-3.5 rounded-xl border text-left transition ${
                    sessionKind === 'ADAPTIVE'
                      ? 'bg-indigo-50/70 border-indigo-500 text-indigo-900'
                      : 'bg-white border-slate-200 hover:bg-slate-50 text-slate-700'
                  }`}
                >
                  <div className="font-semibold text-xs flex items-center justify-between">
                    <span>Computer Adaptive (CAT)</span>
                    <Sparkles className="w-3.5 h-3.5 text-indigo-500" />
                  </div>
                  <div className="text-[11px] text-slate-500 mt-1">
                    Calibrates difficulty after each answer via 2PL IRT Fisher Information. Target 15 questions.
                  </div>
                </button>

                <button
                  type="button"
                  onClick={() => setSessionKind('DIAGNOSTIC')}
                  className={`p-3.5 rounded-xl border text-left transition ${
                    sessionKind === 'DIAGNOSTIC'
                      ? 'bg-indigo-50/70 border-indigo-500 text-indigo-900'
                      : 'bg-white border-slate-200 hover:bg-slate-50 text-slate-700'
                  }`}
                >
                  <div className="font-semibold text-xs flex items-center justify-between">
                    <span>Diagnostic Benchmark</span>
                    <Target className="w-3.5 h-3.5 text-slate-400" />
                  </div>
                  <div className="text-[11px] text-slate-500 mt-1">
                    Broad prerequisite validation across skill boundaries to locate foundational gaps.
                  </div>
                </button>
              </div>
            </div>
          </div>

          <div className="pt-4 border-t border-slate-100 flex items-center justify-between">
            <span className="text-xs text-slate-500">
              Target length: <strong>15 questions</strong> per assessment
            </span>
            <button
              onClick={handleStartSession}
              disabled={isStarting}
              className="inline-flex items-center px-6 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-sm rounded-lg transition shadow-sm disabled:opacity-50"
            >
              {isStarting ? 'Initializing CAT Engine...' : 'Start Assessment'}
              {!isStarting && <ArrowRight className="w-4 h-4 ml-2" />}
            </button>
          </div>
        </div>
      </div>
    );
  }

  const isCodingQuestion = currentItem?.item_type === 'CODING';
  const currentQNum = currentItem?.question_number || 1;
  const totalQEst = currentItem?.total_questions_estimated || sessionMeta.total_questions_estimated || 15;
  const progressPercent = Math.min(100, Math.round(((currentQNum - 1) / totalQEst) * 100));

  return (
    <div className="max-w-4xl mx-auto px-4 py-8 space-y-6">
      {/* Session Breadcrumb & Exit */}
      <div className="flex items-center justify-between text-xs text-slate-500 pb-2">
        <div className="flex items-center space-x-1.5 flex-wrap">
          <span className="font-semibold text-slate-700">
            {currentItem?.domain_name || sessionMeta.domain_name || 'Placement Assessment'}
          </span>
          {(currentItem?.topic_name || sessionMeta.topic_name) && (
            <>
              <ChevronRight className="w-3.5 h-3.5 text-slate-400" />
              <span className="font-bold text-indigo-600">
                {currentItem?.topic_name || sessionMeta.topic_name}
              </span>
            </>
          )}
        </div>
        <button
          onClick={handleAbandonSession}
          className="text-slate-400 hover:text-rose-600 text-xs transition"
        >
          Exit Assessment
        </button>
      </div>

      {/* Test Progress Bar & Question Counter */}
      <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm space-y-2">
        <div className="flex items-center justify-between text-xs">
          <div className="flex items-center space-x-2">
            <span className="font-bold text-slate-900 text-sm">
              Question {currentQNum} of {totalQEst}
            </span>
            <span className="bg-indigo-50 text-indigo-700 border border-indigo-100 px-2 py-0.5 rounded text-[11px] font-semibold">
              {activeSession.kind === 'ADAPTIVE' ? 'Adaptive 2PL IRT' : activeSession.kind}
            </span>
            {isCodingQuestion && (
              <span className="bg-emerald-50 text-emerald-800 border border-emerald-200 px-2 py-0.5 rounded text-[11px] font-semibold flex items-center space-x-1">
                <Code className="w-3 h-3" />
                <span>Interactive Sandbox</span>
              </span>
            )}
          </div>
          <div className="flex items-center space-x-1.5 text-slate-500 font-medium">
            <Clock className="w-3.5 h-3.5" />
            <span>Progress: {progressPercent}%</span>
          </div>
        </div>

        {/* Visual Progress Bar */}
        <div className="w-full bg-slate-100 h-2.5 rounded-full overflow-hidden">
          <div
            className="bg-indigo-600 h-full rounded-full transition-all duration-300"
            style={{ width: `${Math.max(4, progressPercent)}%` }}
          />
        </div>
      </div>

      {/* Shortage or Session Warning Banner */}
      {(sessionMeta.warning || currentItem?.warning) && (
        <div className="p-3 bg-amber-50 border border-amber-200 text-amber-800 rounded-xl text-xs flex items-center space-x-2 shadow-sm">
          <AlertCircle className="w-4 h-4 text-amber-600 flex-shrink-0" />
          <span>{sessionMeta.warning || currentItem?.warning}</span>
        </div>
      )}

      {error && <ErrorBanner message={error} />}

      {/* Main Question Card */}
      {currentItem && (
        <div className="bg-white p-6 sm:p-8 rounded-2xl border border-slate-200 shadow-sm space-y-6">
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-[11px] font-semibold text-indigo-600 tracking-wide uppercase">
                Item ID: {currentItem.id.slice(0, 8)}...
              </span>
              <button
                type="button"
                onClick={() => setShowRationale(!showRationale)}
                className="text-xs text-slate-400 hover:text-indigo-600 inline-flex items-center transition"
              >
                <HelpCircle className="w-3.5 h-3.5 mr-1" />
                {showRationale ? 'Hide item rationale' : 'Why this question?'}
              </button>
            </div>

            {showRationale && (
              <div className="p-3 bg-slate-50 rounded-lg border border-slate-200 text-xs text-slate-600 space-y-1">
                <div className="font-semibold text-slate-800">Fisher Information Selection Strategy:</div>
                <div>
                  {typeof currentItem.selection_explanation === 'object' && currentItem.selection_explanation !== null ? (
                    <div>
                      <p>{currentItem.selection_explanation.explanation_text}</p>
                      <div className="mt-1 flex gap-4 text-[11px] text-slate-500">
                        <span>Strategy: <strong>{currentItem.selection_explanation.selection_strategy}</strong></span>
                        {currentItem.selection_explanation.fisher_information_units && (
                          <span>Fisher Info: <strong>{currentItem.selection_explanation.fisher_information_units}</strong></span>
                        )}
                      </div>
                    </div>
                  ) : (
                    <p>{String(currentItem.selection_explanation || 'Calibrated 2PL IRT item selection')}</p>
                  )}
                </div>
              </div>
            )}

            <div className="text-base sm:text-lg font-medium text-slate-900 leading-relaxed whitespace-pre-wrap">
              {currentItem.stem}
            </div>
          </div>

          {/* CODING QUESTION WORKSPACE */}
          {isCodingQuestion ? (
            <div className="space-y-4 pt-2">
              <div className="flex items-center justify-between text-xs">
                <div className="flex items-center space-x-2">
                  <span className="bg-slate-900 text-slate-100 font-mono px-2.5 py-1 rounded text-xs flex items-center space-x-1.5">
                    <Terminal className="w-3.5 h-3.5 text-emerald-400" />
                    <span>Python 3.11</span>
                  </span>
                  <span className="text-slate-500 text-[11px] flex items-center space-x-1">
                    <ShieldCheck className="w-3.5 h-3.5 text-indigo-600" />
                    <span>Sandboxed Subprocess</span>
                  </span>
                </div>
                <button
                  type="button"
                  onClick={() => setCodeContent(currentItem.code_template || '')}
                  className="text-slate-500 hover:text-slate-700 text-xs inline-flex items-center space-x-1"
                >
                  <RotateCcw className="w-3.5 h-3.5" />
                  <span>Reset Code</span>
                </button>
              </div>

              {/* Code Editor */}
              <div className="rounded-xl border border-slate-700 bg-slate-950 overflow-hidden shadow-inner">
                <div className="bg-slate-900 px-4 py-2 text-[11px] text-slate-400 font-mono flex items-center justify-between border-b border-slate-800">
                  <span>solution.py</span>
                  <span>Tab key inserts 4 spaces</span>
                </div>
                <textarea
                  value={codeContent}
                  onChange={(e) => setCodeContent(e.target.value)}
                  onKeyDown={handleKeyDownInEditor}
                  rows={12}
                  className="w-full p-4 font-mono text-sm bg-slate-950 text-emerald-400 focus:outline-none focus:ring-1 focus:ring-indigo-500 resize-y leading-relaxed"
                  placeholder="# Write your Python implementation here..."
                  spellCheck={false}
                />
              </div>

              {/* Visible Example Test Cases Preview */}
              {currentItem.visible_test_cases && currentItem.visible_test_cases.length > 0 && (
                <div className="p-4 bg-slate-50 rounded-xl border border-slate-200 space-y-2">
                  <div className="text-xs font-semibold text-slate-700 uppercase tracking-wider">
                    Example Test Cases:
                  </div>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs font-mono">
                    {currentItem.visible_test_cases.map((tc, idx) => (
                      <div key={idx} className="bg-white p-2.5 rounded-lg border border-slate-200">
                        <div className="text-slate-500 text-[10px]">Case {idx + 1}:</div>
                        {tc.input && <div className="text-slate-700 truncate">In: {tc.input}</div>}
                        <div className="text-emerald-700 truncate font-semibold">Expected: {tc.expected_output}</div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Run Test Cases Action */}
              <div className="flex items-center justify-between pt-1">
                <button
                  type="button"
                  onClick={handleRunCodeInSandbox}
                  disabled={isRunningCode || !codeContent.trim()}
                  className="inline-flex items-center px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white font-semibold text-xs rounded-lg transition shadow-sm disabled:opacity-50"
                >
                  <Play className="w-3.5 h-3.5 mr-1.5" />
                  {isRunningCode ? 'Running Sandbox...' : 'Run Test Cases'}
                </button>
                <span className="text-[11px] text-slate-400">
                  Execution terminates after 2.0s
                </span>
              </div>

              {/* Execution Results Panel */}
              {sandboxResult && (
                <div className={`p-4 rounded-xl border text-xs space-y-3 ${
                  sandboxResult.all_passed
                    ? 'bg-emerald-50 border-emerald-200 text-emerald-950'
                    : 'bg-amber-50 border-amber-200 text-amber-950'
                }`}>
                  <div className="flex items-center justify-between font-bold">
                    <div className="flex items-center space-x-1.5">
                      {sandboxResult.all_passed ? (
                        <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                      ) : (
                        <AlertCircle className="w-4 h-4 text-amber-600" />
                      )}
                      <span>
                        {sandboxResult.all_passed
                          ? `All Test Cases Passed (${sandboxResult.passed_count}/${sandboxResult.total_count})`
                          : `Some Tests Failed (${sandboxResult.passed_count}/${sandboxResult.total_count} Passed)`}
                      </span>
                    </div>
                    <span className="text-[11px] text-slate-500 font-mono">
                      Latency: {sandboxResult.total_latency_ms} ms
                    </span>
                  </div>

                  {sandboxResult.error && (
                    <div className="p-2.5 bg-rose-100 text-rose-800 rounded font-mono text-[11px]">
                      {sandboxResult.error}
                    </div>
                  )}

                  {/* Individual Test Case Results */}
                  {sandboxResult.test_results && sandboxResult.test_results.length > 0 && (
                    <div className="space-y-1.5">
                      {sandboxResult.test_results.map((tr) => (
                        <div
                          key={tr.test_case_number}
                          className="p-2.5 rounded bg-white border border-slate-200 flex flex-col gap-1 text-[11px] font-mono"
                        >
                          <div className="flex items-center justify-between">
                            <span className="font-semibold text-slate-700">
                              Test #{tr.test_case_number} {tr.is_hidden && '(Hidden Evaluation Case)'}
                            </span>
                            <span className={tr.passed ? 'text-emerald-600 font-bold' : 'text-rose-600 font-bold'}>
                              {tr.passed ? 'PASSED' : tr.timed_out ? 'TIMED OUT' : 'FAILED'}
                            </span>
                          </div>
                          {!tr.is_hidden && (
                            <div className="text-slate-600">
                              <div>Expected: <span className="text-slate-900">{tr.expected_output}</span></div>
                              <div>Actual: <span className="text-slate-900">{tr.actual_output || '<no output>'}</span></div>
                              {tr.error && <div className="text-rose-600">{tr.error}</div>}
                            </div>
                          )}
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}
            </div>
          ) : (
            /* MCQ OPTIONS LIST */
            <div className="space-y-3 pt-2">
              {currentItem.options.map((opt) => {
                const isSelected = selectedOption === opt.id;
                return (
                  <button
                    key={opt.id}
                    type="button"
                    onClick={() => setSelectedOption(opt.id)}
                    className={`w-full text-left p-4 rounded-xl border text-sm transition flex items-start space-x-3 ${
                      isSelected
                        ? 'bg-indigo-50/70 border-indigo-600 text-indigo-950 font-medium shadow-sm'
                        : 'bg-white border-slate-200 hover:border-slate-300 text-slate-800'
                    }`}
                  >
                    <span
                      className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0 mt-0.5 ${
                        isSelected
                          ? 'bg-indigo-600 text-white'
                          : 'bg-slate-100 text-slate-600'
                      }`}
                    >
                      {opt.id}
                    </span>
                    <span className="leading-snug">{opt.text}</span>
                  </button>
                );
              })}
            </div>
          )}

          {/* Confidence Rating Slider */}
          <div className="pt-4 border-t border-slate-100">
            <label className="block text-xs font-semibold text-slate-600 mb-2">
              Certainty / Confidence Level:
            </label>
            <div className="grid grid-cols-3 gap-2 text-xs">
              {[
                { val: 1, label: 'Unsure / Guessing' },
                { val: 2, label: 'Fairly Confident' },
                { val: 3, label: 'Highly Certain' },
              ].map((c) => (
                <button
                  key={c.val}
                  type="button"
                  onClick={() => setConfidence(c.val)}
                  className={`py-2 px-3 rounded-lg border transition font-medium text-center ${
                    confidence === c.val
                      ? 'bg-slate-800 text-white border-slate-800'
                      : 'bg-slate-50 text-slate-600 border-slate-200 hover:bg-slate-100'
                  }`}
                >
                  {c.label}
                </button>
              ))}
            </div>
          </div>

          {/* Action Row */}
          <div className="pt-4 border-t border-slate-100 flex items-center justify-between">
            <span className="text-xs text-slate-400">
              Response latency & calibration metrics logged.
            </span>
            <button
              onClick={handleSubmitAnswer}
              disabled={isSubmitting || (isCodingQuestion ? !codeContent.trim() : !selectedOption)}
              className="inline-flex items-center px-6 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-sm rounded-lg transition shadow-sm disabled:opacity-50"
            >
              {isSubmitting ? 'Evaluating Response...' : 'Submit & Next Question'}
              {!isSubmitting && <ArrowRight className="w-4 h-4 ml-2" />}
            </button>
          </div>
        </div>
      )}

      {/* Immediate diagnostic feedback alert */}
      {feedback && (
        <div
          className={`p-4 rounded-xl border text-xs transition ${
            feedback.isCorrect
              ? 'bg-emerald-50 border-emerald-200 text-emerald-900'
              : 'bg-rose-50 border-rose-200 text-rose-900'
          }`}
        >
          <div className="font-bold flex items-center space-x-1.5 mb-1">
            {feedback.isCorrect ? (
              <CheckCircle2 className="w-4 h-4 text-emerald-600" />
            ) : (
              <XCircle className="w-4 h-4 text-rose-600" />
            )}
            <span>{feedback.isCorrect ? 'Correct Answer' : 'Incorrect Response'}</span>
          </div>
          <p className="leading-relaxed">{feedback.explanation}</p>
          {feedback.misconception && (
            <p className="mt-1.5 font-semibold text-rose-700">
              Diagnostic Tag: {feedback.misconception}
            </p>
          )}
          <div className="mt-2 text-[11px] text-slate-500 font-medium">
            Posterior Ability Estimate updated: $\hat\theta = {feedback.updatedTheta.toFixed(2)}$
          </div>
        </div>
      )}
    </div>
  );
};
