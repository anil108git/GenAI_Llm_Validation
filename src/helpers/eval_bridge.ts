import axios, { AxiosInstance } from 'axios';

const EVAL_SERVICE_URL = 'http://localhost:8000';

const apiClient: AxiosInstance = axios.create({
  baseURL: EVAL_SERVICE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

export interface EvalPayload {
  prompt: string;
  response: string;
  retrieval_context?: string;
  context?: string;
  demographic_features?: Record<string, unknown>;
}

export interface EvalResult {
  score: number;
  success: boolean;
}

async function postEval(endpoint: string, payload: EvalPayload): Promise<EvalResult> {
  const response = await apiClient.post<EvalResult>(endpoint, payload);
  return response.data;
}

export const evalBridge = {
  faithfulness: (payload: EvalPayload) => postEval('/evaluate/faithfulness', payload),
  relevancy: (payload: EvalPayload) => postEval('/evaluate/relevancy', payload),
  contextual: (payload: EvalPayload) => postEval('/evaluate/contextual', payload),
  hallucination: (payload: EvalPayload) => postEval('/evaluate/hallucination', payload),
  bias: (payload: EvalPayload) => postEval('/evaluate/bias', payload),
};
