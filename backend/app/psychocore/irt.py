"""
Psychometric Core Engine for Item Response Theory (2PL Model).
Implements logistic probability, Fisher information, log-likelihood,
and Maximum Likelihood / Expected A Posteriori (EAP) ability estimation.
"""

import math
from typing import List, Tuple, Dict, Any, Optional

DEFAULT_PRIOR_MEAN = 0.0
DEFAULT_PRIOR_SD = 1.0


def probability_2pl(theta: float, a: float, b: float) -> float:
    """
    Computes the probability of a correct response under the 2-Parameter Logistic (2PL) model:
    P(theta) = 1 / (1 + exp(-a * (theta - b)))
    
    where:
    - theta: learner ability parameter in logits [-3.0 to +3.0]
    - a: item discrimination parameter (> 0.0, typically 0.5 to 2.5)
    - b: item difficulty parameter in logits [-3.0 to +3.0]
    """
    # Clip exponent to avoid numerical overflow
    logit = a * (theta - b)
    if logit > 35.0:
        return 1.0
    if logit < -35.0:
        return 0.0
    return 1.0 / (1.0 + math.exp(-logit))


def fisher_information_2pl(theta: float, a: float, b: float) -> float:
    """
    Computes Fisher Information for an item at ability level theta:
    I(theta) = a^2 * P(theta) * (1 - P(theta))
    
    Higher information means the item measures more precisely at that ability.
    Information is maximized when theta == b (difficulty matches learner ability).
    """
    p = probability_2pl(theta, a, b)
    q = 1.0 - p
    return (a ** 2) * p * q


def test_information(theta: float, items: List[Tuple[float, float]]) -> float:
    """
    Computes total test information:
    I_test(theta) = sum(I_i(theta))
    """
    return sum(fisher_information_2pl(theta, a, b) for a, b in items)


def standard_error(information: float) -> float:
    """
    Standard Error of measurement: SE(theta) = 1 / sqrt(I_test(theta))
    """
    if information <= 1e-6:
        return 2.5  # maximum uncertainty cap
    return min(1.0 / math.sqrt(information), 2.5)


def estimate_ability_eap(
    responses: List[Tuple[float, float, bool]],
    quadrature_points: int = 41,
    theta_min: float = -4.0,
    theta_max: float = 4.0
) -> Tuple[float, float]:
    """
    Expected A Posteriori (EAP) ability estimation using Gauss-Hermite numerical integration.
    Guarantees finite, stable ability estimates even for all-correct or all-incorrect responses.
    
    Parameters:
    - responses: list of (a, b, is_correct) tuples for answered scored items.
    
    Returns:
    - (theta_eap, se_eap): estimated ability and posterior standard deviation (SE).
    """
    if not responses:
        return (DEFAULT_PRIOR_MEAN, DEFAULT_PRIOR_SD)

    # Generate quadrature grid
    step = (theta_max - theta_min) / (quadrature_points - 1)
    grid = [theta_min + i * step for i in range(quadrature_points)]

    # Prior: Standard normal N(0, 1)
    def normal_pdf(x: float, mean: float = 0.0, sd: float = 1.0) -> float:
        return (1.0 / (sd * math.sqrt(2 * math.pi))) * math.exp(-0.5 * ((x - mean) / sd) ** 2)

    prior_weights = [normal_pdf(x) for x in grid]

    # Compute likelihood at each quadrature point
    posterior_unnorm = []
    for x, prior_w in zip(grid, prior_weights):
        log_lik = 0.0
        for a, b, is_correct in responses:
            p = probability_2pl(x, a, b)
            # Add small epsilon to avoid log(0)
            p = max(min(p, 0.9999), 0.0001)
            if is_correct:
                log_lik += math.log(p)
            else:
                log_lik += math.log(1.0 - p)
        
        # Combine likelihood and prior
        lik = math.exp(log_lik)
        posterior_unnorm.append(lik * prior_w)

    total_weight = sum(posterior_unnorm)
    if total_weight <= 1e-12:
        return (DEFAULT_PRIOR_MEAN, DEFAULT_PRIOR_SD)

    # Normalize posterior
    posterior = [w / total_weight for w in posterior_unnorm]

    # Compute expected value (mean)
    theta_eap = sum(x * w for x, w in zip(grid, posterior))

    # Compute posterior standard deviation (SE)
    variance_eap = sum(((x - theta_eap) ** 2) * w for x, w in zip(grid, posterior))
    se_eap = math.sqrt(max(variance_eap, 1e-4))

    return (round(theta_eap, 4), round(se_eap, 4))
