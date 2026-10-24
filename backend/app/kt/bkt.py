"""
Bayesian Knowledge Tracing (BKT) Service.
Deterministic skill-level mastery updater with slip, guess, and transition dynamics.
Provides calibrated posterior probabilities, certainty bounds, and predicted accuracy.
"""

from typing import Dict, Any, Tuple

# Standard BKT Hyperparameters (Corbett & Anderson baseline)
DEFAULT_PRIOR_L0 = 0.40    # Initial knowledge prior
DEFAULT_TRANSITION_T = 0.15 # Learning rate between opportunities
DEFAULT_GUESS_G = 0.20      # Probability of guessing correctly for 4-choice MCQ
DEFAULT_SLIP_S = 0.10       # Probability of slipping on known skill


class BKTModel:
    """Standard 4-parameter Bayesian Knowledge Tracing model."""

    def __init__(
        self,
        l0: float = DEFAULT_PRIOR_L0,
        t: float = DEFAULT_TRANSITION_T,
        g: float = DEFAULT_GUESS_G,
        s: float = DEFAULT_SLIP_S
    ):
        self.l0 = l0
        self.t = t
        self.g = g
        self.s = s

    def update_mastery(
        self,
        current_mastery: float,
        is_correct: bool,
        confidence_rating: int = 2
    ) -> Tuple[float, float]:
        """
        Calculates posterior mastery probability P(L_t+1) after observing a response.
        
        Optional confidence weighting:
        - If learner was confident and correct, slip probability is reduced.
        - If learner guessed (low confidence) and was correct, guess probability is adjusted higher.
        
        Returns:
        - (new_mastery, new_confidence): posterior mastery probability [0.0 - 1.0] and estimation certainty [0.0 - 1.0].
        """
        # Minor adaptive calibration based on self-reported confidence
        g = self.g
        s = self.s
        if confidence_rating == 1:  # Low confidence / guessed
            g = min(self.g + 0.15, 0.45)
        elif confidence_rating == 3: # High confidence
            s = max(self.s - 0.05, 0.03)

        p_l = current_mastery

        # Step 1: Compute posterior given observation P(L_t | obs)
        if is_correct:
            numerator = p_l * (1.0 - s)
            denominator = numerator + ((1.0 - p_l) * g)
        else:
            numerator = p_l * s
            denominator = numerator + ((1.0 - p_l) * (1.0 - g))

        p_obs = numerator / max(denominator, 1e-9)

        # Step 2: Apply learning transition to next state P(L_t+1)
        new_mastery = p_obs + ((1.0 - p_obs) * self.t)

        # Clip bounds to keep mathematically valid probabilities
        new_mastery = max(min(round(new_mastery, 4), 0.999), 0.001)

        return new_mastery

    def predict_next_correct(self, mastery: float) -> float:
        """
        Predicts the probability that the learner answers the next item on this skill correctly:
        P(C) = P(L)*(1 - S) + (1 - P(L))*G
        """
        return round(mastery * (1.0 - self.s) + (1.0 - mastery) * self.g, 4)

    def calculate_confidence(self, interaction_count: int, raw_accuracy: float, current_mastery: float) -> float:
        """
        Estimates the epistemic confidence in the mastery assessment [0.0 to 1.0].
        Increases asymptotically with interaction volume and consistency.
        """
        if interaction_count <= 0:
            return 0.15
        
        # Volume factor: 1 - 1/sqrt(N+1)
        volume_factor = 1.0 - (1.0 / ((interaction_count + 1) ** 0.5))
        
        # Consistency alignment between raw accuracy and posterior mastery
        alignment = 1.0 - min(abs(raw_accuracy - current_mastery), 0.5)
        
        confidence = (0.75 * volume_factor) + (0.25 * alignment)
        return round(max(min(confidence, 0.98), 0.15), 4)


# Global default instance
bkt_service = BKTModel()
