import { choice, noul, score, TypeSafeClient } from "@typesafe-ai/sdk";

const client = new TypeSafeClient();

const result = await client.systemOne({
  state: {
    ticket: "I was charged twice and need the duplicate refunded today.",
    accountTier: "business",
  },
  questions: {
    intent: choice("What is the customer's main request?", {
      refund: "The customer wants money returned.",
      technical_help: "The customer needs a bug or integration fixed.",
      information: "The customer is asking for information only.",
      other: "None of the other options clearly fits.",
    }),
    isUrgent: noul("Does the ticket explicitly communicate time pressure?"),
    frustration: score("How frustrated does the customer appear?", [
      "Calm and neutral",
      "Concerned but civil",
      "Very angry or using strong language",
    ]),
  },
});

console.log({
  intent: result.answers.intent.choice,
  intentProbabilities: result.answers.intent.probabilities,
  urgentProbability: result.answers.isUrgent.noul,
  frustrationScore: result.answers.frustration.score,
});
