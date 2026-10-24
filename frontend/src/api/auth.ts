import { apiClient } from './client';
import { User, AuthResponse, UserRole } from '../types';

export interface RegisterPayload {
  email: string;
  password: string;
  full_name: string;
  role: 'STUDENT' | 'TEACHER';
  cohort?: string;
}

export interface LoginPayload {
  email: string;
  password: string;
}

export const authApi = {
  register: (payload: RegisterPayload) =>
    apiClient<User>('/auth/register', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),

  login: (payload: LoginPayload) =>
    apiClient<AuthResponse>('/auth/login', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),

  getMe: () =>
    apiClient<User>('/auth/me', {
      method: 'GET',
    }),
};
