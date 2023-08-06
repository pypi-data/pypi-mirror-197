from typing import List

MAX_SIZE_RECORD = 1024 ** 2  # 1MB
MAX_SIZE_BATCH = (1024 ** 2) * 5  # 5MB
MAX_NUM_RECORDS_IN_BATCH = 500


def split_to_batches(records: List[str]) -> List[List[str]]:
    if not isinstance(records, list) and not isinstance(records, tuple):
        raise ValueError("Input must be an array (list or tuple supported).")

    output = []

    batch = []
    batch_size = 0

    for r in records:
        record_size = _get_record_size(r)

        # Drop too large records
        if record_size > MAX_SIZE_RECORD:
            continue

        # Check if record would break batch size limit, if so, make new batch
        if len(batch) == MAX_NUM_RECORDS_IN_BATCH or (batch_size + record_size) > MAX_SIZE_BATCH:
            output.append(batch)
            batch = []
            batch_size = 0

        # Update batch
        batch.append(r)
        batch_size += record_size

    # Add final batch to output
    output.append(batch)
    return output


def _get_record_size(record: str):
    """
    Depending on encoding, this may not account for all strings (eg. multi-byte encodings with Byte Order Mark).
    Assumed input is always utf-8 encoded.
    If this changes, please modify this function respectively.
    """
    return len(record.encode('utf-8'))
