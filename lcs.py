def calculate_lcs_length(string1, string2):
    """
    Calculate the length of the
    Longest Common Subsequence (LCS)
    using Dynamic Programming.
    """

    m = len(string1)
    n = len(string2)

    # Create DP table
    dp = [
        [0] * (n + 1)
        for _ in range(m + 1)
    ]

    # Fill the DP table
    for i in range(1, m + 1):

        for j in range(1, n + 1):

            if string1[i - 1] == string2[j - 1]:

                dp[i][j] = (
                    dp[i - 1][j - 1] + 1
                )

            else:

                dp[i][j] = max(
                    dp[i - 1][j],
                    dp[i][j - 1]
                )

    return dp[m][n]


def get_lcs_subsequence(string1, string2):
    """
    Reconstruct the actual Longest Common Subsequence string
    by backtracking through the dynamic programming table.
    """
    m = len(string1)
    n = len(string2)

    dp = [
        [0] * (n + 1)
        for _ in range(m + 1)
    ]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if string1[i - 1] == string2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    # Backtrack to reconstruct subsequence
    subsequence = []
    i, j = m, n
    while i > 0 and j > 0:
        if string1[i - 1] == string2[j - 1]:
            subsequence.append(string1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1

    return "".join(reversed(subsequence))


def calculate_similarity(
    string1,
    string2
):
    """
    Calculate similarity percentage
    using LCS.
    """

    lcs_length = calculate_lcs_length(
        string1,
        string2
    )

    max_length = max(
        len(string1),
        len(string2)
    )

    if max_length == 0:
        return 0.0

    similarity = (
        lcs_length / max_length
    ) * 100

    return similarity


def compare_fingerprints(
    fingerprint1,
    fingerprint2
):
    """
    Compare two fingerprint strings
    and return the LCS length and
    similarity percentage.
    """

    lcs_length = calculate_lcs_length(
        fingerprint1,
        fingerprint2
    )

    similarity = calculate_similarity(
        fingerprint1,
        fingerprint2
    )

    return {
        "lcs_length": lcs_length,
        "similarity": similarity
    }