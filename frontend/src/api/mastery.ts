import { apiClient } from './client';

export interface DashboardResponse {
  overall_mastery: number;
  placement_readiness: number;
  study_streak_days: number;
  total_assessments_taken: number;
  total_questions_solved: number;
  retention_due_count: number;
  strong_topics: Array<{
    name?: string;
    topic_name?: string;
    domain?: string;
    domain_name?: string;
    mastery?: number;
    mastery_percentage?: number;
  }>;
  weak_topics: Array<{
    name?: string;
    topic_name?: string;
    domain?: string;
    domain_name?: string;
    mastery?: number;
    mastery_percentage?: number;
  }>;
  placement_domains: Array<{
    domain_id: string;
    domain_name: string;
    readiness_percentage: number;
    tested_skills_count: number;
    total_skills_count: number;
    benchmark_status: string;
    top_strength?: string;
    priority_weakness?: string;
  }>;
  next_best_actions: Array<{
    category: 'LEARN' | 'PRACTICE' | 'REASSESS';
    skill_id: string;
    skill_name: string;
    domain_name: string;
    title: string;
    duration_minutes: number;
    rationale: string;
    action_type: string;
    target_id?: string;
  }>;
  today_challenge?: {
    title: string;
    description: string;
    skill_name?: string;
    target_score?: number;
    xp_reward?: number;
    is_completed?: boolean;
    completed?: boolean;
    score_percentage?: number;
  };
  recent_assessments: Array<{
    session_id: string;
    domain_name?: string;
    completed_at?: string;
    date?: string;
    score?: number;
    accuracy_percentage?: number;
    theta?: number;
    kind?: string;
    status?: string;
  }>;
  mastery_trend: Array<any>;
}

export interface DueSkillItem {
  skill_id: string;
  skill_name: string;
  topic_name?: string;
  domain_name?: string;
  current_retention?: number;
  retention_estimate?: number;
  forgetting_risk?: number;
  next_review_due?: string | null;
  is_overdue?: boolean;
  days_overdue?: number;
  interaction_count?: number;
  stability_days?: number;
}

export interface DueReviewsResponse {
  user_id: string;
  due_count: number;
  due_skills: DueSkillItem[];
}

export interface RecordReviewResponse {
  status: string;
  skill_id: string;
  skill_name: string;
  is_correct: boolean;
  new_retention_estimate: number;
  next_review_due: string | null;
  interaction_count: number;
}

export const masteryApi = {
  getDashboard: () =>
    apiClient<DashboardResponse>('/mastery/dashboard', {
      method: 'GET',
    }),

  getSkills: (domainId?: string) =>
    apiClient<any[]>(domainId ? `/mastery/skills?domain_id=${domainId}` : '/mastery/skills', {
      method: 'GET',
    }),

  getForecast: (targetDomainId?: string) =>
    apiClient<any>('/mastery/forecast', {
      method: 'POST',
      body: JSON.stringify({ target_domain_id: targetDomainId }),
    }),

  getDueReviews: () =>
    apiClient<DueReviewsResponse>('/mastery/retention/due', {
      method: 'GET',
    }),

  recordReview: (skillId: string, isCorrect: boolean) =>
    apiClient<RecordReviewResponse>('/mastery/retention/review', {
      method: 'POST',
      body: JSON.stringify({ skill_id: skillId, is_correct: isCorrect }),
    }),
};
