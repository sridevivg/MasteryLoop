import { apiClient } from './client';

export interface TestCasePayload {
  input: string;
  expected_output: string;
  is_hidden?: boolean;
}

export interface TestCaseResult {
  test_case_number: number;
  passed: boolean;
  latency_ms: number;
  input: string;
  expected_output: string;
  actual_output: string;
  error?: string | null;
  timed_out: boolean;
  is_hidden: boolean;
}

export interface CodingExecutionResponse {
  success: boolean;
  error?: string | null;
  all_passed: boolean;
  passed_count: number;
  total_count: number;
  total_latency_ms: number;
  test_results: TestCaseResult[];
  is_security_violation?: boolean;
  is_syntax_error?: boolean;
}

export interface CodingSubmissionPayload {
  code: string;
  language?: string;
  item_id?: string;
  test_cases?: TestCasePayload[];
}

export const codingApi = {
  executeCode: (payload: CodingSubmissionPayload) =>
    apiClient<CodingExecutionResponse>('/coding/execute', {
      method: 'POST',
      body: JSON.stringify({
        ...payload,
        language: payload.language || 'python',
      }),
    }),
};
