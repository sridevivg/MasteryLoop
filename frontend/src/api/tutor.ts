import { apiClient } from './client';
import { TutorChatResponse, TutorMode, TutorLanguage } from '../types';

export interface ChatMessage {
  role: 'user' | 'assistant' | 'system';
  content: string;
}

export interface TutorChatPayload {
  message: string;
  mode: TutorMode;
  language: TutorLanguage;
  skill_id?: string;
  item_id?: string;
  history?: ChatMessage[];
}

export interface AiDiagnosticsResponse {
  status: string;
  llm_provider: {
    active_provider: string;
    configured_type: string;
    openai_configured: boolean;
    gemini_configured: boolean;
    timeout_seconds: number;
  };
  embedding_provider: {
    active_provider: string;
    configured_type: string;
    dimension: number;
    indexed_chunks: number;
  };
  storage: {
    qdrant_backend: string;
    collection: string;
  };
}

export const tutorApi = {
  chat: (payload: TutorChatPayload) =>
    apiClient<TutorChatResponse>('/tutor/chat', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),

  getDiagnostics: () =>
    apiClient<AiDiagnosticsResponse>('/tutor/diagnostics', {
      method: 'GET',
    }),
};
