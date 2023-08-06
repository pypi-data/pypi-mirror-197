# Maximum Likelihood fit for N-grams 
A small library for quickly deriving the Maximum Likelihood estimates for N-grams.

## Installation
```bash
pip install ngram-ml
```

## Usage
```python
from ngram_ml import NGramMLEstimator
```

## Example
```python
mle = NGramMLEstimator(sentences=tokens, n_grams=2, label_smoothing=1)
mle.calculate_cross_entropy(tokens)
mle.calculate_cross_entropy([['<S>', 'the', 'cat', 'sat', 'on', 'the', 'mat', '</S>']])

mle.generate_sentence(30, initial_pre_seq= tuple([mle.word_to_idx['pencil']]))
mle.generate_most_probable_sentence(30, initial_pre_seq= tuple([mle.word_to_idx['book']]))

```



