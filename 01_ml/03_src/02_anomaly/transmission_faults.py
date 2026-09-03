def remove_record(df, row_index):
    """
    Remove one record to simulate a missing transmission.
    """

    removed_record = df.loc[row_index].copy()

    df = df.drop(index=row_index).reset_index(drop=True)

    return df, removed_record

# Removed row metadata ke liye preserve rahegi.

"""
Before:
        June 21
        June 22
        June 23
        June 24

After:
        June 21
        June 22
        June 24
"""