Package for taking an array of records (utf-8 strings) and splitting it to batches of records, for a delivery system with following limits:
 - max size of a record is 1MB (otherwise discarded)
 - max size of a batch is 5MB (otherwise an additional batch created)
 - max number of records in a batch is 500 (otherwise an additional batch created)

Input is in format: [rec1, rec2, rec3, ..., recN]
Output is ini format: [batch1, batch2, batch3, ..., batchN] where each batch is array of records like input.

To run unittests:  
`python -m unittest -v test/test_records.py`