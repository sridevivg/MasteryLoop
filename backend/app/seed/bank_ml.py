"""
Machine Learning Question Bank.
Topics:
1. Supervised Learning (15 questions across ML_REGRESSION, ML_DECISION_TREES, ML_EVALUATION)
2. Neural Foundations (15 questions across ML_NEURAL_NETS)
"""

ML_ITEMS = [
    # =========================================================================
    # TOPIC 1: Supervised Learning (15 items)
    # =========================================================================
    # --- ML_REGRESSION (5 items) ---
    {
        "skill_code": "ML_REGRESSION",
        "stem": "What is the primary mathematical objective function minimized in Ordinary Least Squares (OLS) Linear Regression?",
        "options": [
            {"id": "A", "text": "Residual Sum of Squares (RSS): the sum of squared differences between observed and predicted values.", "is_distractor": False},
            {"id": "B", "text": "The sum of absolute differences between observed and predicted values (L1 norm).", "is_distractor": True},
            {"id": "C", "text": "The cross-entropy loss between probability distributions.", "is_distractor": True},
            {"id": "D", "text": "The hinge loss between target labels and margins.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "OLS minimizes the sum of squared residuals: $\\sum (y_i - \\hat{y}_i)^2$, providing a closed-form normal equation solution $\\hat{\\beta} = (X^T X)^{-1} X^T y$.",
        "distractor_explanations": {
            "B": "Mean Absolute Error / L1 loss is used in Median Regression (MAE).",
            "C": "Cross-entropy loss is used in Logistic Regression and classification neural networks.",
            "D": "Hinge loss is used in Support Vector Machines (SVM)."
        },
        "a": 1.30,
        "b": -1.20,
        "point_biserial": 0.40
    },
    {
        "skill_code": "ML_REGRESSION",
        "stem": "What is the key difference between Lasso Regression (L1 regularization) and Ridge Regression (L2 regularization)?",
        "options": [
            {"id": "A", "text": "Lasso adds an L1 penalty on the absolute values of coefficients leading to sparse models (feature selection), while Ridge penalizes squared magnitudes shrinking coefficients toward zero without making them exactly zero.", "is_distractor": False},
            {"id": "B", "text": "Ridge eliminates features entirely, whereas Lasso only scales them.", "is_distractor": True},
            {"id": "C", "text": "Lasso requires gradient ascent while Ridge uses gradient descent.", "is_distractor": True},
            {"id": "D", "text": "Ridge is only applicable to non-linear classification problems.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Because L1 contours have sharp corners at axes, the objective minimum frequently intersects at zero, producing exact feature sparsity. L2 contours are spherical, shrinking coefficients smoothly.",
        "distractor_explanations": {
            "B": "The reverse is true: Lasso performs feature selection by zeroing weights; Ridge does not.",
            "C": "Both minimize convex loss functions using standard gradient-based or coordinate-descent optimizers.",
            "D": "Ridge is a classic regularized linear regression technique."
        },
        "a": 1.55,
        "b": 0.30,
        "point_biserial": 0.47
    },
    {
        "skill_code": "ML_REGRESSION",
        "stem": "In Logistic Regression, why is the sigmoid (logistic) function applied to the linear combination of inputs $z = w^T x + b$?",
        "options": [
            {"id": "A", "text": "To map real-valued predictions $(-\\infty, +\\infty)$ onto a valid probability interval $(0, 1)$.", "is_distractor": False},
            {"id": "B", "text": "To introduce non-linear decision boundaries without kernel tricks.", "is_distractor": True},
            {"id": "C", "text": "To prevent overfitting on training data.", "is_distractor": True},
            {"id": "D", "text": "To eliminate the need for feature standardization.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "The sigmoid function $\\sigma(z) = \\frac{1}{1 + e^{-z}}$ squashes linear log-odds into the range (0, 1), representing the Bernoulli probability $P(Y=1|X)$.",
        "distractor_explanations": {
            "B": "The decision boundary $\\sigma(z) = 0.5 \\iff z = 0$ remains strictly linear in the input feature space.",
            "C": "Sigmoid does not regularize or prevent overfitting.",
            "D": "Gradient descent in logistic regression still benefits heavily from feature scaling."
        },
        "a": 1.35,
        "b": -0.70,
        "point_biserial": 0.42
    },
    {
        "skill_code": "ML_REGRESSION",
        "stem": "What does a high Variance inflation Factor (VIF > 10) indicate in multiple linear regression?",
        "options": [
            {"id": "A", "text": "Severe multicollinearity among predictor variables, inflating standard errors of coefficient estimates.", "is_distractor": False},
            {"id": "B", "text": "Heteroscedasticity of residuals across fitted values.", "is_distractor": True},
            {"id": "C", "text": "Underfitting due to an overly simplistic linear model assumption.", "is_distractor": True},
            {"id": "D", "text": "Zero correlation between the predictors and the response variable.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "VIF measures how much the variance of an estimated regression coefficient increases when predictors are correlated: $\\text{VIF} = \\frac{1}{1 - R_j^2}$. VIF > 10 signals problematic collinearity.",
        "distractor_explanations": {
            "B": "Heteroscedasticity is evaluated using the Breusch-Pagan or White test, not VIF.",
            "C": "VIF measures feature interdependency, not model capacity/underfitting.",
            "D": "High VIF means strong correlation among predictors, not absence of correlation."
        },
        "a": 1.60,
        "b": 0.80,
        "point_biserial": 0.49
    },
    {
        "skill_code": "ML_REGRESSION",
        "stem": "Why is Mean Squared Error (MSE) generally NOT used as the loss function for Logistic Regression?",
        "options": [
            {"id": "A", "text": "MSE combined with the sigmoid activation yields a non-convex loss surface with multiple local minima.", "is_distractor": False},
            {"id": "B", "text": "MSE cannot be differentiated with respect to model weights.", "is_distractor": True},
            {"id": "C", "text": "MSE produces negative loss values for binary outcomes.", "is_distractor": True},
            {"id": "D", "text": "MSE is only defined for integer-valued target variables.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Plugging the non-linear sigmoid function into MSE results in a non-convex cost function where gradient descent can get trapped in sub-optimal local minima. Binary Cross-Entropy is convex.",
        "distractor_explanations": {
            "B": "MSE with sigmoid is differentiable via the chain rule.",
            "C": "Squared differences are strictly non-negative.",
            "D": "MSE is defined for continuous real values."
        },
        "a": 1.65,
        "b": 1.10,
        "point_biserial": 0.51
    },

    # --- ML_DECISION_TREES (5 items) ---
    {
        "skill_code": "ML_DECISION_TREES",
        "stem": "In the CART (Classification and Regression Trees) algorithm, what splitting criterion is minimized to evaluate candidate splits for classification tasks?",
        "options": [
            {"id": "A", "text": "Gini Impurity", "is_distractor": False},
            {"id": "B", "text": "Shannon Entropy only", "is_distractor": True},
            {"id": "C", "text": "Mean Absolute Percentage Error", "is_distractor": True},
            {"id": "D", "text": "Adjusted R-squared", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "CART default criterion for classification is Gini impurity: $I_G(p) = 1 - \\sum p_i^2$, measuring the probability of a randomly chosen element being incorrectly labeled.",
        "distractor_explanations": {
            "B": "Entropy is used by ID3 and C4.5, whereas CART uses Gini by default (though both are supported in modern libraries).",
            "C": "MAPE is a regression metric.",
            "D": "Adjusted R-squared is a linear model goodness-of-fit metric."
        },
        "a": 1.30,
        "b": -0.90,
        "point_biserial": 0.39
    },
    {
        "skill_code": "ML_DECISION_TREES",
        "stem": "Why are unpruned decision trees prone to high variance (overfitting)?",
        "options": [
            {"id": "A", "text": "They continue splitting recursively until leaves become pure, capturing noise and idiosyncrasies in the training data.", "is_distractor": False},
            {"id": "B", "text": "They assume a strictly linear relationship between features and targets.", "is_distractor": True},
            {"id": "C", "text": "They have high bias that cannot fit complex training patterns.", "is_distractor": True},
            {"id": "D", "text": "They cannot process categorical features without one-hot encoding.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Without constraints like `max_depth` or minimum samples per leaf, decision trees partition the input space until every training sample is isolated, resulting in low bias but very high variance.",
        "distractor_explanations": {
            "B": "Decision trees are non-parametric and partition space orthogonally, not assuming linearity.",
            "C": "Deep decision trees have very low bias, not high bias.",
            "D": "Tree algorithms naturally handle categorical splits."
        },
        "a": 1.40,
        "b": -0.40,
        "point_biserial": 0.42
    },
    {
        "skill_code": "ML_DECISION_TREES",
        "stem": "How does a **Random Forest** achieve lower variance compared to a single deep decision tree?",
        "options": [
            {"id": "A", "text": "By aggregating predictions across an ensemble of decorrelated trees trained on bootstrap samples with random feature subsets.", "is_distractor": False},
            {"id": "B", "text": "By sequentially boosting errors of previous weak trees using gradient steps.", "is_distractor": True},
            {"id": "C", "text": "By applying L1 regularization to leaf node probabilities.", "is_distractor": True},
            {"id": "D", "text": "By restricting all trees to a maximum depth of 1 (decision stumps).", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Random Forest uses bagging (Bootstrap Aggregating) combined with random subspace feature selection ($m \\approx \\sqrt{p}$), reducing ensemble variance without increasing bias.",
        "distractor_explanations": {
            "B": "Describes Gradient Boosting (GBM/XGBoost), not Random Forest.",
            "C": "Trees do not regularize via L1 penalties on weights.",
            "D": "Decision stumps are typical base learners for AdaBoost, not standard Random Forest."
        },
        "a": 1.45,
        "b": 0.10,
        "point_biserial": 0.45
    },
    {
        "skill_code": "ML_DECISION_TREES",
        "stem": "What is the primary difference between **Bagging** and **Boosting** ensemble techniques?",
        "options": [
            {"id": "A", "text": "Bagging trains base learners in parallel on independent bootstrap samples to reduce variance; Boosting trains learners sequentially to correct mistakes of prior learners, reducing bias.", "is_distractor": False},
            {"id": "B", "text": "Bagging uses deep neural networks; Boosting uses only linear models.", "is_distractor": True},
            {"id": "C", "text": "Bagging reduces bias only; Boosting reduces variance only.", "is_distractor": True},
            {"id": "D", "text": "Bagging assigns unequal weights to training samples; Boosting uses uniform weights.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Bagging (e.g., Random Forest) averages independent high-variance learners in parallel. Boosting (e.g., XGBoost, LightGBM) trains additive models iteratively to eliminate residual errors.",
        "distractor_explanations": {
            "B": "Both are general ensemble frameworks typically applied to decision trees.",
            "C": "The roles are inverted: Bagging primarily targets variance; Boosting primarily targets bias.",
            "D": "Boosting (like AdaBoost) dynamically reweights samples based on error."
        },
        "a": 1.55,
        "b": 0.50,
        "point_biserial": 0.48
    },
    {
        "skill_code": "ML_DECISION_TREES",
        "stem": "Why are decision trees invariant to monotonic transformations of continuous features (e.g., $x' = \\log(x)$ or scaling)?",
        "options": [
            {"id": "A", "text": "Tree splits depend solely on the rank order of feature values, which is preserved under monotonic transformations.", "is_distractor": False},
            {"id": "B", "text": "Trees standardize all inputs to standard normal distributions prior to training.", "is_distractor": True},
            {"id": "C", "text": "Trees calculate Euclidean distance between feature points.", "is_distractor": True},
            {"id": "D", "text": "Logarithmic scaling cancels out in the Gini impurity formula.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "A split $x \\le c$ maps directly to $f(x) \\le f(c)$ if $f$ is strictly monotonic. Because only sorting and thresholding are used, tree decisions remain completely unchanged.",
        "distractor_explanations": {
            "B": "Trees do not require or perform feature scaling or standardization.",
            "C": "Distance metrics are used in KNN and SVM, not axis-aligned decision trees.",
            "D": "Gini impurity depends on label distributions in child partitions, not the numerical feature values."
        },
        "a": 1.65,
        "b": 1.00,
        "point_biserial": 0.52
    },

    # --- ML_EVALUATION (5 items) ---
    {
        "skill_code": "ML_EVALUATION",
        "stem": "In a medical diagnosis task where failing to detect a malignant tumor has catastrophic consequences, which metric must be prioritized?",
        "options": [
            {"id": "A", "text": "Recall (Sensitivity): minimizing False Negatives.", "is_distractor": False},
            {"id": "B", "text": "Precision: minimizing False Positives.", "is_distractor": True},
            {"id": "C", "text": "Specificity: maximizing True Negative rate.", "is_distractor": True},
            {"id": "D", "text": "Raw accuracy across all patients.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Recall is $\\frac{\\text{TP}}{\\text{TP} + \\text{FN}}$. When missing positive cases (False Negatives) is critical, maximizing Recall ensures almost all actual positives are flagged.",
        "distractor_explanations": {
            "B": "Precision is prioritized when False Positives are costly (e.g., spam detection).",
            "C": "Specificity focuses on correctly identifying healthy patients (True Negatives).",
            "D": "Accuracy is misleading in imbalanced datasets (e.g., 99% benign cases)."
        },
        "a": 1.35,
        "b": -0.80,
        "point_biserial": 0.41
    },
    {
        "skill_code": "ML_EVALUATION",
        "stem": "What is the formula for the $F_1$ Score in binary classification?",
        "options": [
            {"id": "A", "text": "$2 \\times \\frac{\\text{Precision} \\times \\text{Recall}}{\\text{Precision} + \\text{Recall}}$ (Harmonic Mean)", "is_distractor": False},
            {"id": "B", "text": "$\\frac{\\text{Precision} + \\text{Recall}}{2}$ (Arithmetic Mean)", "is_distractor": True},
            {"id": "C", "text": "$\\sqrt{\\text{Precision} \\times \\text{Recall}}$ (Geometric Mean)", "is_distractor": True},
            {"id": "D", "text": "$\\frac{\\text{TP} + \\text{TN}}{\\text{TP} + \\text{TN} + \\text{FP} + \\text{FN}}$", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "The F1 score is the harmonic mean of precision and recall. It severely penalizes extreme disparities (if precision or recall is near zero, F1 drops close to zero).",
        "distractor_explanations": {
            "B": "Arithmetic mean does not penalize lopsided metrics (e.g., Precision=1.0, Recall=0.0 would give 0.5).",
            "C": "Geometric mean is used in G-measure, not standard F1.",
            "D": "Defines Accuracy."
        },
        "a": 1.40,
        "b": -0.30,
        "point_biserial": 0.43
    },
    {
        "skill_code": "ML_EVALUATION",
        "stem": "What does an Area Under the ROC Curve (ROC-AUC) value of 0.5 indicate about a binary classification model?",
        "options": [
            {"id": "A", "text": "The model has no discriminative ability; its predictions are no better than random guessing.", "is_distractor": False},
            {"id": "B", "text": "The model makes perfect predictions on 50% of the test samples.", "is_distractor": True},
            {"id": "C", "text": "The model has an accuracy of exactly 50%.", "is_distractor": True},
            {"id": "D", "text": "The model has inverted predictions and should be inverted to achieve 1.0.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "The ROC curve plots TPR vs. FPR across all classification thresholds. A diagonal line from (0,0) to (1,1) has an area of 0.5, representing chance performance.",
        "distractor_explanations": {
            "B": "ROC-AUC evaluates ranking across all thresholds, not sample subsets.",
            "C": "Accuracy depends on the choice of threshold and class priors; ROC-AUC is threshold-independent.",
            "D": "An AUC of 0.0 represents a completely inverted classifier, not 0.5."
        },
        "a": 1.45,
        "b": 0.00,
        "point_biserial": 0.45
    },
    {
        "skill_code": "ML_EVALUATION",
        "stem": "Why is **Stratified K-Fold Cross Validation** preferred over standard K-Fold Cross Validation for classification with imbalanced classes?",
        "options": [
            {"id": "A", "text": "It preserves the percentage of samples for each class in every fold, preventing folds with zero minority class instances.", "is_distractor": False},
            {"id": "B", "text": "It trains K models concurrently on multiple GPU cores to speed up training.", "is_distractor": True},
            {"id": "C", "text": "It eliminates the need for a separate validation or test split.", "is_distractor": True},
            {"id": "D", "text": "It automatically balances class weights using SMOTE.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Stratification guarantees that each fold represents the true class distribution of the overall dataset, yielding stable and representative performance estimates for rare classes.",
        "distractor_explanations": {
            "B": "Parallel training can be used with either method; stratification is about split sampling.",
            "C": "A held-out test split is still best practice for final evaluation.",
            "D": "SMOTE is an oversampling technique; stratified k-fold is an evaluation partitioning strategy."
        },
        "a": 1.50,
        "b": 0.40,
        "point_biserial": 0.47
    },
    {
        "skill_code": "ML_EVALUATION",
        "stem": "In evaluating binary classifiers on severe class imbalance (e.g., 99.9% negative, 0.1% positive like fraud detection), why is the **Precision-Recall (PR) Curve** often more informative than the **ROC Curve**?",
        "options": [
            {"id": "A", "text": "The ROC curve uses False Positive Rate (FP / TN), which stays deceptively near zero due to huge TN counts; the PR curve focuses exclusively on positive instances without being dominated by TN.", "is_distractor": False},
            {"id": "B", "text": "The PR curve can only be plotted if accuracy is above 90%.", "is_distractor": True},
            {"id": "C", "text": "ROC curves cannot handle probabilities between 0.0 and 1.0.", "is_distractor": True},
            {"id": "D", "text": "The PR curve is immune to changes in classification threshold.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "When TN is enormous, FPR changes very little even with thousands of false alarms, inflating the ROC-AUC. Precision directly reflects false positives relative to true positives.",
        "distractor_explanations": {
            "B": "PR curves can be computed regardless of accuracy.",
            "C": "ROC curves are explicitly built on predicted probabilities.",
            "D": "PR curves, like ROC curves, vary dynamically across classification thresholds."
        },
        "a": 1.65,
        "b": 1.20,
        "point_biserial": 0.52
    },

    # =========================================================================
    # TOPIC 2: Neural Foundations (15 items)
    # =========================================================================
    # --- ML_NEURAL_NETS (15 items) ---
    {
        "skill_code": "ML_NEURAL_NETS",
        "stem": "What was the critical limitation of the single-layer Perceptron demonstrated by Minsky and Papert in 1969?",
        "options": [
            {"id": "A", "text": "It cannot solve non-linearly separable problems, such as the XOR logical function.", "is_distractor": False},
            {"id": "B", "text": "It could not be trained using gradient descent.", "is_distractor": True},
            {"id": "C", "text": "It required more than 100 hidden layers to converge.", "is_distractor": True},
            {"id": "D", "text": "It could only process positive floating-point inputs.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "A single linear hyperplane cannot separate the XOR truth table inputs (0,1) and (1,0) from (0,0) and (1,1). Multi-layer networks with non-linear activations were required.",
        "distractor_explanations": {
            "B": "The Rosenblatt Perceptron learning rule successfully updated weights for linearly separable data.",
            "C": "Perceptrons had zero hidden layers.",
            "D": "Inputs can take any real value in $\\mathbb{R}^d$."
        },
        "a": 1.30,
        "b": -1.30,
        "point_biserial": 0.39
    },
    {
        "skill_code": "ML_NEURAL_NETS",
        "stem": "What is the primary function of non-linear activation functions (e.g., ReLU, GeLU) in deep neural networks?",
        "options": [
            {"id": "A", "text": "To enable the network to approximate arbitrary non-linear functions (Universal Approximation Theorem).", "is_distractor": False},
            {"id": "B", "text": "To keep all layer weights strictly bounded between 0 and 1.", "is_distractor": True},
            {"id": "C", "text": "To accelerate data loading from disk into GPU memory.", "is_distractor": True},
            {"id": "D", "text": "To enforce orthogonal weight matrices during backpropagation.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Without non-linear activations, composing multiple linear layers $W_2(W_1 x + b_1) + b_2$ simply collapses mathematically into a single linear transformation $W' x + b'$.",
        "distractor_explanations": {
            "B": "ReLU is unbounded for positive inputs ($f(x) = \\max(0, x)$).",
            "C": "Activation functions are math operations in computation graphs, not disk I/O.",
            "D": "Orthogonality is enforced via regularization or specific initialization, not activation functions."
        },
        "a": 1.35,
        "b": -0.90,
        "point_biserial": 0.41
    },
    {
        "skill_code": "ML_NEURAL_NETS",
        "stem": "What is the **vanishing gradient problem** commonly encountered in deep networks with Sigmoid or Tanh activations?",
        "options": [
            {"id": "A", "text": "During backpropagation, gradients shrink exponentially as they are multiplied across layers because derivatives of Sigmoid/Tanh are bounded ($< 0.25$), preventing early layers from learning.", "is_distractor": False},
            {"id": "B", "text": "Loss values become NaN due to numerical underflow in floating point arithmetic.", "is_distractor": True},
            {"id": "C", "text": "Weights in the output layer grow infinitely large and overflow memory.", "is_distractor": True},
            {"id": "D", "text": "The learning rate decays to zero after the first epoch.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Because $\\sigma'(z) \\le 0.25$, multiplying many such values via the chain rule causes $\\frac{\\partial L}{\\partial W_1} \\to 0$ in deep architectures.",
        "distractor_explanations": {
            "B": "NaN from underflow/overflow is typical of exploding gradients or divide-by-zero.",
            "C": "Exploding gradients cause weights to grow unbounded.",
            "D": "Learning rate schedules are configured externally by the practitioner."
        },
        "a": 1.45,
        "b": -0.30,
        "point_biserial": 0.44
    },
    {
        "skill_code": "ML_NEURAL_NETS",
        "stem": "Why did the Rectified Linear Unit (ReLU: $f(x) = \\max(0, x)$) largely replace Sigmoid in hidden layers of deep networks?",
        "options": [
            {"id": "A", "text": "Its derivative is 1 for all positive inputs, preventing gradient saturation and drastically speeding up convergence.", "is_distractor": False},
            {"id": "B", "text": "It is bounded between -1 and +1, preventing weight explosion.", "is_distractor": True},
            {"id": "C", "text": "It is infinitely differentiable at all real numbers including $x=0$.", "is_distractor": True},
            {"id": "D", "text": "It guarantees that no neuron in the network will ever output zero.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "For $x > 0$, $\\frac{d}{dx}\\text{ReLU}(x) = 1$. Gradients flow backward without attenuation, mitigating the vanishing gradient problem and allowing deep networks to train effectively.",
        "distractor_explanations": {
            "B": "ReLU is unbounded for positive values.",
            "C": "ReLU is not differentiable at $x=0$ (subgradient is used: 0 or 1).",
            "D": "Neurons with negative inputs output 0 (which can lead to 'dying ReLU')."
        },
        "a": 1.40,
        "b": -0.60,
        "point_biserial": 0.43
    },
    {
        "skill_code": "ML_NEURAL_NETS",
        "stem": "What is the **Dying ReLU** problem and how does Leaky ReLU mitigate it?",
        "options": [
            {"id": "A", "text": "If a neuron's net input stays negative, its gradient is permanently 0 and weights never update; Leaky ReLU adds a small non-zero slope (e.g., $0.01x$) for $x < 0$ so gradients still flow.", "is_distractor": False},
            {"id": "B", "text": "The neuron outputs $\\infty$ causing runtime crash; Leaky ReLU caps outputs at 1.", "is_distractor": True},
            {"id": "C", "text": "The learning rate becomes negative; Leaky ReLU inverts weights.", "is_distractor": True},
            {"id": "D", "text": "The weights decay to zero due to L2 regularization; Leaky ReLU disables weight decay.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "When inputs to a ReLU neuron are negative, the gradient is 0. If a large gradient step pulls weights such that the neuron is always inactive, it 'dies'. Leaky ReLU maintains $\\alpha x$ for $x < 0$.",
        "distractor_explanations": {
            "B": "Exploding gradients, not dying ReLU.",
            "C": "Learning rates are hyperparameter constants or schedules.",
            "D": "Weight decay is independent of activation functions."
        },
        "a": 1.50,
        "b": 0.20,
        "point_biserial": 0.46
    },
    {
        "skill_code": "ML_NEURAL_NETS",
        "stem": "What is the mathematical foundation of the **Backpropagation** algorithm in training feedforward neural networks?",
        "options": [
            {"id": "A", "text": "The chain rule of calculus applied to propagate partial derivatives of the loss backwards from output to input.", "is_distractor": False},
            {"id": "B", "text": "Monte Carlo Markov Chain sampling of the weight parameter space.", "is_distractor": True},
            {"id": "C", "text": "Singular Value Decomposition of the layer activation matrices.", "is_distractor": True},
            {"id": "D", "text": "Simulated annealing across discrete loss surfaces.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Backpropagation computes $\\frac{\\partial L}{\\partial W^{(l)}} = \\frac{\\partial L}{\\partial z^{(l)}} \\cdot \\frac{\\partial z^{(l)}}{\\partial W^{(l)}}$ recursively by caching intermediate forward activations and propagating error signals backward.",
        "distractor_explanations": {
            "B": "MCMC is a probabilistic sampling technique, not standard backpropagation.",
            "C": "SVD is matrix factorization used in PCA and dimensionality reduction.",
            "D": "Simulated annealing is a gradient-free global optimization heuristic."
        },
        "a": 1.35,
        "b": -0.80,
        "point_biserial": 0.40
    },
    {
        "skill_code": "ML_NEURAL_NETS",
        "stem": "Why is initializing all neural network weights to **zero** problematic when training with gradient descent and backpropagation?",
        "options": [
            {"id": "A", "text": "All neurons in each hidden layer compute identical activations and receive identical gradients, causing symmetry that prevents individual neurons from learning distinct features.", "is_distractor": False},
            {"id": "B", "text": "Zero weights produce a division by zero error during the forward pass.", "is_distractor": True},
            {"id": "C", "text": "The loss function cannot be evaluated when outputs are zero.", "is_distractor": True},
            {"id": "D", "text": "Zero weights cause the learning rate to be multiplied by zero.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Zero initialization creates complete symmetry across hidden units. Regardless of how many neurons a layer has, all neurons will compute $z = 0 + b$, yield identical outputs, and update identically.",
        "distractor_explanations": {
            "B": "Forward pass is multiplication $W x + b = 0 + b$; no division occurs.",
            "C": "Cross-entropy and MSE can be evaluated when inputs are zero.",
            "D": "Learning rate is not affected by weight values."
        },
        "a": 1.50,
        "b": 0.10,
        "point_biserial": 0.45
    },
    {
        "skill_code": "ML_NEURAL_NETS",
        "stem": "What is the core principle behind **Xavier (Glorot) Initialization**?",
        "options": [
            {"id": "A", "text": "Setting weight variance to $\\frac{2}{n_{\\text{in}} + n_{\\text{out}}}$ to keep activation and gradient variances approximately constant across forward and backward passes.", "is_distractor": False},
            {"id": "B", "text": "Setting all weights to 1.0 to ensure strong initial gradient signals.", "is_distractor": True},
            {"id": "C", "text": "Initializing weights from a uniform distribution between -100 and +100.", "is_distractor": True},
            {"id": "D", "text": "Using PCA on the input batch to determine initial layer weights.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Xavier initialization stabilizes signal variance through linear and tanh layers, preventing activations from vanishing or exploding as depth increases.",
        "distractor_explanations": {
            "B": "Setting weights to 1 causes severe activation explosion in deep networks.",
            "C": "Large values saturate activations immediately into zero-gradient regions.",
            "D": "Xavier is an analytical formula based on layer fan-in and fan-out, not PCA."
        },
        "a": 1.60,
        "b": 0.70,
        "point_biserial": 0.49
    },
    {
        "skill_code": "ML_NEURAL_NETS",
        "stem": "Why is **He (Kaiming) Initialization** specifically recommended over Xavier initialization when using ReLU activations?",
        "options": [
            {"id": "A", "text": "Because ReLU zeros out approximately half of all activations, He initialization uses variance $\\frac{2}{n_{\\text{in}}}$ to compensate for the lost variance.", "is_distractor": False},
            {"id": "B", "text": "Because He initialization eliminates negative weights completely.", "is_distractor": True},
            {"id": "C", "text": "Because Xavier initialization is mathematically incompatible with GPUs.", "is_distractor": True},
            {"id": "D", "text": "Because He initialization enforces L1 weight sparsity during forward pass.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Since ReLU zeroes out half the distribution, the expected variance of activations is cut by half. He initialization multiplies the variance by 2 ($\text{Var}(W) = 2/n_{\text{in}}$) to maintain constant signal variance.",
        "distractor_explanations": {
            "B": "He initialization samples from a zero-mean normal or uniform distribution (has negative weights).",
            "C": "Both are simple random sampling routines executed identically on CPU/GPU.",
            "D": "It is an initial state generator, not a sparsity regularizer."
        },
        "a": 1.65,
        "b": 1.10,
        "point_biserial": 0.52
    },
    {
        "skill_code": "ML_NEURAL_NETS",
        "stem": "How does **Dropout** act as a regularizer during neural network training?",
        "options": [
            {"id": "A", "text": "By randomly setting a fraction $p$ of neuron activations to zero on each forward pass, preventing neurons from co-adapting and approximating an ensemble of sub-networks.", "is_distractor": False},
            {"id": "B", "text": "By permanently deleting low-magnitude weight connections from the model graph.", "is_distractor": True},
            {"id": "C", "text": "By dropping corrupted input images during batch loading.", "is_distractor": True},
            {"id": "D", "text": "By reducing the learning rate whenever validation error increases.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "During training, dropout randomly zeroes out units with probability $p$. This forces the network to learn robust, distributed representations rather than relying on specific co-adapted features.",
        "distractor_explanations": {
            "B": "Permanent pruning of small weights is model compression/pruning, not training dropout.",
            "C": "Dropout operates on hidden activations, not dropping data samples.",
            "D": "Describes ReduceLROnPlateau learning rate scheduling."
        },
        "a": 1.45,
        "b": -0.10,
        "point_biserial": 0.44
    },
    {
        "skill_code": "ML_NEURAL_NETS",
        "stem": "What is the operational difference in how **Dropout** behaves during training versus inference (testing)?",
        "options": [
            {"id": "A", "text": "During training, neurons are randomly dropped and remaining activations are scaled by $\\frac{1}{1-p}$ (inverted dropout); during inference, dropout is disabled and all neurons remain active.", "is_distractor": False},
            {"id": "B", "text": "Dropout is only active during inference to generate probabilistic ensembles.", "is_distractor": True},
            {"id": "C", "text": "During inference, dropout drops 50% more units to speed up latency.", "is_distractor": True},
            {"id": "D", "text": "Dropout behavior is identical in both training and inference modes.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Inverted dropout scales activations by $\\frac{1}{1-p}$ during training so that during inference, the network can evaluate deterministically without any extra multiplication or unit deactivation.",
        "distractor_explanations": {
            "B": "Standard dropout is disabled at inference (MC Dropout can be used for uncertainty, but that is a specialized technique).",
            "C": "Dropping units at test time degrades deterministic performance.",
            "D": "Dropout must be toggled off at evaluation time (`model.eval()`)."
        },
        "a": 1.55,
        "b": 0.50,
        "point_biserial": 0.48
    },
    {
        "skill_code": "ML_NEURAL_NETS",
        "stem": "What is the primary benefit of **Batch Normalization** in deep neural network training?",
        "options": [
            {"id": "A", "text": "It normalizes layer inputs across the mini-batch to zero mean and unit variance, reducing internal covariate shift and allowing much higher learning rates.", "is_distractor": False},
            {"id": "B", "text": "It eliminates the need for activation functions entirely.", "is_distractor": True},
            {"id": "C", "text": "It compresses the neural network weights into 8-bit integers.", "is_distractor": True},
            {"id": "D", "text": "It ensures that the loss function is strictly concave.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Batch Normalization stabilizes the distribution of layer inputs during training: $\\hat{x} = \\frac{x - \\mu_B}{\\sqrt{\\sigma_B^2 + \\epsilon}}$, followed by learnable scale $\\gamma$ and shift $\\beta$, smoothing the optimization landscape.",
        "distractor_explanations": {
            "B": "Activation functions are still required immediately following or preceding BatchNorm.",
            "C": "Quantization handles integer compression, not batch normalization.",
            "D": "Deep neural net loss surfaces remain non-convex."
        },
        "a": 1.50,
        "b": 0.30,
        "point_biserial": 0.46
    },
    {
        "skill_code": "ML_NEURAL_NETS",
        "stem": "How does the **Adam (Adaptive Moment Estimation)** optimizer compute parameter updates?",
        "options": [
            {"id": "A", "text": "By maintaining exponential moving averages of both past gradients (first moment) and squared gradients (second moment), incorporating bias corrections for initial steps.", "is_distractor": False},
            {"id": "B", "text": "By calculating the exact Hessian matrix of second-order derivatives at every iteration.", "is_distractor": True},
            {"id": "C", "text": "By using simulated annealing with temperature decay.", "is_distractor": True},
            {"id": "D", "text": "By randomly permuting parameter values until loss decreases.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Adam combines the benefits of Momentum ($m_t = \\beta_1 m_{t-1} + (1-\\beta_1)g_t$) and RMSprop ($v_t = \\beta_2 v_{t-1} + (1-\\beta_2)g_t^2$) with bias correction: $\\hat{m}_t / (1-\\beta_1^t)$ and $\\hat{v}_t / (1-\\beta_2^t)$.",
        "distractor_explanations": {
            "B": "Exact Hessian computation (Newton-Raphson) is $O(d^2)$ or $O(d^3)$ and intractable for deep networks.",
            "C": "Adam is a first-order gradient descent variant, not simulated annealing.",
            "D": "Adam follows directional gradient vectors, not random permutation."
        },
        "a": 1.60,
        "b": 0.85,
        "point_biserial": 0.50
    },
    {
        "skill_code": "ML_NEURAL_NETS",
        "stem": "What is the difference between **Stochastic Gradient Descent (SGD)**, **Batch Gradient Descent**, and **Mini-Batch Gradient Descent**?",
        "options": [
            {"id": "A", "text": "Batch GD computes gradients over the entire dataset per step; SGD computes over 1 single sample per step; Mini-Batch GD computes over a small subset (e.g., 32-256 samples).", "is_distractor": False},
            {"id": "B", "text": "Batch GD is faster than SGD on massive datasets.", "is_distractor": True},
            {"id": "C", "text": "SGD never fluctuates, while Batch GD exhibits extreme noise.", "is_distractor": True},
            {"id": "D", "text": "Mini-batch GD cannot be accelerated on GPU hardware.", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Mini-batch balances the vectorization parallelism of GPUs with the noise-induced saddle point escaping properties of stochastic sampling.",
        "distractor_explanations": {
            "B": "Batch GD requires passing through millions of rows before a single weight update, making it far slower than SGD/mini-batch.",
            "C": "SGD fluctuates significantly; Batch GD converges smoothly along gradient contours.",
            "D": "Mini-batch GD is specifically designed to maximize GPU tensor core utilization."
        },
        "a": 1.35,
        "b": -0.70,
        "point_biserial": 0.41
    },
    {
        "skill_code": "ML_NEURAL_NETS",
        "stem": "What is the **Cross-Entropy Loss** formula for a multi-class classification problem with $C$ classes and one-hot encoded ground truth $y$?",
        "options": [
            {"id": "A", "text": "$L = -\\sum_{c=1}^C y_c \\log(\\hat{y}_c)$ where $\\hat{y} = \\text{Softmax}(z)$", "is_distractor": False},
            {"id": "B", "text": "$L = \\sum_{c=1}^C (y_c - \\hat{y}_c)^2$", "is_distractor": True},
            {"id": "C", "text": "$L = \\max(0, 1 - y \\cdot \\hat{y})$", "is_distractor": True},
            {"id": "D", "text": "$L = \\sum_{c=1}^C |y_c - \\hat{y}_c|$", "is_distractor": True}
        ],
        "answer_key": "A",
        "explanation": "Categorical cross-entropy measures the divergence between true one-hot distribution $y$ and predicted softmax probabilities $\\hat{y}$: $-\\sum y_c \\log(\\hat{y}_c) = -\\log(\\hat{y}_{\\text{true}})$.",
        "distractor_explanations": {
            "B": "Sum of squared errors (MSE).",
            "C": "Multi-class hinge loss.",
            "D": "Sum of absolute differences (L1 loss)."
        },
        "a": 1.45,
        "b": 0.00,
        "point_biserial": 0.44
    }
]
