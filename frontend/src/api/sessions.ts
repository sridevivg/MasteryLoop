import { apiClient } from './client';

export interface StartSessionPayload {
  domain_id?: string;
  topic_id?: string;
  kind?: 'ADAPTIVE' | 'DIAGNOSTIC' | 'FIXED' | 'MASTERY_REASSESSMENT';
  max_questions?: number;
}

export interface SanitizedQuestionItem {
  id: string;
  stem: string;
  item_type: string;
  options: Array<{
    id: string;
    text: string;
  }>;
  code_template?: string;
  visible_test_cases?: Array<{
    input: string;
    expected_output: string;
    is_hidden: boolean;
  }>;
  question_number: number;
  total_questions_estimated: number;
  selection_explanation: any;
  domain_name?: string;
  topic_name?: string;
  warning?: string;
}

export interface StartSessionResponse {
  session_id: string;
  kind: string;
  first_item: SanitizedQuestionItem;
  started_at: string;
  domain_name?: string;
  topic_name?: string;
  total_questions_estimated?: number;
  warning?: string;
}

export interface ActiveSessionStatusResponse {
  session_id: string;
  kind: string;
  status: string;
  domain_name?: string;
  topic_id?: string;
  topic_name?: string;
  current_question_number: number;
  total_questions_estimated: number;
  theta_estimate: number;
  se_estimate: number;
  warning?: string;
  current_item?: SanitizedQuestionItem;
  is_completed: boolean;
  report?: any;
}

export interface SubmitResponsePayload {
  item_id: string;
  response_value: string;
  latency_ms: number;
  confidence_rating?: number;
}

export interface SubmitResponseResult {
  is_correct: boolean;
  correct_key: string;
  explanation: string;
  misconception_feedback?: string;
  updated_theta: number;
  updated_se: number;
  next_item?: SanitizedQuestionItem;
  is_completed: boolean;
  report?: any;
}

export interface SessionHistoryItem {
  session_id: string;
  kind: string;
  status: string;
  domain_name: string;
  accuracy_percentage?: number;
  questions_answered: number;
  estimated_ability_theta: number;
  started_at: string;
  completed_at?: string;
}

export const sessionsApi = {
  startSession: (payload: StartSessionPayload) =>
    apiClient<StartSessionResponse>('/sessions', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),

  submitResponse: (sessionId: string, payload: SubmitResponsePayload) =>
    apiClient<SubmitResponseResult>(`/sessions/${sessionId}/respond`, {
      method: 'POST',
      body: JSON.stringify(payload),
    }),

  getSessionReport: (sessionId: string) =>
    apiClient<any>(`/sessions/${sessionId}/report`, {
      method: 'GET',
    }),

  getCurrentSession: (sessionId: string) =>
    apiClient<ActiveSessionStatusResponse>(`/sessions/${sessionId}/current`, {
      method: 'GET',
    }),

  getHistory: () =>
    apiClient<SessionHistoryItem[]>('/sessions/history/me', {
      method: 'GET',
    }),
};
