import glob
import os
from typing import Optional
from logging import Logger

import tensorflow as tf
from ml4ir.config.keys import DataFormatKey, DataSplitKey
from ml4ir.data import csv_reader
from ml4ir.data import tfrecord_reader
from ml4ir.config.features import FeatureConfig


class RankingDataset:
    def __init__(
        self,
        data_dir: str,
        data_format: str,
        feature_config: FeatureConfig,
        max_num_records: int,
        loss_key: str,
        scoring_key: str,
        batch_size: int = 128,
        train_pcent_split: float = 0.8,
        val_pcent_split: float = -1,
        test_pcent_split: float = -1,
        use_part_files: bool = False,
        parse_tfrecord: bool = True,
        logger: Logger = None,
    ):
        self.feature_config = feature_config
        self.max_num_records = max_num_records
        self.data_dir: str = data_dir
        self.data_format: str = data_format
        self.loss_key: str = loss_key
        self.scoring_key: str = scoring_key
        self.batch_size: int = batch_size
        self.logger = logger

        self.train_pcent_split: float = train_pcent_split
        self.val_pcent_split: float = val_pcent_split
        self.test_pcent_split: float = test_pcent_split
        self.use_part_files: bool = use_part_files

        self.train: Optional[tf.data.TFRecordDataset] = None
        self.validation: Optional[tf.data.TFRecordDataset] = None
        self.test: Optional[tf.data.TFRecordDataset] = None
        self.create_dataset(parse_tfrecord)

    def create_dataset(self, parse_tfrecord=True):
        """
        Loads and creates train, validation and test datasets
        """
        to_split = len(glob.glob(os.path.join(self.data_dir, DataSplitKey.TEST))) == 0

        if self.data_format == DataFormatKey.CSV:
            data_reader = csv_reader
        elif self.data_format == DataFormatKey.TFRECORD:
            data_reader = tfrecord_reader
        else:
            raise NotImplementedError

        if to_split:
            """
            If the data is stored as
            data_dir
            │
            ├── data_file
            ├── data_file
            ├── ...
                              └── data_file
            """
            raise NotImplementedError

        else:
            """
            If the data is stored as
            data_dir
            │
            ├── train
            │   ├── data_file
            │   ├── data_file
            │   ├── ...
                              │   └── data_file
            ├── validation
            │   ├── data_file
            │   ├── data_file
            │   ├── ...
                              │   └── data_file
            └── test
                ├── data_file
                ├── data_file
                ├── ...
                                              └── data_file
            """
            self.train = data_reader.read(
                data_dir=os.path.join(self.data_dir, DataSplitKey.TRAIN),
                feature_config=self.feature_config,
                tfrecord_dir=os.path.join(self.data_dir, "tfrecord", DataSplitKey.TRAIN),
                max_num_records=self.max_num_records,
                batch_size=self.batch_size,
                use_part_files=self.use_part_files,
                parse_tfrecord=parse_tfrecord,
                logger=self.logger,
            )
            self.validation = data_reader.read(
                data_dir=os.path.join(self.data_dir, DataSplitKey.VALIDATION),
                feature_config=self.feature_config,
                tfrecord_dir=os.path.join(self.data_dir, "tfrecord", DataSplitKey.VALIDATION),
                max_num_records=self.max_num_records,
                batch_size=self.batch_size,
                use_part_files=self.use_part_files,
                parse_tfrecord=parse_tfrecord,
                logger=self.logger,
            )
            self.test = data_reader.read(
                data_dir=os.path.join(self.data_dir, DataSplitKey.TEST),
                feature_config=self.feature_config,
                tfrecord_dir=os.path.join(self.data_dir, "tfrecord", DataSplitKey.TEST),
                max_num_records=self.max_num_records,
                batch_size=self.batch_size,
                use_part_files=self.use_part_files,
                parse_tfrecord=parse_tfrecord,
                logger=self.logger,
            )

    def balance_classes(self):
        """
        Balance class labels in the train dataset

        NOTE: This step should ideally be done as a preprocessing step
        """
        raise NotImplementedError
