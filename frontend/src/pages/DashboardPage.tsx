import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { masteryApi, DashboardResponse, DueReviewsResponse } from '../api/mastery';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { ErrorBanner } from '../components/ErrorBanner';
import {
  Award,
  TrendingUp,
  Target,
  Sparkles,
  ArrowRight,
  BookOpen,
  CheckCircle,
  AlertTriangle,
  History,
  Zap,
  Play,
  Brain,
  Clock,
  RotateCcw,
  Check,
  X
} from 'lucide-react';
import {
  ResponsiveContainer,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip
} from 'recharts';

export const DashboardPage: React.FC = () => {
  const [data, setData] = useState<DashboardResponse | null>(null);
  const [dueReviews, setDueReviews] = useState<DueReviewsResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [reviewingId, setReviewingId] = useState<string | null>(null);
  const [reviewFeedback, setReviewFeedback] = useState<string | null>(null);

  const fetchDashboard = async () => {
    try {
      setLoading(true);
      setError(null);
      const [dashRes, dueRes] = await Promise.all([
        masteryApi.getDashboard(),
        masteryApi.getDueReviews().catch(() => null)
      ]);
      setData(dashRes);
      setDueReviews(dueRes);
    } catch (err: any) {
      setError(err.message || 'Could not load learner dashboard data.');
    } finally {
      setLoading(false);
    }
  };

  const handleReviewSkill = async (skillId: string, isCorrect: boolean) => {
    try {
      setReviewingId(skillId);
      const res = await masteryApi.recordReview(skillId, isCorrect);
      setReviewFeedback(
        isCorrect
          ? `Retention reinforced for ${res.skill_name}! Next review scheduled.`
          : `Review recorded for ${res.skill_name}. Memory decay accelerated for earlier practice.`
      );
      const [dashRes, dueRes] = await Promise.all([
        masteryApi.getDashboard(),
        masteryApi.getDueReviews().catch(() => null)
      ]);
      setData(dashRes);
      setDueReviews(dueRes);
    } catch (err: any) {
      setReviewFeedback(`Failed to update review: ${err.message || 'Server error'}`);
    } finally {
      setReviewingId(null);
      setTimeout(() => setReviewFeedback(null), 5000);
    }
  };

  useEffect(() => {
    fetchDashboard();
  }, []);

  if (loading) {
    return <LoadingSpinner message="Calibrating cognitive mastery profile..." />;
  }

  if (error) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-8">
        <ErrorBanner message={error} onRetry={fetchDashboard} />
      </div>
    );
  }

  if (!data) return null;

  const isNewLearner = data.total_assessments_taken === 0 && data.overall_mastery === 0;

  // Prepare radar data for domains
  const radarData = data.placement_domains.map((d) => ({
    domain: d.domain_name.replace(' & ', '\n').split(' ')[0],
    readiness: d.readiness_percentage,
    fullName: d.domain_name,
  }));

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Top Banner / Welcome */}
      <div className="flex flex-col md:flex-row md:items-center justify-between pb-6 border-b border-slate-200 gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 tracking-tight">Placement Mastery Dashboard</h1>
          <p className="text-sm text-slate-500 mt-1">
            Real-time Bayesian Knowledge Tracing across 11 Placement Domains
          </p>
        </div>
        <div className="flex items-center space-x-3">
          <Link
            to="/assessment"
            className="inline-flex items-center px-4 py-2 rounded-lg bg-indigo-600 text-white text-sm font-semibold hover:bg-indigo-700 transition shadow-sm"
          >
            <Play className="w-4 h-4 mr-1.5" /> Start Adaptive Test
          </Link>
          <Link
            to="/tutor"
            className="inline-flex items-center px-4 py-2 rounded-lg bg-white border border-slate-200 text-slate-700 text-sm font-semibold hover:bg-slate-50 transition"
          >
            <Sparkles className="w-4 h-4 mr-1.5 text-indigo-500" /> Socratic AI Tutor
          </Link>
        </div>
      </div>

      {/* Empty State for New Learners */}
      {isNewLearner && (
        <div className="bg-indigo-50/70 border border-indigo-100 rounded-2xl p-8 text-center max-w-3xl mx-auto">
          <div className="w-14 h-14 bg-indigo-100 text-indigo-700 rounded-2xl flex items-center justify-center mx-auto mb-4">
            <Target className="w-8 h-8" />
          </div>
          <h2 className="text-xl font-bold text-slate-900">No Assessment History Found</h2>
          <p className="text-slate-600 text-sm mt-2 max-w-xl mx-auto leading-relaxed">
            Welcome to MasteryLoop! We don't fabricate learner statistics. Complete your first diagnostic
            assessment to calibrate your initial IRT ability parameter ($\theta$) and generate personalized
            mastery graphs.
          </p>
          <div className="mt-6">
            <Link
              to="/assessment"
              className="inline-flex items-center px-5 py-2.5 rounded-lg bg-indigo-600 text-white font-semibold text-sm hover:bg-indigo-700 transition shadow-sm"
            >
              Start Diagnostic Assessment <ArrowRight className="w-4 h-4 ml-1.5" />
            </Link>
          </div>
        </div>
      )}

      {/* Summary KPI Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between text-slate-500 text-xs font-semibold uppercase tracking-wider">
            <span>Overall Mastery</span>
            <Award className="w-4 h-4 text-indigo-500" />
          </div>
          <div className="mt-2 flex items-baseline space-x-2">
            <span className="text-3xl font-bold text-slate-900">{data.overall_mastery}%</span>
            <span className="text-xs text-slate-500">BKT Posterior</span>
          </div>
          <div className="w-full bg-slate-100 rounded-full h-1.5 mt-3 overflow-hidden">
            <div
              className="bg-indigo-600 h-1.5 rounded-full transition-all duration-500"
              style={{ width: `${Math.min(data.overall_mastery, 100)}%` }}
            />
          </div>
        </div>

        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between text-slate-500 text-xs font-semibold uppercase tracking-wider">
            <span>Placement Readiness</span>
            <TrendingUp className="w-4 h-4 text-emerald-500" />
          </div>
          <div className="mt-2 flex items-baseline space-x-2">
            <span className="text-3xl font-bold text-slate-900">{data.placement_readiness}%</span>
            <span className="text-xs text-slate-500">Benchmark Goal</span>
          </div>
          <div className="w-full bg-slate-100 rounded-full h-1.5 mt-3 overflow-hidden">
            <div
              className="bg-emerald-500 h-1.5 rounded-full transition-all duration-500"
              style={{ width: `${Math.min(data.placement_readiness, 100)}%` }}
            />
          </div>
        </div>

        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between text-slate-500 text-xs font-semibold uppercase tracking-wider">
            <span>Assessments Taken</span>
            <CheckCircle className="w-4 h-4 text-blue-500" />
          </div>
          <div className="mt-2 flex items-baseline space-x-2">
            <span className="text-3xl font-bold text-slate-900">{data.total_assessments_taken}</span>
            <span className="text-xs text-slate-500">Sessions</span>
          </div>
          <p className="text-xs text-slate-400 mt-3">{data.total_questions_solved} total questions analyzed</p>
        </div>

        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between text-slate-500 text-xs font-semibold uppercase tracking-wider">
            <span>Study Streak</span>
            <Zap className="w-4 h-4 text-amber-500" />
          </div>
          <div className="mt-2 flex items-baseline space-x-2">
            <span className="text-3xl font-bold text-slate-900">{data.study_streak_days}</span>
            <span className="text-xs text-slate-500">Consecutive Days</span>
          </div>
          <p className="text-xs text-slate-400 mt-3">
            {data.retention_due_count > 0
              ? `${data.retention_due_count} skills due for spaced review`
              : 'Memory retention on schedule'}
          </p>
        </div>
      </div>

      {/* Main Grid: Domain Readiness & Next-Best Actions */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Placement Domains Radar / Breakdown */}
        <div className="lg:col-span-2 bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-6">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-lg font-bold text-slate-900">Domain-Level Readiness Radar</h2>
              <p className="text-xs text-slate-500">Cognitive coverage across engineering, quantitative & placement topics</p>
            </div>
            <Link to="/curriculum" className="text-xs font-semibold text-indigo-600 hover:text-indigo-700">
              View All 11 Domains →
            </Link>
          </div>

          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart data={radarData}>
                <PolarGrid stroke="#e2e8f0" />
                <PolarAngleAxis dataKey="domain" tick={{ fill: '#64748b', fontSize: 11 }} />
                <PolarRadiusAxis angle={30} domain={[0, 100]} stroke="#cbd5e1" />
                <Radar
                  name="Mastery %"
                  dataKey="readiness"
                  stroke="#6366f1"
                  fill="#6366f1"
                  fillOpacity={0.25}
                />
                <Tooltip
                  formatter={(val: any) => [`${val}%`, 'Readiness']}
                  labelFormatter={(idx: any) => radarData[idx]?.fullName || idx}
                />
              </RadarChart>
            </ResponsiveContainer>
          </div>

          {/* Domain Readiness Bars */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-4 border-t border-slate-100">
            {data.placement_domains.slice(0, 6).map((d) => (
              <div key={d.domain_id} className="p-3 bg-slate-50 rounded-lg border border-slate-100 text-xs">
                <div className="flex justify-between font-medium text-slate-700 mb-1">
                  <span className="truncate pr-2">{d.domain_name}</span>
                  <span className="font-semibold text-slate-900">{d.readiness_percentage}%</span>
                </div>
                <div className="w-full bg-slate-200 rounded-full h-1 overflow-hidden">
                  <div
                    className={`h-1 rounded-full ${
                      d.readiness_percentage >= 70
                        ? 'bg-emerald-500'
                        : d.readiness_percentage >= 40
                        ? 'bg-amber-500'
                        : 'bg-indigo-400'
                    }`}
                    style={{ width: `${d.readiness_percentage}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Prioritized 3 Next-Best Actions */}
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm flex flex-col justify-between">
          <div>
            <div className="flex items-center space-x-2 text-indigo-600 font-bold text-xs uppercase tracking-wider mb-2">
              <Sparkles className="w-4 h-4" />
              <span>Prioritized Actions</span>
            </div>
            <h2 className="text-lg font-bold text-slate-900">Next-Best Actions</h2>
            <p className="text-xs text-slate-500 mt-1 mb-4">
              Exactly 3 actions computed from prerequisite graph & BKT gaps
            </p>

            <div className="space-y-3">
              {data.next_best_actions && data.next_best_actions.length > 0 ? (
                data.next_best_actions.slice(0, 3).map((action, i) => (
                  <div
                    key={i}
                    className="p-3.5 rounded-xl border border-slate-200 hover:border-indigo-300 hover:bg-indigo-50/20 transition group"
                  >
                    <div className="flex items-center justify-between mb-1">
                      <span
                        className={`text-[10px] font-bold px-2 py-0.5 rounded tracking-wide uppercase ${
                          action.category === 'LEARN'
                            ? 'bg-blue-100 text-blue-800'
                            : action.category === 'PRACTICE'
                            ? 'bg-emerald-100 text-emerald-800'
                            : 'bg-purple-100 text-purple-800'
                        }`}
                      >
                        {action.category}
                      </span>
                      <span className="text-[11px] text-slate-400">{action.duration_minutes} mins</span>
                    </div>
                    <h3 className="text-sm font-semibold text-slate-800 group-hover:text-indigo-600 transition">
                      {action.title}
                    </h3>
                    <p className="text-xs text-slate-500 mt-1 leading-snug">{action.rationale}</p>
                    <div className="mt-2.5 pt-2 border-t border-slate-100 flex items-center justify-between">
                      <span className="text-[10px] text-slate-400 font-medium">{action.domain_name}</span>
                      <Link
                        to={action.category === 'LEARN' ? '/tutor' : '/assessment'}
                        className="text-xs font-semibold text-indigo-600 hover:text-indigo-700 inline-flex items-center"
                      >
                        Start <ArrowRight className="w-3 h-3 ml-1" />
                      </Link>
                    </div>
                  </div>
                ))
              ) : (
                <div className="p-4 bg-slate-50 rounded-xl text-center text-xs text-slate-500">
                  Take a diagnostic test to generate your personalized next-best actions.
                </div>
              )}
            </div>
          </div>

          {/* Daily Challenge card (if present) */}
          {data.today_challenge && (
            <div className="mt-6 pt-4 border-t border-slate-200">
              <div className="p-3.5 bg-amber-50/70 border border-amber-200 rounded-xl text-xs">
                <div className="flex items-center space-x-1.5 text-amber-800 font-bold mb-1">
                  <Zap className="w-3.5 h-3.5 text-amber-600" />
                  <span>Today's Challenge (+{data.today_challenge.xp_reward} XP)</span>
                </div>
                <p className="font-semibold text-slate-800">{data.today_challenge.title}</p>
                <p className="text-slate-600 mt-0.5">{data.today_challenge.description}</p>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Spaced Repetition & Due Reviews (Ebbinghaus Decay Engine) */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
          <div className="flex items-center space-x-3">
            <div className="p-2.5 bg-indigo-50 text-indigo-600 rounded-xl">
              <Brain className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <h2 className="text-lg font-bold text-slate-900">Ebbinghaus Spaced Repetition & Due Reviews</h2>
                {dueReviews && dueReviews.due_count > 0 ? (
                  <span className="px-2 py-0.5 rounded-full text-xs font-semibold bg-rose-100 text-rose-700 animate-pulse">
                    {dueReviews.due_count} Due Now
                  </span>
                ) : (
                  <span className="px-2 py-0.5 rounded-full text-xs font-medium bg-emerald-100 text-emerald-700">
                    Retention Optimal
                  </span>
                )}
              </div>
              <p className="text-xs text-slate-500 mt-0.5">
                Dynamic decay model: R(t) = e^(-t/S). Cognitive stability scales with repeated active recall.
              </p>
            </div>
          </div>
          <Link
            to="/tutor"
            className="inline-flex items-center text-xs font-semibold text-indigo-600 hover:text-indigo-700"
          >
            Review with Socratic Tutor →
          </Link>
        </div>

        {reviewFeedback && (
          <div className="p-3 bg-indigo-50 border border-indigo-200 rounded-xl text-xs text-indigo-900 font-medium flex items-center justify-between">
            <span>{reviewFeedback}</span>
            <button onClick={() => setReviewFeedback(null)} className="text-indigo-500 hover:text-indigo-700">✕</button>
          </div>
        )}

        {dueReviews && dueReviews.due_skills.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 pt-2">
            {dueReviews.due_skills.map((item: any) => {
              const retention = (item.current_retention ?? item.retention_estimate ?? 0);
              const daysOverdue = item.days_overdue ?? 0;
              const forgettingRisk = item.forgetting_risk ?? (1 - retention);
              return (
                <div
                  key={item.skill_id}
                  className="p-4 rounded-xl border border-slate-200 bg-slate-50/50 hover:bg-white hover:border-indigo-200 transition space-y-3"
                >
                  <div className="flex items-start justify-between">
                    <div>
                      <h3 className="text-sm font-bold text-slate-800 line-clamp-1">{item.skill_name}</h3>
                      <p className="text-[11px] text-slate-500">{item.domain_name} • {item.topic_name}</p>
                    </div>
                    <span className={`px-2 py-0.5 rounded text-[10px] font-semibold ${
                      item.is_overdue ? 'bg-rose-100 text-rose-700' : 'bg-amber-100 text-amber-700'
                    }`}>
                      {item.is_overdue ? `${Number(daysOverdue).toFixed(1)}d Overdue` : 'Due Today'}
                    </span>
                  </div>

                  {/* Retention Bar */}
                  <div>
                    <div className="flex justify-between text-[11px] mb-1">
                      <span className="text-slate-500">Estimated Recall:</span>
                      <span className="font-semibold text-slate-700">{(retention * 100).toFixed(0)}%</span>
                    </div>
                    <div className="w-full bg-slate-200 rounded-full h-1.5 overflow-hidden">
                      <div
                        className={`h-1.5 rounded-full ${
                          retention >= 0.6 ? 'bg-amber-500' : 'bg-rose-500'
                        }`}
                        style={{ width: `${Math.min(retention * 100, 100)}%` }}
                      />
                    </div>
                    <div className="flex justify-between text-[10px] text-slate-400 mt-1">
                      <span>Forgetting Risk: {(forgettingRisk * 100).toFixed(0)}%</span>
                      <span>Reviewed: {item.interaction_count ?? 1}x</span>
                    </div>
                  </div>

                  {/* Quick Review Buttons */}
                  <div className="pt-2 border-t border-slate-100 flex items-center justify-between gap-2">
                    <span className="text-[10px] text-slate-500 font-medium">Quick Recall:</span>
                    <div className="flex items-center space-x-1.5">
                      <button
                        onClick={() => handleReviewSkill(item.skill_id, true)}
                        disabled={reviewingId === item.skill_id}
                        title="I remembered this concept accurately"
                        className="px-2.5 py-1 rounded bg-emerald-50 hover:bg-emerald-100 text-emerald-700 text-xs font-semibold flex items-center transition disabled:opacity-50"
                      >
                        <Check className="w-3 h-3 mr-1" /> Remembered
                      </button>
                      <button
                        onClick={() => handleReviewSkill(item.skill_id, false)}
                        disabled={reviewingId === item.skill_id}
                        title="I forgot or struggled with this concept"
                        className="px-2.5 py-1 rounded bg-rose-50 hover:bg-rose-100 text-rose-700 text-xs font-semibold flex items-center transition disabled:opacity-50"
                      >
                        <X className="w-3 h-3 mr-1" /> Forgot
                      </button>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        ) : (
          <div className="p-4 bg-emerald-50/50 border border-emerald-100 rounded-xl text-center text-xs text-emerald-800 flex items-center justify-center space-x-2">
            <CheckCircle className="w-4 h-4 text-emerald-600" />
            <span>
              All retention intervals are currently optimal! Memory stability indicates high recall retention. Reviews are scheduled automatically as forgetting risk increases.
            </span>
          </div>
        )}
      </div>

      {/* Strong vs Weak Skills & Recent Assessment History */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Strengths & Gaps */}
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
          <h2 className="text-lg font-bold text-slate-900">Identified Cognitive Gaps & Strengths</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div className="p-4 bg-rose-50/60 rounded-xl border border-rose-100">
              <div className="flex items-center space-x-2 text-rose-700 font-semibold text-xs mb-2">
                <AlertTriangle className="w-4 h-4 text-rose-500" />
                <span>Priority Learning Gaps</span>
              </div>
              {data.weak_topics && data.weak_topics.length > 0 ? (
                <ul className="space-y-2">
                  {data.weak_topics.slice(0, 4).map((w: any, i) => {
                    const topicName = w.topic_name || w.name || 'Core Topic';
                    const domainName = w.domain_name || w.domain || 'Placement';
                    const mastery = w.mastery_percentage !== undefined ? w.mastery_percentage : ((w.mastery ?? 0) * 100);
                    return (
                      <li key={i} className="text-xs">
                        <div className="font-medium text-slate-800">{topicName}</div>
                        <div className="text-slate-500 text-[10px]">{domainName} • {Number(mastery).toFixed(0)}% mastery</div>
                      </li>
                    );
                  })}
                </ul>
              ) : (
                <p className="text-xs text-slate-400">No critical cognitive gaps detected yet.</p>
              )}
            </div>

            <div className="p-4 bg-emerald-50/60 rounded-xl border border-emerald-100">
              <div className="flex items-center space-x-2 text-emerald-700 font-semibold text-xs mb-2">
                <CheckCircle className="w-4 h-4 text-emerald-500" />
                <span>Confirmed Mastered Skills</span>
              </div>
              {data.strong_topics && data.strong_topics.length > 0 ? (
                <ul className="space-y-2">
                  {data.strong_topics.slice(0, 4).map((s: any, i) => {
                    const topicName = s.topic_name || s.name || 'Core Topic';
                    const domainName = s.domain_name || s.domain || 'Placement';
                    const mastery = s.mastery_percentage !== undefined ? s.mastery_percentage : ((s.mastery ?? 0) * 100);
                    return (
                      <li key={i} className="text-xs">
                        <div className="font-medium text-slate-800">{topicName}</div>
                        <div className="text-slate-500 text-[10px]">{domainName} • {Number(mastery).toFixed(0)}% mastery</div>
                      </li>
                    );
                  })}
                </ul>
              ) : (
                <p className="text-xs text-slate-400">Complete assessments to certify mastered skills.</p>
              )}
            </div>
          </div>
        </div>

        {/* Assessment History */}
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-bold text-slate-900">Recent Assessment History</h2>
            <History className="w-4 h-4 text-slate-400" />
          </div>

          {data.recent_assessments && data.recent_assessments.length > 0 ? (
            <div className="divide-y divide-slate-100 text-xs">
              {data.recent_assessments.slice(0, 5).map((session: any, i) => {
                const accuracy = session.score !== undefined ? session.score : (session.accuracy_percentage !== undefined ? Math.round(session.accuracy_percentage) : 0);
                const theta = session.theta !== undefined ? Number(session.theta).toFixed(2) : '0.00';
                const dateStr = session.completed_at ? new Date(session.completed_at).toLocaleDateString() : (session.date || 'Recent');
                return (
                  <div key={i} className="py-2.5 flex items-center justify-between">
                    <div>
                      <span className="font-semibold text-slate-800">{session.domain_name || 'General Assessment'}</span>
                      <span className="text-slate-400 block text-[10px]">
                        {dateStr}
                      </span>
                    </div>
                    <div className="text-right">
                      <span className="font-bold text-indigo-600">{accuracy}% Accuracy</span>
                      <span className="text-slate-500 block text-[10px]">θ = {theta}</span>
                    </div>
                  </div>
                );
              })}
            </div>
          ) : (
            <p className="text-xs text-slate-500 py-6 text-center">
              No previous assessment sessions recorded.
            </p>
          )}
        </div>
      </div>

    </div>
  );
};
