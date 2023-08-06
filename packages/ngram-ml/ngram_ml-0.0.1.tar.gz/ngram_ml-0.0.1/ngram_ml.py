import numpy as np
from itertools import product


class NGramMLEstimator:
    """Maximum Likelihood Estimation for n-grams."""

    def __init__(
        self, sentences: list[list[str, ...]], n_grams: int, label_smoothing: int = 1
    ) -> None:
        """

        :param sentences:
        :type sentences:
        :param n_grams:
        :type n_grams:
        :param label_smoothing:
        :type label_smoothing:
        """
        self.sentences = [
            sentence if sentence[0] == "<S>" else ["<S>"] + sentence + ["</S>"]
            for sentence in sentences
        ]
        self.n_grams = n_grams
        self.label_smoothing = label_smoothing
        self.word_to_idx, self.idx_to_word = NGramMLEstimator.get_word_idx_mappers(
            self.sentences
        )  # label to idx is same as label is always a single word
        self.pre_seq_to_idx, self.idx_to_pre_seq = self._get_pre_seq_to_idx_mappers()

        self.idx_sentences = NGramMLEstimator.map_words_to_idx(
            self.sentences, self.word_to_idx
        )
        self.N = self.get_cooccurence_counts()
        self.P = self.N / self.N.sum(axis=1, keepdims=True)

    @staticmethod
    def get_word_idx_mappers(
        sentences: list[list[str, ...]]
    ) -> tuple[dict[str, int], dict[int, str]]:
        """Generate a mapping from word to index.

        :param sentences: Tokenized sentences
        :type sentences: list[list[str,...]]
        :return: Mapping from word to index
        :rtype: tuple[dict[str, int],dict[int, str]]
        """
        word_to_idx = {}
        word_to_idx["<UNK>"] = 0
        word_to_idx["<S>"] = 1
        word_to_idx["</S>"] = 2

        unique_words = set([word for sentence in sentences for word in sentence])
        for i, word in enumerate(
            [word for word in unique_words if word not in ["<UNK>", "<S>", "</S>"]]
        ):
            word_to_idx[word] = i + 3

        idx_to_word = {v: k for k, v in word_to_idx.items()}
        return word_to_idx, idx_to_word

    @staticmethod
    def map_words_to_idx(
        sentences: list[list[str, ...]], word_to_idx: dict[str, int]
    ) -> list[list[int, ...]]:
        """Map words to indices.

        :param sentences: Tokenized sentences
        :type sentences: list[list[str,...]]
        :param word_to_idx: Mapping from word to index
        :type word_to_idx: dict[str, int]
        :return: Sentences with words replaced by indices
        :rtype: list[list[int,...]]
        """
        return [
            [
                word_to_idx[word]
                if word in word_to_idx.keys()
                else word_to_idx["<UNK>"]
                for word in sentence
            ]
            for sentence in sentences
        ]

    def _get_pre_seq_to_idx_mappers(self) -> tuple[dict[tuple[int, ...], int], dict[int, tuple[int, ...]]]:
        """

        :return: Mapping from preceeding sequence to index and vice versa
        :rtype: tuple[dict[tuple[int, ...], int], dict[int, tuple[int, ...]]]
        """
        preceeding_seq = list(
            product(self.word_to_idx.values(), repeat=self.n_grams - 1)
        )
        pre_seq_to_idx = {pre_seq: idx for idx, pre_seq in enumerate(preceeding_seq)}
        idx_to_pre_seq = {idx: pre_seq for idx, pre_seq in enumerate(preceeding_seq)}
        return pre_seq_to_idx, idx_to_pre_seq

    def get_cooccurence_counts(self) -> np.ndarray:
        """Get cooccurence counts for n-grams in sentences.

        :param sentences: Tokenized sentences
        :type sentences: list[list[str,...]]
        :param n_grams: Number of n-grams
        :type n_grams: int
        :return: Counts of pre_seq n-1 words and label n-th word shape = (n_unique_words**(n_grams - 1), n_unique_words)
        :rtype: np.ndarray
        """
        N = (
            np.zeros((len(self.pre_seq_to_idx), len(self.word_to_idx)), dtype=np.int32)
            + self.label_smoothing
        )

        for idx_sentence in self.idx_sentences:
            for i in range(len(idx_sentence) - self.n_grams + 1):
                pre_seq_idx = tuple(idx_sentence[i : i + self.n_grams - 1])
                label_idx = idx_sentence[i + self.n_grams - 1]
                N[self.pre_seq_to_idx[pre_seq_idx], label_idx] += 1

        return N

    def calculate_cross_entropy(
        self, sentences: list[list[str, ...]]
    ) -> tuple[float, int, float]:
        """Cross-entropy of the given sentence

        :param sentence: Tokenized sentence
        :type sentence: list[str,...]
        :return: Cross-entropy of sentence
        :rtype: float
        """
        sentences = [
            sentence if sentence[0] != "<S>" else ["<S>"] + sentence + ["</S>"]
            for sentence in sentences
        ]
        sentences_idx = NGramMLEstimator.map_words_to_idx(sentences, self.word_to_idx)

        log_prob = 0
        counter = 0
        for sentence_idx in sentences_idx:
            for i in range(len(sentence_idx) - self.n_grams + 1):
                pre_seq_idx = tuple(sentence_idx[i : i + self.n_grams - 1])
                label_idx = sentence_idx[i + self.n_grams - 1]
                log_prob += np.log(self.P[self.pre_seq_to_idx[pre_seq_idx], label_idx])
                counter += 1

        return -log_prob, counter, -log_prob / counter

    def generate_sentence(
        self, max_n_words: int, initial_pre_seq: tuple[str, ...] = None
    ) -> list[str]:
        """Generate a sentence of n_words.

        :param max_n_words: Number of words in sentence
        :type n_words: int
        :return: Sentence
        :rtype: list[str]
        """
        sentence = []
        pre_seq = (
            tuple([self.word_to_idx["<S>"]] * (self.n_grams - 1))
            if initial_pre_seq is None
            else initial_pre_seq
        )
        for i in range(max_n_words):
            label_idx = np.random.choice(
                len(self.word_to_idx), p=self.P[self.pre_seq_to_idx[pre_seq]]
            )
            label = self.idx_to_word[label_idx]
            if label == "</S>":
                break
            sentence.append(label)
            pre_seq = pre_seq[1:] + (label_idx,)
        return sentence

    def generate_most_probable_sentence(
        self, max_n_words: int, initial_pre_seq: tuple[str, ...] = None
    ) -> list[str]:
        """Generate a sentence of n_words.

        :param max_n_words: Number of words in sentence
        :type n_words: int
        :return: Sentence
        :rtype: list[str]
        """
        sentence = []
        pre_seq = (
            tuple([self.word_to_idx["<S>"]] * (self.n_grams - 1))
            if initial_pre_seq is None
            else initial_pre_seq
        )
        for i in range(max_n_words):
            label_idx = np.argmax(self.P[self.pre_seq_to_idx[pre_seq]])
            label = self.idx_to_word[label_idx]
            if label == "</S>":
                break
            sentence.append(label)
            pre_seq = pre_seq[1:] + (label_idx,)
        return sentence
