import unittest

from examples.python.decision_policies import (
    ActionDecision,
    gate_action,
    rag_decision,
    weighted_score,
)


class GateActionTests(unittest.TestCase):
    def test_low_confidence_always_goes_to_review(self):
        self.assertEqual(gate_action("check_balance", 0.59), ActionDecision("human_review"))

    def test_low_stakes_action_can_run_without_confirmation(self):
        self.assertEqual(gate_action("check_balance", 0.60), ActionDecision("show_balance"))

    def test_transfer_requires_confirmation_until_high_confidence(self):
        self.assertEqual(
            gate_action("approve_transfer", 0.90),
            ActionDecision("approve_transfer", requires_confirmation=True),
        )
        self.assertEqual(
            gate_action("approve_transfer", 0.91),
            ActionDecision("approve_transfer", requires_confirmation=False),
        )

    def test_unknown_action_is_safe_by_default(self):
        self.assertEqual(gate_action("delete_account", 0.99), ActionDecision("human_review"))

    def test_confidence_must_be_in_range(self):
        with self.assertRaises(ValueError):
            gate_action("support", 1.01)


class WeightedScoreTests(unittest.TestCase):
    def test_weights_are_normalized(self):
        self.assertAlmostEqual(
            weighted_score({"quality": 0.8, "speed": 0.4}, {"quality": 3, "speed": 1}),
            0.7,
        )

    def test_dimensions_must_match(self):
        with self.assertRaises(ValueError):
            weighted_score({"quality": 0.8}, {"speed": 1})

    def test_zero_weights_are_rejected(self):
        with self.assertRaises(ValueError):
            weighted_score({"quality": 0.8}, {"quality": 0})


class RagDecisionTests(unittest.TestCase):
    def test_injection_risk_wins_over_relevance(self):
        self.assertEqual(
            rag_decision(
                answers_query=0.99,
                supports_answer=0.99,
                contains_injection=0.20,
                relevance_score=2.0,
            ),
            "reject_injection_risk",
        )

    def test_weak_evidence_is_rejected(self):
        self.assertEqual(
            rag_decision(
                answers_query=0.64,
                supports_answer=0.90,
                contains_injection=0.01,
                relevance_score=2.0,
            ),
            "reject_weak_evidence",
        )

    def test_good_evidence_is_kept(self):
        self.assertEqual(
            rag_decision(
                answers_query=0.80,
                supports_answer=0.77,
                contains_injection=0.02,
                relevance_score=1.50,
            ),
            "keep",
        )


if __name__ == "__main__":
    unittest.main()
