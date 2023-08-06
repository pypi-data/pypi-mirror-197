import unittest
from causal_testing.testing.causal_test_outcome import ExactValue, SomeEffect
from causal_testing.testing.causal_test_result import CausalTestResult, TestValue
from causal_testing.testing.estimators import LinearRegressionEstimator


class TestCausalTestOutcome(unittest.TestCase):
    """Test the TestCausalTestOutcome basic methods."""

    def setUp(self) -> None:
        self.estimator = LinearRegressionEstimator(
            treatment="A",
            outcome="A",
            treatment_value=1,
            control_value=0,
            adjustment_set={},
        )

    def test_None_ci(self):
        test_value = TestValue(type="ate", value=0)
        ctr = CausalTestResult(
            estimator=self.estimator,
            test_value=test_value,
            confidence_intervals=[None, None],
            effect_modifier_configuration=None,
        )

        self.assertIsNone(ctr.ci_low())
        self.assertIsNone(ctr.ci_high())
        self.assertEqual(
            ctr.to_dict(),
            {
                "treatment": "A",
                "control_value": 0,
                "treatment_value": 1,
                "outcome": "A",
                "adjustment_set": set(),
                "test_value": test_value,
            },
        )

    def test_empty_adjustment_set(self):
        test_value = TestValue(type="ate", value=0)
        ctr = CausalTestResult(
            estimator=self.estimator,
            test_value=test_value,
            confidence_intervals=None,
            effect_modifier_configuration=None,
        )

        self.assertIsNone(ctr.ci_low())
        self.assertIsNone(ctr.ci_high())
        self.assertEqual(
            str(ctr),
            (
                "Causal Test Result\n==============\n"
                "Treatment: A\n"
                "Control value: 0\n"
                "Treatment value: 1\n"
                "Outcome: A\n"
                "Adjustment set: set()\n"
                "ate: 0\n"
            ),
        )

    def test_exactValue_pass(self):
        test_value = TestValue(type="ate", value=5.05)
        ctr = CausalTestResult(
            estimator=self.estimator,
            test_value=test_value,
            confidence_intervals=None,
            effect_modifier_configuration=None,
        )
        ev = ExactValue(5, 0.1)
        self.assertTrue(ev.apply(ctr))

    def test_exactValue_fail(self):
        test_value = TestValue(type="ate", value=0)
        ctr = CausalTestResult(
            estimator=self.estimator,
            test_value=test_value,
            confidence_intervals=None,
            effect_modifier_configuration=None,
        )
        ev = ExactValue(5, 0.1)
        self.assertFalse(ev.apply(ctr))

    def test_someEffect_pass(self):
        test_value = TestValue(type="ate", value=5.05)
        ctr = CausalTestResult(
            estimator=self.estimator,
            test_value=test_value,
            confidence_intervals=[4.8, 6.7],
            effect_modifier_configuration=None,
        )
        ev = SomeEffect()
        self.assertTrue(ev.apply(ctr))

    def test_someEffect_fail(self):
        test_value = TestValue(type="ate", value=0)
        ctr = CausalTestResult(
            estimator=self.estimator,
            test_value=test_value,
            confidence_intervals=[-0.1, 0.2],
            effect_modifier_configuration=None,
        )
        ev = SomeEffect()
        self.assertFalse(ev.apply(ctr))
        self.assertEqual(
            str(ctr),
            (
                "Causal Test Result\n==============\n"
                "Treatment: A\n"
                "Control value: 0\n"
                "Treatment value: 1\n"
                "Outcome: A\n"
                "Adjustment set: set()\n"
                "ate: 0\n"
                "Confidence intervals: [-0.1, 0.2]\n"
            ),
        )
        self.assertEqual(
            ctr.to_dict(),
            {
                "treatment": "A",
                "control_value": 0,
                "treatment_value": 1,
                "outcome": "A",
                "adjustment_set": set(),
                "test_value": test_value,
                "ci_low": -0.1,
                "ci_high": 0.2,
            },
        )
