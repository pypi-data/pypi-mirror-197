from torch.utils.data import Dataset
import torch
from ngram_ml import NGramMLEstimator


class NGramDataset(Dataset):
    """
    A dataset for ngrams.
    """

    def __init__(self, sentences: list[list[str]], n_grams: int):
        """

        :param sentences: list of sentences, each sentence is a list of words
        :type sentences: list[list[str]]
        :param n_grams: number of words in the ngram
        :type n_grams: int
        """
        self.n_grams = n_grams
        self.sentences = sentences
        self.word_to_idx, self.idx_to_word = NGramMLEstimator.get_word_idx_mappers(
            self.sentences
        )  # label to idx is same as label is always a single word
        self.n_unique_words = len(self.word_to_idx)

        self.idx_sentences = NGramMLEstimator.map_words_to_idx(
            self.sentences, self.word_to_idx
        )
        self.x, self.y = self.get_dataset_instances()

    def __len__(self) -> int:
        return len(self.x)

    def __getitem__(self, idx: int) -> tuple[torch.tensor, torch.tensor]:
        return self.x[idx], self.y[idx]

    def get_dataset_instances(self) -> tuple[torch.tensor, torch.tensor]:
        """
        Convert the sentences to a dataset of ngrams.

        :return: x and y tensors
        :rtype: tuple[torch.tensor, torch.tensor]
        """

        x, y = [], []
        for sentence_idx in self.idx_sentences:
            for i in range(len(sentence_idx) - self.n_grams + 1):
                x.append(sentence_idx[i : i + self.n_grams - 1])
                y.append(sentence_idx[i + self.n_grams - 1])

        return torch.tensor(x, dtype=torch.int64), torch.tensor(y, dtype=torch.int64)
