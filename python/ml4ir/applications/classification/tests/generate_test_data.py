# Generating csv test data for classification model in tests.

import string
import csv

from random import seed
from random import randint


CSV_TRAIN_FILE_PATH = "data/csv/train/file_0.csv"
CSV_TEST_FILE_PATH = "data/csv/test/file_0.csv"
CSV_VALIDATION_FILE_PATH = "data/csv/validation/file_0.csv"
COLUMNS_HEADER = ["query_key", "query_text", "domain_id", "user_context", "entity_id"]

VOCABULARY_QUERY = [
    "the", "tragedy", "of", "hamlet", "prince", "denmark", "shakespeare", "homepage", "entire", "play", "act", "i",
    "scene", "elsinore", "a", "platform", "before", "castle", "francisco", "at", "his", "post", "enter", "to", "him",
    "bernardo", "whos", "there", "nay", "answer", "me", "stand", "and", "unfold", "yourself", "long", "live", "king",
    "he", "you", "come", "most", "carefully", "upon", "your", "hour", "tis", "now", "struck", "twelve", "get", "thee",
    "bed", "for", "this", "relief", "much", "thanks", "bitter", "cold", "am", "sick", "heart", "have", "had", "quiet",
    "guard", "not", "mouse", "stirring", "well", "good", "night", "if", "do", "meet", "horatio", "marcellus", "rivals",
    "my", "watch", "bid", "them", "make", "haste", "think", "hear", "ho", "friends", "ground", "liegemen", "dane"
]
VOCABULARY_FEATURE_DOMAIN_ID = [char for char in string.ascii_lowercase.upper()]
VOCABULARY_FEATURE_ENTITY = ["AAA", "BBB", "CCC", "DDD", "EEE", "FFF", "GGG", "HHH"]
VOCABULARY_LABEL = VOCABULARY_FEATURE_ENTITY[:5]

TOTAL_DATA_SIZE = 1000
PARTITION_TRAIN = 0.7
PARTITION_VALIDATION = 0.1
PARTITION_TEST = 0.2


class FeatureGenerator:
    """Helper to randomly generate features based on a given vocabulary list."""
    def __init__(self, vocabulary, max_token_length, sequence_joiner=" "):
        self.__max_token_length = max_token_length
        self.__vocabulary = vocabulary
        self.__vocabulary_length = len(vocabulary) - 1
        self.__sequence_joiner = sequence_joiner

    def generate_feature(self):
        query_tokens = [self.__vocabulary[randint(0, self.__vocabulary_length)]
                        for _ in range(0, randint(1, self.__max_token_length))]
        return self.__sequence_joiner.join(query_tokens)


def generate_csv_test_data():
    """Generates data under classification/tests/csv folder."""
    seed(123)
    feature_query_text_generator = FeatureGenerator(VOCABULARY_QUERY, 7)
    feature_domain_id_generator = FeatureGenerator(VOCABULARY_FEATURE_DOMAIN_ID, 1)
    feature_user_context_generator = FeatureGenerator(VOCABULARY_FEATURE_ENTITY, 20, sequence_joiner=",")
    label_generator = FeatureGenerator(VOCABULARY_LABEL, 1)
    generators = [
        feature_query_text_generator,
        feature_domain_id_generator,
        feature_user_context_generator,
        label_generator
    ]

    for (path, number_rows) in [(CSV_TRAIN_FILE_PATH, TOTAL_DATA_SIZE * PARTITION_TRAIN),
                                (CSV_TEST_FILE_PATH, TOTAL_DATA_SIZE * PARTITION_VALIDATION),
                                (CSV_VALIDATION_FILE_PATH, TOTAL_DATA_SIZE * PARTITION_TEST)]:
        rows = [COLUMNS_HEADER] + [['query_id_' + str(idx)] + [g.generate_feature() for g in generators]
                                   for idx in range(0, int(number_rows))]
        with open(path, 'w', newline='') as file:
            writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC)
            writer.writerows(rows)


def main():
    generate_csv_test_data()
    return


if __name__ == "__main__":
    """
    Generates data under classification/tests folder used to train and assess classification model in tests.
    """
    main()
