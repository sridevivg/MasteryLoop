import { apiClient } from './client';
import { Domain, Skill } from '../types';

export interface PrerequisiteDetail {
  id: string;
  name: string;
  code: string;
  difficulty_level: number;
}

export interface SkillPrerequisitesResponse {
  target_skill: PrerequisiteDetail;
  direct_prerequisites: PrerequisiteDetail[];
  foundational_prerequisites_topological: PrerequisiteDetail[];
  direct_dependents: PrerequisiteDetail[];
  all_downstream_dependents: PrerequisiteDetail[];
}

export interface TopicSummary {
  id: string;
  name: string;
  domain_id: string;
  domain_name: string;
  description?: string;
  question_count: number;
}

export const curriculumApi = {
  getDomains: () =>
    apiClient<Domain[]>('/curriculum/domains', {
      method: 'GET',
    }),

  getTopics: (domainId?: string) =>
    apiClient<TopicSummary[]>(domainId ? `/curriculum/topics?domain_id=${domainId}` : '/curriculum/topics', {
      method: 'GET',
    }),

  getValidationReport: () =>
    apiClient<any>('/curriculum/validation-report', {
      method: 'GET',
    }),

  getDomainHierarchy: (domainIdOrCode: string) =>
    apiClient<Domain>(`/curriculum/domains/${domainIdOrCode}`, {
      method: 'GET',
    }),

  getSkill: (skillIdOrCode: string) =>
    apiClient<Skill>(`/curriculum/skills/${skillIdOrCode}`, {
      method: 'GET',
    }),

  getSkillPrerequisites: (skillIdOrCode: string) =>
    apiClient<SkillPrerequisitesResponse>(`/curriculum/skills/${skillIdOrCode}/prerequisites`, {
      method: 'GET',
    }),

  getGraph: (domainId?: string) =>
    apiClient<any>(domainId ? `/curriculum/graph?domain_id=${domainId}` : '/curriculum/graph', {
      method: 'GET',
    }),
};
