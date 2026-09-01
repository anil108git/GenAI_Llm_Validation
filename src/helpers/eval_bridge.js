const axios = require('axios');

const EVAL_SERVICE_URL = process.env.EVAL_SERVICE_URL || 'http://127.0.0.1:8000';
const client = axios.create({
  baseURL: EVAL_SERVICE_URL,
  headers: { 'Content-Type': 'application/json' },
  timeout: 10000,
});

async function postEval(endpoint, payload) {
  const response = await client.post(endpoint, payload);
  return response.data;
}

module.exports = {
  postEval,
  faithfulness: (payload) => postEval('/evaluate/faithfulness', payload),
  relevancy: (payload) => postEval('/evaluate/relevancy', payload),
  contextual: (payload) => postEval('/evaluate/contextual', payload),
  hallucination: (payload) => postEval('/evaluate/hallucination', payload),
  bias: (payload) => postEval('/evaluate/bias', payload),
};
