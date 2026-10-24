import React, { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { authApi } from '../api/auth';
import { ErrorBanner } from '../components/ErrorBanner';
import { LogIn, ArrowRight, UserCheck, ShieldCheck, Sparkles } from 'lucide-react';

export const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { login } = useAuth();

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const from = (location.state as any)?.from?.pathname || '/';

  const executeLogin = async (loginEmail: string, loginPass: string) => {
    setError(null);
    try {
      setLoading(true);
      const authRes = await authApi.login({
        email: loginEmail.trim(),
        password: loginPass,
      });

      // Fetch user profile
      localStorage.setItem('masteryloop_token', authRes.access_token);
      const userProfile = await authApi.getMe();
      login(authRes.access_token, userProfile);

      navigate(from, { replace: true });
    } catch (err: any) {
      setError(err.message || 'Login failed. Please verify your credentials.');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email.trim() || !password) {
      setError('Please provide both your email address and password.');
      return;
    }
    await executeLogin(email, password);
  };

  const handleQuickLogin = (demoEmail: string) => {
    setEmail(demoEmail);
    setPassword('Password123!');
    executeLogin(demoEmail, 'Password123!');
  };

  return (
    <div className="min-h-[calc(100vh-4rem)] flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8 bg-slate-50">
      <div className="max-w-md w-full space-y-6 bg-white p-8 rounded-2xl border border-slate-200 shadow-sm">
        <div>
          <div className="w-12 h-12 bg-indigo-50 text-indigo-600 rounded-xl flex items-center justify-center mx-auto mb-3">
            <LogIn className="w-6 h-6" />
          </div>
          <h2 className="text-center text-2xl font-bold text-slate-900 tracking-tight">
            Sign in to MasteryLoop
          </h2>
          <p className="mt-1.5 text-center text-xs text-slate-500">
            Adaptive placement preparation & cognitive knowledge tracing
          </p>
        </div>

        {/* 1-Click Demo Profiles */}
        <div className="p-3.5 bg-indigo-50/70 border border-indigo-100 rounded-xl space-y-2">
          <div className="flex items-center space-x-1.5 text-indigo-900 text-xs font-semibold">
            <Sparkles className="w-3.5 h-3.5 text-indigo-600" />
            <span>Instant Demo Sign-in:</span>
          </div>
          <div className="grid grid-cols-2 gap-2 text-xs">
            <button
              type="button"
              onClick={() => handleQuickLogin('student@masteryloop.ai')}
              disabled={loading}
              className="p-2 rounded-lg bg-white border border-indigo-200 hover:border-indigo-400 hover:bg-indigo-50/50 text-left transition flex items-center space-x-2 text-slate-700 shadow-sm disabled:opacity-50"
            >
              <UserCheck className="w-3.5 h-3.5 text-indigo-600 flex-shrink-0" />
              <div className="truncate">
                <div className="font-semibold text-slate-900 text-[11px]">Demo Student</div>
                <div className="text-[10px] text-slate-500">Learner Account</div>
              </div>
            </button>

            <button
              type="button"
              onClick={() => handleQuickLogin('teacher@masteryloop.ai')}
              disabled={loading}
              className="p-2 rounded-lg bg-white border border-indigo-200 hover:border-indigo-400 hover:bg-indigo-50/50 text-left transition flex items-center space-x-2 text-slate-700 shadow-sm disabled:opacity-50"
            >
              <ShieldCheck className="w-3.5 h-3.5 text-amber-600 flex-shrink-0" />
              <div className="truncate">
                <div className="font-semibold text-slate-900 text-[11px]">Demo Teacher</div>
                <div className="text-[10px] text-slate-500">Review Queue SME</div>
              </div>
            </button>
          </div>
        </div>

        {error && <ErrorBanner message={error} />}

        <form className="space-y-4" onSubmit={handleSubmit}>
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-600 mb-1">
              Email address
            </label>
            <input
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="student@example.com"
              className="w-full px-3.5 py-2.5 border border-slate-200 rounded-lg text-sm text-slate-800 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-600 transition"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-600 mb-1">
              Password
            </label>
            <input
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              className="w-full px-3.5 py-2.5 border border-slate-200 rounded-lg text-sm text-slate-800 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-600 transition"
            />
          </div>

          <div>
            <button
              type="submit"
              disabled={loading}
              className="w-full flex justify-center items-center py-2.5 px-4 border border-transparent rounded-lg text-sm font-semibold text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed transition shadow-sm"
            >
              {loading ? 'Authenticating...' : 'Sign in'}
              {!loading && <ArrowRight className="w-4 h-4 ml-1.5" />}
            </button>
          </div>
        </form>

        <div className="pt-2 border-t border-slate-100 text-center">
          <p className="text-xs text-slate-500">
            Don't have an account yet?{' '}
            <Link to="/register" className="font-semibold text-indigo-600 hover:text-indigo-700">
              Create an account
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};
