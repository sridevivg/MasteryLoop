import React, { useState, useEffect, useRef } from 'react';
import { useLocation } from 'react-router-dom';
import { tutorApi, ChatMessage, TutorChatPayload, AiDiagnosticsResponse } from '../api/tutor';
import { curriculumApi } from '../api/curriculum';
import { TutorMode, TutorLanguage, SourceCitation, Domain } from '../types';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { ErrorBanner } from '../components/ErrorBanner';
import {
  Sparkles,
  Send,
  HelpCircle,
  BookOpen,
  Bug,
  Users,
  Clock,
  ShieldAlert,
  ChevronDown,
  ChevronUp,
  Cpu,
  Layers,
  ArrowRight
} from 'lucide-react';

interface DisplayMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  mode?: TutorMode;
  language?: TutorLanguage;
  citations?: SourceCitation[];
  suggestions?: string[];
  providerUsed?: string;
  timestamp: string;
}

export const TutorPage: React.FC = () => {
  const location = useLocation();
  const preselectedSkillId = (location.state as any)?.skillId || '';

  const [mode, setMode] = useState<TutorMode>('TEACH_FROM_BASICS');
  const [language, setLanguage] = useState<TutorLanguage>('ENGLISH');
  const [skillId, setSkillId] = useState<string>(preselectedSkillId);
  const [inputMessage, setInputMessage] = useState<string>('');
  const [messages, setMessages] = useState<DisplayMessage[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [diagnostics, setDiagnostics] = useState<AiDiagnosticsResponse | null>(null);
  const [expandedCitationIdx, setExpandedCitationIdx] = useState<string | null>(null);

  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  useEffect(() => {
    const fetchDiag = async () => {
      try {
        const diag = await tutorApi.getDiagnostics();
        setDiagnostics(diag);
      } catch (err) {
        console.warn('Could not load AI diagnostics:', err);
      }
    };
    fetchDiag();
  }, []);

  const handleSendMessage = async (textToSend?: string) => {
    const text = (textToSend || inputMessage).trim();
    if (!text || isLoading) return;

    setError(null);
    const userMsg: DisplayMessage = {
      id: `user-${Date.now()}`,
      role: 'user',
      content: text,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    setMessages((prev) => [...prev, userMsg]);
    setInputMessage('');
    setIsLoading(true);

    // Build history for backend
    const apiHistory: ChatMessage[] = messages.slice(-4).map((m) => ({
      role: m.role,
      content: m.content,
    }));

    const payload: TutorChatPayload = {
      message: text,
      mode,
      language,
      skill_id: skillId || undefined,
      history: apiHistory,
    };

    try {
      const response = await tutorApi.chat(payload);

      const assistantMsg: DisplayMessage = {
        id: `asst-${Date.now()}`,
        role: 'assistant',
        content: response.response,
        mode: response.mode,
        language: response.language,
        citations: response.citations,
        suggestions: response.followup_suggestions,
        providerUsed: response.provider_used,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };

      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err: any) {
      setError(err.message || 'Socratic tutor generation error. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const modeDescriptions: Record<TutorMode, { label: string; icon: any; desc: string }> = {
    HINT: {
      label: 'Progressive Hints',
      icon: HelpCircle,
      desc: 'Provides structured guidance without leaking full solutions immediately.',
    },
    TEACH_FROM_BASICS: {
      label: 'Teach from Basics',
      icon: BookOpen,
      desc: 'Explains fundamental first-principles and prerequisite foundations.',
    },
    DEBUG: {
      label: 'Code Debugging',
      icon: Bug,
      desc: 'Isolates boundary conditions, off-by-one loops, and mutation errors.',
    },
    INTERVIEW: {
      label: 'Mock Interview',
      icon: Users,
      desc: 'Technical placement interview simulation with complexity trade-offs.',
    },
    QUICK_REVISION: {
      label: 'Quick Revision',
      icon: Clock,
      desc: 'Summarizes key algorithmic invariants, formulas, and common traps.',
    },
    EXAM: {
      label: 'Exam Mode',
      icon: ShieldAlert,
      desc: 'Timed practice with strict answer-key withholding.',
    },
    EXAM_MODE: {
      label: 'Exam Mode',
      icon: ShieldAlert,
      desc: 'Timed practice with strict answer-key withholding.',
    },
  };

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-6">
      {/* Header & Diagnostics bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-slate-200 gap-3">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 tracking-tight flex items-center">
            <Sparkles className="w-6 h-6 mr-2 text-indigo-600" /> Socratic Placement AI Tutor
          </h1>
          <p className="text-xs text-slate-500 mt-0.5">
            Grounded in Qdrant curriculum vector store with multilingual synthesis
          </p>
        </div>

        {diagnostics && (
          <div className="flex items-center space-x-2 text-[11px] bg-slate-50 border border-slate-200 px-3 py-1.5 rounded-lg text-slate-600">
            <Cpu className="w-3.5 h-3.5 text-indigo-500 flex-shrink-0" />
            <span>
              LLM: <strong className="text-slate-800">{diagnostics.llm_provider.active_provider}</strong>
            </span>
            <span>•</span>
            <span>
              RAG: <strong className="text-slate-800">{diagnostics.embedding_provider.active_provider}</strong>
            </span>
          </div>
        )}
      </div>

      {/* Mode & Language Controls Bar */}
      <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm space-y-3">
        <div className="flex flex-wrap items-center justify-between gap-3">
          {/* Mode Pill Buttons */}
          <div className="flex flex-wrap gap-1.5">
            {(['TEACH_FROM_BASICS', 'HINT', 'DEBUG', 'INTERVIEW', 'QUICK_REVISION', 'EXAM'] as TutorMode[]).map(
              (m) => {
                const info = modeDescriptions[m];
                const Icon = info.icon;
                const active = mode === m;
                return (
                  <button
                    key={m}
                    onClick={() => setMode(m)}
                    className={`inline-flex items-center px-3 py-1.5 rounded-lg text-xs font-semibold transition border ${
                      active
                        ? 'bg-indigo-600 text-white border-indigo-600 shadow-sm'
                        : 'bg-white text-slate-700 border-slate-200 hover:bg-slate-50'
                    }`}
                  >
                    <Icon className="w-3.5 h-3.5 mr-1.5" />
                    {info.label}
                  </button>
                );
              }
            )}
          </div>

          {/* Language Selector */}
          <div className="flex items-center space-x-2">
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Language:</span>
            <select
              value={language}
              onChange={(e) => setLanguage(e.target.value as TutorLanguage)}
              className="px-2.5 py-1 rounded-lg border border-slate-200 bg-white text-xs font-semibold text-slate-800 focus:outline-none focus:ring-1 focus:ring-indigo-500"
            >
              <option value="ENGLISH">English</option>
              <option value="TANGLISH">Tanglish (Tamil + English)</option>
              <option value="TAMIL">Tamil (தமிழ்)</option>
            </select>
          </div>
        </div>

        {/* Exam Mode Safeguard Banner */}
        {(mode === 'EXAM' || mode === 'EXAM_MODE') && (
          <div className="p-3 bg-amber-50 border border-amber-200 text-amber-900 rounded-lg text-xs flex items-center space-x-2">
            <ShieldAlert className="w-4 h-4 text-amber-600 flex-shrink-0" />
            <span>
              <strong>Exam Mode Active:</strong> Under assessment rules, complete worked solutions and answer keys
              are restricted until you submit your attempt.
            </span>
          </div>
        )}
      </div>

      {error && <ErrorBanner message={error} />}

      {/* Chat Messages Container */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-sm flex flex-col h-[500px]">
        <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-4">
          {messages.length === 0 ? (
            <div className="h-full flex flex-col items-center justify-center text-center p-6 text-slate-400 space-y-3">
              <div className="w-12 h-12 bg-indigo-50 text-indigo-500 rounded-2xl flex items-center justify-center">
                <Sparkles className="w-6 h-6" />
              </div>
              <h3 className="text-sm font-semibold text-slate-700">How can I guide your preparation today?</h3>
              <p className="text-xs max-w-md leading-relaxed text-slate-500">
                Ask a concept question, request debugging guidance for an error, or simulate a technical
                placement interview in English, Tamil, or Tanglish.
              </p>
              <div className="flex flex-wrap gap-2 justify-center pt-2">
                {[
                  'Explain Two-Pointer technique from basics',
                  'Why does BST search degrade to O(N)?',
                  'What is the difference between LEFT JOIN and WHERE?',
                  'Two pointer while loop index out of bounds epdi fix panradhu?',
                ].map((prompt, i) => (
                  <button
                    key={i}
                    onClick={() => handleSendMessage(prompt)}
                    className="text-xs bg-slate-50 hover:bg-indigo-50 text-slate-600 hover:text-indigo-700 border border-slate-200 hover:border-indigo-200 px-3 py-1.5 rounded-full transition"
                  >
                    "{prompt}"
                  </button>
                ))}
              </div>
            </div>
          ) : (
            messages.map((msg) => (
              <div
                key={msg.id}
                className={`flex flex-col ${msg.role === 'user' ? 'items-end' : 'items-start'} space-y-1.5`}
              >
                <div
                  className={`max-w-[85%] rounded-2xl p-4 text-xs leading-relaxed ${
                    msg.role === 'user'
                      ? 'bg-indigo-600 text-white rounded-tr-none'
                      : 'bg-slate-50 text-slate-800 border border-slate-200 rounded-tl-none whitespace-pre-wrap'
                  }`}
                >
                  {msg.content}

                  {/* Citations Excerpt Drawer */}
                  {msg.citations && msg.citations.length > 0 && (
                    <div className="mt-3 pt-3 border-t border-slate-200/60 space-y-1.5">
                      <span className="text-[10px] font-bold text-slate-500 uppercase tracking-wider block">
                        Verified Sources ({msg.citations.length}):
                      </span>
                      {msg.citations.map((c, idx) => {
                        const citKey = `${msg.id}-${idx}`;
                        const isExpanded = expandedCitationIdx === citKey;
                        return (
                          <div key={idx} className="bg-white p-2 rounded border border-slate-200 text-[11px]">
                            <button
                              onClick={() => setExpandedCitationIdx(isExpanded ? null : citKey)}
                              className="w-full text-left font-semibold text-indigo-700 flex items-center justify-between"
                            >
                              <span className="truncate pr-2">{c.title}</span>
                              <span className="text-[10px] text-slate-400 flex items-center flex-shrink-0">
                                Rel: {(((c.relevance_score ?? 0)) * 100).toFixed(0)}%
                                {isExpanded ? (
                                  <ChevronUp className="w-3 h-3 ml-1" />
                                ) : (
                                  <ChevronDown className="w-3 h-3 ml-1" />
                                )}
                              </span>
                            </button>
                            {isExpanded && (
                              <p className="mt-1 text-slate-600 text-[10px] bg-slate-50 p-2 rounded border border-slate-100">
                                "{c.chunk_text}"
                              </p>
                            )}
                          </div>
                        );
                      })}
                    </div>
                  )}

                  {/* Follow-up Suggestion Chips */}
                  {msg.suggestions && msg.suggestions.length > 0 && (
                    <div className="mt-3 pt-2 flex flex-wrap gap-1.5">
                      {msg.suggestions.map((s, i) => (
                        <button
                          key={i}
                          onClick={() => handleSendMessage(s)}
                          className="text-[11px] bg-indigo-50 hover:bg-indigo-100 text-indigo-800 font-medium px-2.5 py-1 rounded-full transition"
                        >
                          {s} →
                        </button>
                      ))}
                    </div>
                  )}
                </div>

                <div className="text-[10px] text-slate-400 px-1 flex items-center space-x-2">
                  <span>{msg.timestamp}</span>
                  {msg.providerUsed && (
                    <>
                      <span>•</span>
                      <span>{msg.providerUsed}</span>
                    </>
                  )}
                </div>
              </div>
            ))
          )}

          {isLoading && (
            <div className="flex items-center space-x-2 text-xs text-slate-400 p-2">
              <div className="w-2 h-2 rounded-full bg-indigo-500 animate-bounce" />
              <div className="w-2 h-2 rounded-full bg-indigo-500 animate-bounce delay-100" />
              <div className="w-2 h-2 rounded-full bg-indigo-500 animate-bounce delay-200" />
              <span className="ml-1">Retrieving curriculum context & formulating guidance...</span>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Bar */}
        <div className="p-3 border-t border-slate-200 bg-slate-50/60 rounded-b-2xl">
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSendMessage();
            }}
            className="flex items-center space-x-2"
          >
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              placeholder={`Ask in ${language === 'TANGLISH' ? 'Tanglish' : language === 'TAMIL' ? 'Tamil' : 'English'} (${modeDescriptions[mode].label})...`}
              className="flex-1 px-4 py-2.5 border border-slate-200 rounded-xl text-xs bg-white text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-600 transition"
            />
            <button
              type="submit"
              disabled={isLoading || !inputMessage.trim()}
              className="p-2.5 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl transition shadow-sm disabled:opacity-40 disabled:cursor-not-allowed"
            >
              <Send className="w-4 h-4" />
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};
