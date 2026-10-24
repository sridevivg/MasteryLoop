import { apiClient } from './client';

export interface DraftItemResponse {
  id: string;
  stem: string;
  item_type: string;
  options: Array<{
    id: string;
    text: string;
    is_distractor?: boolean;
  }>;
  explanation?: string;
  distractor_explanations?: Record<string, string>;
  a: number;
  b: number;
  point_biserial: number;
  is_calibrated: number;
  exposure_count: number;
  state: string;
  origin: string;
  lineage?: {
    model?: string;
    screening_checks?: {
      schema_valid?: boolean;
      distractors_verified?: boolean;
      blind_solver_passed?: boolean;
    };
    created_at?: string;
    prompt_version?: string;
  };
}

export interface ReviewItemPayload {
  action: 'APPROVE' | 'EDIT' | 'REJECT' | 'REQUEST_REGEN';
  reason: string;
  edits?: Record<string, any>;
}

export interface GenerateDraftPayload {
  skill_id: string;
  difficulty_band?: 'easy' | 'medium' | 'hard';
  item_type?: 'MCQ' | 'CODING_SNIPPET' | 'SQL_QUERY';
}

export const itemsApi = {
  getReviewQueue: () =>
    apiClient<DraftItemResponse[]>('/items/review-queue', {
      method: 'GET',
    }),

  reviewItem: (itemId: string, payload: ReviewItemPayload) =>
    apiClient<any>(`/items/${itemId}/review`, {
      method: 'POST',
      body: JSON.stringify(payload),
    }),

  generateDraft: (payload: GenerateDraftPayload) =>
    apiClient<DraftItemResponse>('/items/generate', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),
};
