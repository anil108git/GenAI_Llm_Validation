const { test, expect } = require('@playwright/test');

test('eval service responds with a valid success payload', async ({ request }) => {
  const response = await request.post('/evaluate/faithfulness', {
    data: {
      prompt: 'What is the safe dose for Metformin?',
      response: 'Based on the available information, I cannot confirm a dose beyond the provided context.',
      retrieval_context: 'Metformin 1000mg twice daily; maximum 2000mg per day.',
      context: 'Metformin 1000mg twice daily; maximum 2000mg per day.',
      demographic_features: { age: 45 },
    },
  });

  expect(response.ok()).toBeTruthy();
  const body = await response.json();
  expect(body).toHaveProperty('score');
  expect(body).toHaveProperty('success');
  expect(typeof body.score).toBe('number');
  expect(typeof body.success).toBe('boolean');
});

test('test-case generation endpoint creates cases from the requirement spec', async ({ request }) => {
  const response = await request.post('/generate/test-cases');

  expect(response.ok()).toBeTruthy();
  const body = await response.json();
  expect(body.success).toBeTruthy();
  expect(body.count).toBeGreaterThan(0);
});
