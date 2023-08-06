from sklearn.model_selection import train_test_split


def train_val_test_split(
    X,
    y,
    val_size: int | float = 0.2,
    test_size: int | float = 0.2,
    random_state: int | None = None,
):
    """
    Splits a dataset into training, validation and test sets in a stratified fashion.

    Arguments:
        X: the training set
        y: the trianing labels
        val_size: the size of the validation set (as a percentage or as an absolute number)
        test_size: the size of the test set (as a percentage or as an absolute number)
        random_state: seed for number generation

    Returns:
        (X_train, y_train), (X_val, y_val), (X_test, y_test): splitted data
    """

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, stratify=y, test_size=test_size, random_state=random_state
    )
    X_train, X_val, y_train, y_val = train_test_split(
        X_train, y_train, stratify=y_train, test_size=val_size, random_state=random_state
    )
    return (X_train, y_train), (X_val, y_val), (X_test, y_test)
