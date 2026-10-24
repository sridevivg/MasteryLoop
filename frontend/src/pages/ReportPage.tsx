import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { sessionsApi } from '../api/sessions';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { ErrorBanner } from '../components/ErrorBanner';
import {
  Award,
  CheckCircle,
  TrendingUp,
  AlertCircle,
  Sparkles,
  ArrowRight,
  BookOpen,
  Home
} from 'lucide-react';

export const ReportPage: React.FC = () => {
  const { sessionId } = useParams<{ sessionId: string }>();
  const [report, setReport] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchReport = async () => {
      if (!sessionId) return;
      try {
        setLoading(true);
        setError(null);
        const data = await sessionsApi.getSessionReport(sessionId);
        setReport(data);
      } catch (err: any) {
        setError(err.message || 'Failed to load assessment report.');
      } finally {
        setLoading(false);
      }
    };
    fetchReport();
  }, [sessionId]);

  if (loading) {
    return <LoadingSpinner message="Calculating psychometric 2PL calibration & skill gaps..." />;
  }

  if (error) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-8">
        <ErrorBanner message={error} />
      </div>
    );
  }

  if (!report) return null;

  const scoreInfo = report.overall_score || {};
  const psycho = report.psychometrics || {};
  const skills = report.skill_evaluations || [];
  const nextActions = report.next_best_actions || [];

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-8">
      {/* Header */}
      <div className="pb-6 border-b border-slate-200 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <span className="text-xs font-bold text-indigo-600 uppercase tracking-wider">
            Diagnostic Certification Report
          </span>
          <h1 className="text-2xl font-bold text-slate-900 tracking-tight mt-1">
            {report.domain_name || 'Adaptive Assessment'} Results
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Session ID: {report.session_id} • Completed {new Date().toLocaleDateString()}
          </p>
        </div>
        <div className="flex items-center space-x-3">
          <Link
            to="/"
            className="inline-flex items-center px-4 py-2 border border-slate-200 text-slate-700 text-xs font-semibold rounded-lg hover:bg-slate-50 transition"
          >
            <Home className="w-3.5 h-3.5 mr-1.5" /> Dashboard
          </Link>
          <Link
            to="/tutor"
            className="inline-flex items-center px-4 py-2 bg-indigo-600 text-white text-xs font-semibold rounded-lg hover:bg-indigo-700 transition shadow-sm"
          >
            <Sparkles className="w-3.5 h-3.5 mr-1.5" /> Review with Tutor
          </Link>
        </div>
      </div>

      {/* Primary KPI Grid: Score vs Psychometrics */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
            Raw Measured Accuracy
          </span>
          <div className="mt-2 flex items-baseline space-x-2">
            <span className="text-3xl font-bold text-slate-900">
              {scoreInfo.accuracy_percentage ?? 0}%
            </span>
            <span className="text-xs text-slate-400">
              ({scoreInfo.correct_count} / {scoreInfo.total_questions})
            </span>
          </div>
          <p className="text-[11px] text-slate-500 mt-2">
            Deterministic proportion of items answered correctly.
          </p>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
            Calibrated Ability ($\hat\theta$)
          </span>
          <div className="mt-2 flex items-baseline space-x-2">
            <span className="text-3xl font-bold text-indigo-600">
              {psycho.theta !== undefined ? Number(psycho.theta).toFixed(2) : '0.00'}
            </span>
            <span className="text-xs text-slate-400">
              SE: ±{psycho.standard_error ? Number(psycho.standard_error).toFixed(2) : '0.30'}
            </span>
          </div>
          <p className="text-[11px] text-slate-500 mt-2">
            IRT 2PL latent placement readiness trait.
          </p>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm">
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
            Placement Performance Band
          </span>
          <div className="mt-2">
            <span className="inline-block text-lg font-bold text-emerald-700 bg-emerald-50 px-2.5 py-1 rounded-lg border border-emerald-200">
              {psycho.ability_band || 'Developing Candidate'}
            </span>
          </div>
          <p className="text-[11px] text-slate-500 mt-2">
            Standard benchmark relative to engineering cohorts.
          </p>
        </div>
      </div>

      {/* Skill-Level Breakdown */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
        <h2 className="text-base font-bold text-slate-900">Evaluated Skills & BKT Posteriors</h2>
        <div className="divide-y divide-slate-100 text-xs">
          {skills.map((s: any, idx: number) => {
            const mastery = s.mastery_estimate ?? s.estimate ?? 0.5;
            const isMastered = mastery >= 0.70;
            return (
              <div key={idx} className="py-3 flex items-center justify-between">
                <div>
                  <div className="font-semibold text-slate-800">{s.skill_name || s.name}</div>
                  <div className="text-slate-400 text-[11px]">
                    Code: {s.skill_code || 'SKILL'} • {s.correct_count ?? 1} / {s.total_count ?? 1} correct
                  </div>
                </div>
                <div className="text-right flex items-center space-x-3">
                  <div>
                    <span className="font-bold text-slate-800">{(mastery * 100).toFixed(0)}%</span>
                    <span className="text-slate-400 block text-[10px]">Mastery</span>
                  </div>
                  <span
                    className={`px-2 py-0.5 rounded text-[10px] font-bold tracking-wide uppercase ${
                      isMastered ? 'bg-emerald-100 text-emerald-800' : 'bg-rose-100 text-rose-800'
                    }`}
                  >
                    {isMastered ? 'Mastered' : 'Needs Focus'}
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Prioritized 3 Next-Best Actions */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
        <div className="flex items-center space-x-2 text-indigo-600 font-bold text-xs uppercase tracking-wider">
          <Sparkles className="w-4 h-4" />
          <span>Cognitive Prescription</span>
        </div>
        <h2 className="text-base font-bold text-slate-900">Targeted Next-Best Actions</h2>
        <p className="text-xs text-slate-500">
          Generated automatically to address isolated foundational learning gaps
        </p>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2">
          {nextActions.map((action: any, i: number) => (
            <div
              key={i}
              className="p-4 rounded-xl border border-slate-200 bg-slate-50/50 flex flex-col justify-between"
            >
              <div>
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
                <h3 className="text-xs font-bold text-slate-800 mt-2">{action.title}</h3>
                <p className="text-[11px] text-slate-500 mt-1 leading-relaxed">{action.rationale}</p>
              </div>
              <div className="pt-3 mt-3 border-t border-slate-200/60 flex items-center justify-between text-xs">
                <span className="text-[10px] text-slate-400">{action.duration_minutes} mins</span>
                <Link
                  to={action.category === 'LEARN' ? '/tutor' : '/assessment'}
                  className="font-semibold text-indigo-600 hover:text-indigo-700 inline-flex items-center"
                >
                  Start <ArrowRight className="w-3 h-3 ml-1" />
                </Link>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
