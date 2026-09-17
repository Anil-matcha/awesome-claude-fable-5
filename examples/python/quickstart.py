"""Small live Jev example.

Run from the repository root after installing ``typesafe-sdk`` and setting
``TYPESAFE_API_KEY``.
"""

from typesafe_sdk import Choice, Noul, Score, TypeSafeClient


def main() -> None:
    state = {
        "ticket": "I was charged twice and need the duplicate refunded today.",
        "account_tier": "business",
    }

    with TypeSafeClient() as client:
        response = client.system_one(
            state=state,
            questions={
                "intent": Choice(
                    instructions="What is the customer's main request?",
                    criteria={
                        "refund": "The customer wants money returned.",
                        "technical_help": "The customer needs a bug or integration fixed.",
                        "information": "The customer is asking for information only.",
                        "other": "None of the other options clearly fits.",
                    },
                ),
                "is_urgent": Noul(
                    instructions="Does the ticket explicitly communicate time pressure?",
                ),
                "frustration": Score(
                    instructions="How frustrated does the customer appear?",
                    criteria=[
                        "Calm and neutral",
                        "Concerned but civil",
                        "Very angry or using strong language",
                    ],
                ),
            },
        )

    intent = response.answers["intent"]
    urgency = response.answers["is_urgent"]
    frustration = response.answers["frustration"]

    print(f"intent: {intent.choice}")
    print(f"intent probabilities: {intent.probabilities}")
    print(f"intent confidence: {intent.confidence:.3f}")
    print(f"urgent probability: {urgency.noul:.3f}")
    print(f"frustration score: {frustration.score:.3f}")


if __name__ == "__main__":
    main()
