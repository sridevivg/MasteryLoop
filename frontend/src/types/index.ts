// User & Auth Types
export type UserRole = 'STUDENT' | 'TEACHER' | 'ADMIN';

export interface User {
  id: string;
  email: string;
  full_name?: string;
  role: UserRole;
  is_active: boolean;
  created_at: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  role: UserRole;
  user_id: string;
  email: string;
}

// Curriculum Types
export interface Skill {
  id: string;
  code: string;
  name: string;
  description?: string;
  difficulty_target: number;
  bloom_level: string;
  subtopic_id: string;
  is_active: boolean;
}

export interface Subtopic {
  id: string;
  name: string;
  description?: string;
  skills: Skill[];
}

export interface Topic {
  id: string;
  name: string;
  description?: string;
  subtopics: Subtopic[];
}

export interface Domain {
  id: string;
  code: string;
  name: string;
  description: string;
  icon: string;
  order_index: number;
  topic_count?: number;
  skill_count?: number;
  topics?: Topic[];
}

// Assessment Types
export interface SanitizedQuestion {
  stem: string;
  options: Record<string, string>;
  skill_name: string;
  skill_code: string;
  bloom_level: string;
}

export interface NextQuestionResponse {
  question_number: number;
  item_id: string;
  question: SanitizedQuestion;
  current_ability_estimate: number;
  is_complete: boolean;
}

export interface SessionResponsePayload {
  selected_key: string;
  time_spent_seconds: number;
}

export interface InteractionFeedback {
  interaction_id: string;
  is_correct: boolean;
  misconception_detected: boolean;
  misconception_tag?: string;
  feedback_message: string;
  new_ability_estimate: number;
}

export interface NextBestAction {
  action_type: 'LEARN' | 'PRACTICE' | 'REASSESS';
  skill_code: string;
  skill_name: string;
  rationale: string;
  priority: number;
}

export interface AssessmentReport {
  session_id: string;
  final_theta: number;
  standard_error: number;
  confidence_interval: [number, number];
  questions_answered: number;
  accuracy: number;
  score_percentage: number;
  performance_band: string;
  skill_breakdown: Array<{
    skill_code: string;
    skill_name: string;
    mastery_estimate: number;
    status: 'Mastered' | 'In Progress' | 'Needs Remediation';
  }>;
  next_best_actions: NextBestAction[];
}

// Learner Mastery Dashboard Types
export interface LearnerDashboardData {
  overall_readiness_score: number;
  placement_probability: number;
  skills_mastered_count: number;
  total_skills_count: number;
  domain_readiness: Array<{
    domain_code: string;
    domain_name: string;
    mastery_percentage: number;
  }>;
  strong_skills: Array<{
    skill_name: string;
    domain: string;
    mastery: number;
  }>;
  weak_skills: Array<{
    skill_name: string;
    domain: string;
    mastery: number;
  }>;
  recent_sessions: Array<{
    session_id: string;
    domain_name: string;
    completed_at: string;
    score: number;
    theta: number;
  }>;
  next_best_actions: NextBestAction[];
}

// Socratic Tutor Types
export type TutorMode = 'HINT' | 'TEACH_FROM_BASICS' | 'DEBUG' | 'INTERVIEW' | 'QUICK_REVISION' | 'EXAM' | 'EXAM_MODE';
export type TutorLanguage = 'ENGLISH' | 'TAMIL' | 'TANGLISH';

export interface SourceCitation {
  title: string;
  chunk_text: string;
  relevance_score: number;
  domain?: string;
}

export interface TutorChatResponse {
  response: string;
  mode: TutorMode;
  language: TutorLanguage;
  citations: SourceCitation[];
  followup_suggestions: string[];
  provider_used?: string;
}

// Teacher Review Types
export type ItemStatus = 'GENERATED' | 'VALIDATING' | 'HUMAN_REVIEW' | 'APPROVED' | 'PILOT' | 'CALIBRATED' | 'ACTIVE' | 'RETIRED';

export interface ReviewQueueItem {
  id: string;
  stem: string;
  item_type: string;
  options: Record<string, string>;
  correct_answer_key: string;
  distractor_rationale: Record<string, string>;
  solution_explanation: string;
  skill_code: string;
  skill_name: string;
  provisional_b: number;
  provisional_a: number;
  status: ItemStatus;
  screening_metadata?: {
    schema_valid?: boolean;
    distractors_verified?: boolean;
    blind_solver_passed?: boolean;
    distractor_checks?: Record<string, boolean>;
  };
  prompt_version?: string;
  created_at: string;
}
