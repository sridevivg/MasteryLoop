import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import {
  LayoutDashboard,
  BookOpen,
  CheckCircle2,
  Sparkles,
  ShieldCheck,
  LogOut,
  Menu,
  X,
  Cpu
} from 'lucide-react';

export const Navbar: React.FC = () => {
  const { user, isAuthenticated, logout, isTeacher } = useAuth();
  const location = useLocation();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const isActive = (path: string) => location.pathname === path;

  const navLinks = [
    { name: 'Dashboard', path: '/', icon: LayoutDashboard },
    { name: 'Curriculum', path: '/curriculum', icon: BookOpen },
    { name: 'Assessment', path: '/assessment', icon: CheckCircle2 },
    { name: 'Socratic Tutor', path: '/tutor', icon: Sparkles },
    ...(isTeacher ? [{ name: 'Teacher Review', path: '/teacher/review', icon: ShieldCheck }] : []),
  ];

  return (
    <nav className="bg-white border-b border-slate-200 sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          {/* Logo & Main Navigation */}
          <div className="flex items-center space-x-8">
            <Link to="/" className="flex items-center space-x-2.5">
              <div className="w-9 h-9 rounded-lg bg-indigo-600 text-white flex items-center justify-center font-bold text-lg shadow-sm">
                ML
              </div>
              <div className="flex flex-col">
                <span className="font-semibold text-slate-900 tracking-tight text-base leading-none">
                  MasteryLoop
                </span>
                <span className="text-[10px] text-slate-500 font-medium tracking-wide uppercase mt-0.5">
                  Adaptive Placement Platform
                </span>
              </div>
            </Link>

            {isAuthenticated && (
              <div className="hidden md:flex space-x-1">
                {navLinks.map((link) => {
                  const Icon = link.icon;
                  const active = isActive(link.path);
                  return (
                    <Link
                      key={link.path}
                      to={link.path}
                      className={`inline-flex items-center px-3 py-1.5 rounded-md text-sm font-medium transition ${
                        active
                          ? 'bg-indigo-50 text-indigo-700'
                          : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
                      }`}
                    >
                      <Icon className="w-4 h-4 mr-1.5 opacity-80" />
                      {link.name}
                    </Link>
                  );
                })}
              </div>
            )}
          </div>

          {/* Right Controls */}
          <div className="hidden md:flex items-center space-x-4">
            {isAuthenticated ? (
              <>
                <div className="flex items-center space-x-2 bg-slate-50 border border-slate-200 px-2.5 py-1 rounded-full text-xs text-slate-600">
                  <Cpu className="w-3.5 h-3.5 text-indigo-500" />
                  <span>Qdrant RAG Grounded</span>
                </div>

                <div className="flex items-center space-x-3 pl-2 border-l border-slate-200">
                  <div className="text-right">
                    <p className="text-sm font-medium text-slate-800 leading-none">
                      {user?.full_name || user?.email?.split('@')[0] || 'User'}
                    </p>
                    <span
                      className={`inline-block text-[10px] font-semibold px-1.5 py-0.5 rounded uppercase mt-0.5 ${
                        user?.role === 'TEACHER' || user?.role === 'ADMIN'
                          ? 'bg-amber-100 text-amber-800'
                          : 'bg-emerald-100 text-emerald-800'
                      }`}
                    >
                      {user?.role}
                    </span>
                  </div>
                  <button
                    onClick={logout}
                    title="Sign Out"
                    className="p-1.5 text-slate-400 hover:text-slate-700 hover:bg-slate-100 rounded-md transition"
                  >
                    <LogOut className="w-4 h-4" />
                  </button>
                </div>
              </>
            ) : (
              <div className="flex items-center space-x-3">
                <Link
                  to="/login"
                  className="text-sm font-medium text-slate-600 hover:text-slate-900 px-3 py-1.5 rounded-md hover:bg-slate-100 transition"
                >
                  Sign In
                </Link>
                <Link
                  to="/register"
                  className="text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 px-3.5 py-1.5 rounded-md transition shadow-sm"
                >
                  Create Account
                </Link>
              </div>
            )}
          </div>

          {/* Mobile menu button */}
          <div className="flex items-center md:hidden">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 rounded-md text-slate-500 hover:text-slate-800 hover:bg-slate-100 focus:outline-none"
            >
              {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu Dropdown */}
      {mobileMenuOpen && (
        <div className="md:hidden border-t border-slate-200 px-4 pt-2 pb-4 space-y-1 bg-white">
          {isAuthenticated ? (
            <>
              {navLinks.map((link) => {
                const Icon = link.icon;
                const active = isActive(link.path);
                return (
                  <Link
                    key={link.path}
                    to={link.path}
                    onClick={() => setMobileMenuOpen(false)}
                    className={`flex items-center px-3 py-2 rounded-md text-sm font-medium ${
                      active ? 'bg-indigo-50 text-indigo-700' : 'text-slate-700 hover:bg-slate-100'
                    }`}
                  >
                    <Icon className="w-4 h-4 mr-2" />
                    {link.name}
                  </Link>
                );
              })}
              <div className="pt-3 border-t border-slate-100 mt-2 flex items-center justify-between">
                <div>
                  <div className="text-sm font-medium text-slate-800">{user?.email}</div>
                  <div className="text-xs text-slate-500 font-semibold">{user?.role}</div>
                </div>
                <button
                  onClick={() => {
                    setMobileMenuOpen(false);
                    logout();
                  }}
                  className="text-sm text-rose-600 font-medium px-2 py-1 rounded hover:bg-rose-50"
                >
                  Sign Out
                </button>
              </div>
            </>
          ) : (
            <div className="space-y-2 pt-2">
              <Link
                to="/login"
                onClick={() => setMobileMenuOpen(false)}
                className="block text-center py-2 text-sm font-medium text-slate-700 bg-slate-100 rounded-md"
              >
                Sign In
              </Link>
              <Link
                to="/register"
                onClick={() => setMobileMenuOpen(false)}
                className="block text-center py-2 text-sm font-medium text-white bg-indigo-600 rounded-md"
              >
                Create Account
              </Link>
            </div>
          )}
        </div>
      )}
    </nav>
  );
};
