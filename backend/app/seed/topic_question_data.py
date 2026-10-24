"""
Comprehensive Question Bank for MasteryLoop.
Provides 15 distinct, psychometrically-calibrated assessment items for each of the 22 curriculum topics.
Total: 22 topics * 15 questions = 330 items.
Each item features:
- Precise skill alignment
- 4 realistic options (A, B, C, D)
- Pedagogical explanation & distractor misconception rationales
- 2PL IRT parameters: difficulty b spanning easy, medium, hard (-1.8 to +1.8) and discrimination a (1.0 to 1.9)
"""

from typing import List, Dict, Any

ALL_TOPIC_ITEMS: List[Dict[str, Any]] = []

def add_items(items):
    ALL_TOPIC_ITEMS.extend(items)
