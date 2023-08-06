
def tpm(counts, lengths):
    """
    Performs TPM normalization on a pandas DataFrame of count data

    Args:
    counts (pandas.DataFrame): DataFrame containing raw count data for each gene in each sample
    lengths (pandas.Series): Series containing gene lengths

    Returns:
    pandas.DataFrame: DataFrame containing TPM-normalized expression values for each gene in each sample
    """

    # Normalize raw read counts by gene length
    norm_counts = counts.divide(lengths, axis=0)

    # Calculate sum of normalized read counts for each sample
    sum_norm_counts = norm_counts.sum(axis=0)

    # Calculate TPM values
    tpm_df = norm_counts.divide(sum_norm_counts, axis=1) * 1e6

    return tpm_df


def cpm_norm(counts):
    """
    Performs CPM normalization on a pandas DataFrame of count data

    Args:
    counts (pandas.DataFrame): DataFrame containing raw count data for each gene in each sample

    Returns:
    pandas.DataFrame: DataFrame containing CPM-normalized expression values for each gene in each sample
    """

    # Compute the total count for each sample
    total_counts = counts.sum(axis='rows')

    # Divide counts by the total count for each sample, and scale to 1M
    cpm_df = counts.divide(total_counts, axis='columns') * 1e6

    return cpm_df


def rpkm(raw_data, lengths):
    """
    Performs RPKM normalization on a pandas DataFrame of count data

    Args:
    counts (pandas.DataFrame): DataFrame containing raw count data for each gene in each sample
    lengths (pandas.Series): Series containing gene lengths

    Returns:
    pandas.DataFrame: DataFrame containing RPKM-normalized expression values for each gene in each sample
    """
    # Normalized read counts for each sample
    norm_counts = raw_data.divide(lengths, axis=0)

    # Calculate sum of read counts for each sample
    sum_counts = 1 / raw_data.sum(axis=0)

    # Multiply length by the sum of read counts
    sum_norm_counts = norm_counts.multiply(sum_counts, axis=1)

    # Calculate RPKM values
    rpkm_df = sum_norm_counts * 1e9

    return rpkm_df


def tpm_from_rpkm(rpkm):
    """
    Performs TPM normalization on a pandas DataFrame of RPKM-normalized data

    Args:
    rpkm (pandas.DataFrame): Dataframe containing RPKM-normalized expression values for each gene in each sample

    Returns:
    pandas.DataFrame: DataFrame containing TPM-normalized expression values for each gene in each sample
    """
    # Sum of normalized values for each sample
    sum_counts = rpkm.sum(axis=0)

    # Calculate TPM values
    tpm_df = rpkm.divide(sum_counts) * 1e6

    return tpm_df

