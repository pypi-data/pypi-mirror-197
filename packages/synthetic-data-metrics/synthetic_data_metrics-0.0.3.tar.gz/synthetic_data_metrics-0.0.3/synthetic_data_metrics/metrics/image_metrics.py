from numpy import expand_dims
from numpy import log
from numpy import mean
from numpy import std
from numpy import exp
import numpy as np
from sklearn.metrics import jaccard_score


def calc_inception_score(softmax_list,  eps=1e-16) -> float:
    """Calculates the Inception Score.

    This function calculates the score (KL divergence between the label
    distribution and marginal distribution) for each image in images.

    Args:
        - features (array) : list of Array of features to evaluate.
        list of length splits containing array size [n_samples/n_splits, 1000]
        - eps (#TODO) : #TODO.

    Returns:
        The mean and standard deviation of the scores.

    Raises:
        Checks images is a nested array of values in the range [0,255].
    """

    # TODO: add assertions here

    scores = []

    for split_data in softmax_list:
        # average across all pieces of data
        p_y = expand_dims(split_data.mean(axis=0), 0)
        # calculate KL divergence using log probabilities
        kl_d = split_data * (log(split_data + eps) - log(p_y + eps))
        # sum over classes
        sum_kl_d = kl_d.sum(axis=1)
        # average over images
        avg_kl_d = mean(sum_kl_d)
        # undo the log
        score = exp(avg_kl_d)
        print(score)
        # store

        scores.append(score)

    # average across images
    is_avg, is_std = mean(scores), std(scores)

    return is_avg, is_std


def calc_fid():
    return None


def calc_dim_reduced_iou(dataset1_2PC, dataset2_2PC):
    """Calculates the Dimensionality reduced IoU Score.

    This function calculates the IoU Score between given 2d numpy array
    assuming them as muliclass and apply weighted average.

    Args:
        - features (array) : list of Array of features to evaluate.
    Returns:
        The IoU score.

    Raises:
        Checks number and size of images in each dataset are same .
    """
    dataset1_2PC_flatten = np.round(dataset1_2PC.flatten())
    dataset2_2PC_flatten = np.round(dataset2_2PC.flatten())
    j_score = jaccard_score(dataset1_2PC_flatten, dataset2_2PC_flatten,
                            average='weighted')
    return j_score


def calc_dim_reduced_dice(dataset1_2PC, dataset2_2PC):
    """Calculates the Dimensionality reduced Dice Score.

    This function calculates the Dice Score between given 2d numpy array
    assuming them as muliclass and apply weighted average.

    Args:
        - features (array) : list of Array of features to evaluate.
    Returns:
        The Dice score.

    Raises:
        Checks number and size of images in each dataset are same .
    """
    j_score = calc_dim_reduced_iou(dataset1_2PC, dataset2_2PC)
    dice_score = (2*j_score)/(1+j_score)
    return dice_score
