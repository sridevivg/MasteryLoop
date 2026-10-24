import React from 'react';
import { AlertCircle, RefreshCw } from 'lucide-react';

interface ErrorBannerProps {
  message: string;
  onRetry?: () => void;
}

export const ErrorBanner: React.FC<ErrorBannerProps> = ({ message, onRetry }) => (
  <div className="bg-rose-50 border border-rose-200 text-rose-800 rounded-lg p-4 flex items-start justify-between">
    <div className="flex items-start space-x-3">
      <AlertCircle className="w-5 h-5 text-rose-600 mt-0.5 flex-shrink-0" />
      <div>
        <p className="text-sm font-medium">{message}</p>
      </div>
    </div>
    {onRetry && (
      <button
        onClick={onRetry}
        className="ml-4 inline-flex items-center text-xs font-semibold text-rose-700 hover:text-rose-900 bg-rose-100 hover:bg-rose-200 px-2.5 py-1.5 rounded transition"
      >
        <RefreshCw className="w-3.5 h-3.5 mr-1" /> Retry
      </button>
    )}
  </div>
);
