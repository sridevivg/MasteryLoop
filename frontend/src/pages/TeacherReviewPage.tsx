import React, { useState, useEffect } from 'react';
import { itemsApi, DraftItemResponse } from '../api/items';
import { curriculumApi } from '../api/curriculum';
import { Domain, Skill } from '../types';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { ErrorBanner } from '../components/ErrorBanner';
import {
  ShieldCheck,
  CheckCircle,
  XCircle,
  AlertTriangle,
  Sparkles,
  Layers,
  HelpCircle,
  Filter,
  Check,
  X
} from 'lucide-react';

export const TeacherReviewPage: React.FC = () => {
  const [queue, setQueue] = useState<DraftItemResponse[]>([]);
  const [selectedItem, setSelectedItem] = useState<DraftItemResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [reviewNotes, setReviewNotes] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [actionSuccess, setActionSuccess] = useState<string | null>(null);

  // Question drafting modal state
  const [showDraftModal, setShowDraftModal] = useState(false);
  const [domains, setDomains] = useState<Domain[]>([]);
  const [draftSkillId, setDraftSkillId] = useState('');
  const [draftDifficulty, setDraftDifficulty] = useState<'easy' | 'medium' | 'hard'>('medium');
  const [isDrafting, setIsDrafting] = useState(false);

  const fetchQueue = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await itemsApi.getReviewQueue();
      setQueue(data);
      if (data.length > 0 && !selectedItem) {
        setSelectedItem(data[0]);
      }
    } catch (err: any) {
      setError(err.message || 'Failed to fetch items in review queue.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchQueue();
    const loadCurriculum = async () => {
      try {
        const doms = await curriculumApi.getDomains();
        setDomains(doms);
      } catch (err) {
        console.warn('Failed loading domains for drafting:', err);
      }
    };
    loadCurriculum();
  }, []);

  const handleReviewAction = async (action: 'APPROVE' | 'REJECT') => {
    if (!selectedItem) return;
    if (!reviewNotes.trim()) {
      setError('Please provide review notes justifying your decision.');
      return;
    }

    try {
      setIsSubmitting(true);
      setError(null);
      await itemsApi.reviewItem(selectedItem.id, {
        action,
        reason: reviewNotes.trim(),
      });

      setActionSuccess(`Item ${selectedItem.id.slice(0, 8)}... was successfully marked ${action}D.`);
      setReviewNotes('');
      // Refresh review queue
      const updatedQueue = await itemsApi.getReviewQueue();
      setQueue(updatedQueue);
      setSelectedItem(updatedQueue.length > 0 ? updatedQueue[0] : null);
    } catch (err: any) {
      setError(err.message || 'Error processing item review.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleGenerateDraft = async () => {
    if (!draftSkillId) {
      setError('Please provide a skill ID or code to ground the question.');
      return;
    }

    try {
      setIsDrafting(true);
      setError(null);
      const drafted = await itemsApi.generateDraft({
        skill_id: draftSkillId,
        difficulty_band: draftDifficulty,
        item_type: 'MCQ',
      });

      setShowDraftModal(false);
      setActionSuccess(`New item drafted and screened: ${drafted.id.slice(0, 8)}...`);
      fetchQueue();
    } catch (err: any) {
      setError(err.message || 'Error generating draft item.');
    } finally {
      setIsDrafting(false);
    }
  };

  if (loading) {
    return <LoadingSpinner message="Fetching items pending subject-matter expert review..." />;
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-6 border-b border-slate-200 gap-4">
        <div>
          <span className="text-xs font-bold text-amber-600 uppercase tracking-wider flex items-center">
            <ShieldCheck className="w-4 h-4 mr-1 text-amber-500" /> Human-in-the-Loop Quality Control
          </span>
          <h1 className="text-2xl font-bold text-slate-900 tracking-tight mt-1">
            Teacher Question Review Queue
          </h1>
          <p className="text-xs text-slate-500 mt-0.5">
            8-Stage Lifecycle: GENERATED → VALIDATING → HUMAN_REVIEW → APPROVED → PILOT → CALIBRATED
          </p>
        </div>

        <button
          onClick={() => setShowDraftModal(true)}
          className="inline-flex items-center px-4 py-2 bg-indigo-600 text-white rounded-lg text-xs font-semibold hover:bg-indigo-700 transition shadow-sm"
        >
          <Sparkles className="w-3.5 h-3.5 mr-1.5" /> Draft New Item (AI Grounded)
        </button>
      </div>

      {actionSuccess && (
        <div className="p-3 bg-emerald-50 border border-emerald-200 text-emerald-800 rounded-lg text-xs font-semibold flex items-center justify-between">
          <span>{actionSuccess}</span>
          <button onClick={() => setActionSuccess(null)} className="text-emerald-600 hover:text-emerald-800">
            <X className="w-4 h-4" />
          </button>
        </div>
      )}

      {error && <ErrorBanner message={error} />}

      {/* Main Review Layout */}
      {queue.length === 0 ? (
        <div className="bg-white rounded-2xl border border-slate-200 p-12 text-center max-w-xl mx-auto space-y-3">
          <div className="w-12 h-12 bg-emerald-50 text-emerald-600 rounded-2xl flex items-center justify-center mx-auto">
            <CheckCircle className="w-6 h-6" />
          </div>
          <h2 className="text-base font-bold text-slate-800">Review Queue is Clear</h2>
          <p className="text-xs text-slate-500 leading-relaxed">
            There are currently no AI-drafted items awaiting human SME validation. All active bank items have
            undergone psychometric screening and reviewer verification.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Queue List */}
          <div className="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm space-y-3">
            <div className="flex items-center justify-between pb-3 border-b border-slate-100">
              <span className="text-xs font-bold text-slate-700 uppercase tracking-wider">
                Pending Items ({queue.length})
              </span>
              <span className="text-[10px] bg-amber-100 text-amber-800 font-semibold px-2 py-0.5 rounded">
                HUMAN_REVIEW
              </span>
            </div>

            <div className="space-y-2 max-h-[550px] overflow-y-auto">
              {queue.map((item) => {
                const isSelected = selectedItem?.id === item.id;
                return (
                  <button
                    key={item.id}
                    onClick={() => {
                      setSelectedItem(item);
                      setActionSuccess(null);
                    }}
                    className={`w-full text-left p-3 rounded-xl border transition text-xs space-y-1 ${
                      isSelected
                        ? 'bg-indigo-50/70 border-indigo-400 text-indigo-950 font-medium'
                        : 'bg-white border-slate-200 hover:bg-slate-50 text-slate-700'
                    }`}
                  >
                    <div className="flex items-center justify-between text-[10px] text-slate-400">
                      <span>ID: {item.id.slice(0, 10)}...</span>
                      <span>b = {item.b.toFixed(2)}</span>
                    </div>
                    <div className="line-clamp-2 text-slate-800 font-medium">{item.stem}</div>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Item Inspector & Decision Panel */}
          {selectedItem && (
            <div className="lg:col-span-2 bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-6">
              {/* Question Meta */}
              <div className="flex items-center justify-between pb-4 border-b border-slate-100">
                <div>
                  <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">
                    Origin: {selectedItem.origin} • Item ID: {selectedItem.id}
                  </span>
                  <div className="flex items-center space-x-2 mt-1">
                    <span className="text-xs font-bold text-amber-700 bg-amber-50 px-2 py-0.5 rounded border border-amber-200">
                      State: {selectedItem.state}
                    </span>
                    <span className="text-xs font-semibold text-slate-600 bg-slate-100 px-2 py-0.5 rounded">
                      Provisional b: {selectedItem.b.toFixed(2)} (Difficulty)
                    </span>
                    <span className="text-xs font-semibold text-slate-600 bg-slate-100 px-2 py-0.5 rounded">
                      Provisional a: {selectedItem.a.toFixed(2)} (Discrimination)
                    </span>
                  </div>
                </div>
              </div>

              {/* Automated Screening Check Badges */}
              {selectedItem.lineage?.screening_checks && (
                <div className="p-3 bg-slate-50 rounded-xl border border-slate-200 text-xs space-y-1">
                  <span className="font-bold text-slate-700 block text-[11px] mb-1">
                    Automated Pre-Screening Pass Report:
                  </span>
                  <div className="flex flex-wrap gap-2">
                    <span className="inline-flex items-center text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded text-[11px] font-semibold border border-emerald-200">
                      <Check className="w-3 h-3 mr-1" /> Schema Validated
                    </span>
                    <span className="inline-flex items-center text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded text-[11px] font-semibold border border-emerald-200">
                      <Check className="w-3 h-3 mr-1" /> Distractors Verified
                    </span>
                    <span className="inline-flex items-center text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded text-[11px] font-semibold border border-emerald-200">
                      <Check className="w-3 h-3 mr-1" /> Blind Solver Sanity Check
                    </span>
                  </div>
                </div>
              )}

              {/* Question Stem */}
              <div>
                <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Question Stem:</h3>
                <p className="text-sm font-semibold text-slate-900 bg-slate-50 p-4 rounded-xl border border-slate-200 whitespace-pre-wrap">
                  {selectedItem.stem}
                </p>
              </div>

              {/* Options & Distractors */}
              <div>
                <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">
                  Options & Distractor Diagnostic Feedback:
                </h3>
                <div className="space-y-2">
                  {selectedItem.options.map((opt) => {
                    const isCorrect = !opt.is_distractor;
                    return (
                      <div
                        key={opt.id}
                        className={`p-3 rounded-xl border text-xs flex items-start space-x-3 ${
                          isCorrect
                            ? 'bg-emerald-50/70 border-emerald-300 text-emerald-950 font-medium'
                            : 'bg-white border-slate-200 text-slate-800'
                        }`}
                      >
                        <span
                          className={`w-5 h-5 rounded-full flex items-center justify-center text-[10px] font-bold flex-shrink-0 mt-0.5 ${
                            isCorrect ? 'bg-emerald-600 text-white' : 'bg-slate-100 text-slate-600'
                          }`}
                        >
                          {opt.id}
                        </span>
                        <div className="flex-1">
                          <p className="leading-snug">{opt.text}</p>
                          {isCorrect && (
                            <span className="text-[10px] font-bold text-emerald-700 uppercase tracking-wider mt-1 block">
                              ★ Correct Answer
                            </span>
                          )}
                          {selectedItem.distractor_explanations?.[opt.id] && (
                            <p className="text-[10px] text-slate-500 mt-1 italic">
                              Distractor Analysis: {selectedItem.distractor_explanations[opt.id]}
                            </p>
                          )}
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* Solution Explanation */}
              {selectedItem.explanation && (
                <div>
                  <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-1">
                    Pedagogical Solution Derivation:
                  </h3>
                  <p className="text-xs text-slate-700 bg-slate-50 p-3 rounded-lg border border-slate-100 leading-relaxed">
                    {selectedItem.explanation}
                  </p>
                </div>
              )}

              {/* Reviewer Action Form */}
              <div className="pt-4 border-t border-slate-200 space-y-3">
                <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider">
                  Reviewer Audit Notes:
                </label>
                <textarea
                  value={reviewNotes}
                  onChange={(e) => setReviewNotes(e.target.value)}
                  placeholder="Enter audit notes (e.g. 'Distractors verified against syllabus. Complexity trade-offs sound.')..."
                  className="w-full px-3 py-2 text-xs border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-600"
                  rows={3}
                />

                <div className="flex items-center justify-end space-x-3 pt-2">
                  <button
                    onClick={() => handleReviewAction('REJECT')}
                    disabled={isSubmitting}
                    className="inline-flex items-center px-4 py-2 border border-rose-200 bg-rose-50 text-rose-700 text-xs font-semibold rounded-lg hover:bg-rose-100 transition disabled:opacity-50"
                  >
                    <XCircle className="w-3.5 h-3.5 mr-1.5" /> Reject Item
                  </button>
                  <button
                    onClick={() => handleReviewAction('APPROVE')}
                    disabled={isSubmitting}
                    className="inline-flex items-center px-5 py-2 bg-emerald-600 text-white text-xs font-semibold rounded-lg hover:bg-emerald-700 transition shadow-sm disabled:opacity-50"
                  >
                    <CheckCircle className="w-3.5 h-3.5 mr-1.5" /> Approve for Pilot Calibration
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Question Drafting Modal */}
      {showDraftModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/40 p-4">
          <div className="bg-white rounded-2xl max-w-md w-full p-6 space-y-4 shadow-xl border border-slate-200">
            <div className="flex justify-between items-center pb-3 border-b border-slate-100">
              <h2 className="text-base font-bold text-slate-900 flex items-center">
                <Sparkles className="w-4 h-4 mr-2 text-indigo-600" /> Draft AI Grounded Question
              </h2>
              <button
                onClick={() => setShowDraftModal(false)}
                className="text-slate-400 hover:text-slate-600 p-1"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <p className="text-xs text-slate-500 leading-relaxed">
              Items are generated strictly using retrieved curriculum chunks and must pass automated schema,
              distractor, and blind solver screening before entering the human review queue.
            </p>

            <div className="space-y-3">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Target Skill Code</label>
                <input
                  type="text"
                  value={draftSkillId}
                  onChange={(e) => setDraftSkillId(e.target.value)}
                  placeholder="e.g. DSA_BST or SQL_JOINS"
                  className="w-full px-3 py-2 text-xs border border-slate-200 rounded-lg focus:outline-none focus:ring-1 focus:ring-indigo-500"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Target Difficulty Band</label>
                <select
                  value={draftDifficulty}
                  onChange={(e) => setDraftDifficulty(e.target.value as any)}
                  className="w-full px-3 py-2 text-xs border border-slate-200 rounded-lg bg-white text-slate-800"
                >
                  <option value="easy">Easy (b: -1.5 to -0.5)</option>
                  <option value="medium">Medium (b: -0.5 to +0.5)</option>
                  <option value="hard">Hard (b: +0.5 to +1.8)</option>
                </select>
              </div>
            </div>

            <div className="flex justify-end space-x-2 pt-3 border-t border-slate-100">
              <button
                onClick={() => setShowDraftModal(false)}
                className="px-3 py-1.5 text-xs text-slate-600 hover:bg-slate-100 rounded-lg"
              >
                Cancel
              </button>
              <button
                onClick={handleGenerateDraft}
                disabled={isDrafting}
                className="px-4 py-1.5 text-xs font-semibold text-white bg-indigo-600 hover:bg-indigo-700 rounded-lg transition shadow-sm disabled:opacity-50"
              >
                {isDrafting ? 'Drafting & Screening...' : 'Draft Item'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
