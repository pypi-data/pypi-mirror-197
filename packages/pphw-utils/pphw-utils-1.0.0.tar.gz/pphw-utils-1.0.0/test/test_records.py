import unittest

from pphw_utils.records import split_to_batches, MAX_SIZE_RECORD, MAX_SIZE_BATCH, MAX_NUM_RECORDS_IN_BATCH


class TestSplittingRecordsToBatches(unittest.TestCase):

    def test_invalid_records(self):
        records = 'aa'
        # Test a non-array input raises ValueError
        with self.assertRaises(ValueError):
            split_to_batches(records)

    def test_valid_records(self):
        records = ['aa', 'bb', 'cc']
        # Test a set of valid records is batched successfully and order preserved
        self.assertEqual(split_to_batches(records), [['aa', 'bb', 'cc']])

    def test_max_record_size(self):
        too_large_record = 'a' * MAX_SIZE_RECORD + 'a'
        records = [too_large_record]
        # Test a too large record is discarded
        self.assertEqual(split_to_batches(records), [[]])

    def test_max_batch_size(self):
        nr_max_size_records = MAX_SIZE_BATCH // MAX_SIZE_RECORD
        records = ['a' * MAX_SIZE_RECORD for _ in range(nr_max_size_records + 1)]  # Add +1 to enforce a second batch
        # Test a second batch is created when MAX_SIZE_BATCH is reached
        self.assertEqual(len(split_to_batches(records)), 2)

    def test_max_num_records_in_batch(self):
        records = ['a' for _ in range(MAX_NUM_RECORDS_IN_BATCH + 1)]  # Add +1 to enforce a second batch
        # Test a second batch is created when MAX_NUM_RECORDS_IN_BATCH is reached
        self.assertEqual(len(split_to_batches(records)), 2)
