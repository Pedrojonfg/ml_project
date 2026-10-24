# Course notes index

Source: `course-notes.pdf` — *Machine Learning Lecture Notes*, Nacho Molina, IE University, Bachelor in Applied Mathematics, 2025–2026 (111 PDF pages).

**Page offset:** PDF page = printed page + 3. Use PDF pages with the Read tool's `pages` parameter. Printed pages below.

## Contents

### Part 1 — Foundations

| Ch. | Topic | Printed pages | Key sections |
|-----|-------|---------------|--------------|
| 1 | Introduction & the learning problem | 2–11 | Definitions (Bishop, Mitchell), paradigms |
| 2 | Linear regression | 12–23 | Assumptions, MSE, normal equations, gradient descent, SGD, metrics, probabilistic view |
| 3 | Logistic regression | 24–35 | Sigmoid, cross-entropy, GD, probabilistic interpretation, metrics, extensions |
| 4 | Dimensionality reduction & clustering | 36–49 | PCA (4.2, p.37), k-means (4.3, p.45) |
| 5 | Performance, generalization, regularization | 50–54 | Over/underfitting, bias–variance (5.2), regularization (5.3) |

### Part 2 — Nonlinear and non-parametric models

| Ch. | Topic | Printed pages | Key sections |
|-----|-------|---------------|--------------|
| 6 | Kernel methods | 56–69 | Ridge dual (6.2), kernel trick (6.3), geometry, kernel classification, kernel PCA |
| 7 | Neural networks | 70–84 | Components, activations, universal approximation, backprop, regression/classification, autoencoders, practical training (7.8) |
| 8 | Tree-based methods | 85–107 | Decision trees, tree regularization, bagging & random forests, boosting & gradient boosting, practical guidance (8.6) |

Bibliography: printed p.108.

## Likely NOT covered, or only thin

Not verified exhaustively — always `grep` the notes before assuming (see SKILL.md). Treat as `outside-notes` if absent:

- Cross-validation schemes in depth, nested CV, hyperparameter search strategies
- Data preprocessing in depth: imputation, encoding, outlier handling, feature engineering
- Class imbalance (resampling, cost-sensitive learning), calibration
- Evaluation beyond the listed metrics: ROC/PR subtleties, statistical significance tests
- Lasso/elastic net details and sparsity theory
- Support vector machines (margin, hinge loss, duality) beyond kernel classification
- Probabilistic latent models (GMM, EM), other clustering (hierarchical, DBSCAN)
- Advanced optimizers (momentum, Adam, schedules), batch/layer normalization
- Time series, sequence models, CNNs/RNNs/transformers
- Interpretability methods (SHAP, partial dependence) beyond variable importance
