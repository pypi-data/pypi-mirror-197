# Author: Matouš Elphick
# License: BSD 3 clause
import numpy as np
import inspect
import pyclesperanto_prototype as cle
from apoc._feature_sets import PredefinedFeatureSet
from scipy import stats, ndimage
from skimage.segmentation import watershed
from sklearn.metrics import jaccard_score
from sklearn.preprocessing import LabelEncoder
from typing import Union, Optional


def mask_img(image, mask):
    """
    Applies binary mask to image.

    Args:
        image: Image to apply binary mask to.
        mask: Binary mask.

    Returns:
        Image with binary mask applied.
    """
    mask[mask > 0] = 1
    return image * mask


def remove_membrane(image_input, mask_input, compactness: int = 0.005, verbose=False):
    """
    This function removes the membrane and generates
    internal mask and applies it to the raw input image
    for the "Complete Process" execution mode.

    Uses sobel filter -> watershed -> local mean neighbor count -> fancy indexing

    Args:
        verbose:
        compactness: Higher values result in more regularly-shaped watershed basins.
        image_input: Raw Image
        mask_input: Mitochondria Mask Image

    Returns:
        Generate the internal mask and applies it to the raw image.
    """
    processed = []
    for image_index in range(len(image_input)):
        sobel = cle.pull(cle.sobel(image_input[image_index])).astype(np.uint32)
        segments_watershed = watershed(sobel, compactness=compactness, mask=mask_input[image_index])
        touch_matrix = cle.generate_touch_matrix(segments_watershed)
        neighbor_count = cle.count_touching_neighbors(touch_matrix)
        local_mean_neighbor_count = cle.mean_of_touching_neighbors(neighbor_count, touch_matrix)
        parametric_image = cle.replace_intensities(segments_watershed, local_mean_neighbor_count)
        membrane_mask = cle.pull(parametric_image).astype(np.uint32)
        membrane_mask[membrane_mask <= 4] = 0
        membrane_mask[membrane_mask == stats.mode(membrane_mask[0], keepdims=False)[0]] = 0
        membrane_mask[membrane_mask > 0] = 1
        processed.append(image_input[image_index] * np.array(ndimage.binary_fill_holes(membrane_mask)))
    return np.asarray(processed)


def to_np(features, label=None):
    """
    Function which takes a feature set and or ground truth
    and reshapes it such that it can be used as training
    and labels for the VEMClassifier.

    Args:
        features: Image X features
        label: Image y labels

    Returns:
        `X`, `y` training data in format readable by VEMClassifier
        and the `feature_stack`.
    See Also:
        https://github.com/haesleinhuepf/apoc
    """
    feature_stack = features.reshape(-1, features.shape[3])
    if label is None:
        return feature_stack
    else:
        # make the annotation 1-dimensional
        ground_truth_np = label.reshape(-1)

        X = feature_stack
        y = ground_truth_np

        # remove all pixels from the feature and annotations which have not been annotated
        mask = y > 0
        X = X[mask]
        y = y[mask]

        # Encode target labels with value between 0 and n_classes-1.
        le = LabelEncoder()
        y = le.fit_transform(y)

        return X, y, feature_stack


def pre_process(X, mask=None, rem_membrane=False, verbose=False):
    """
    Function to check if there is to be any preprocessing
    on the user inputted X. If mask is not none then a mask
    will be applied. If the mask is not none and rem_membrane
    is True then the outer segments of the mask will be removed.

    Args:
        verbose:
        X: Image
        mask: Mask image
        rem_membrane: Flag to remove membrane

    Returns:
        X which has had preprocessing applied.
    """
    if mask is not None and rem_membrane:
        if mask.any():
            X = remove_membrane(X, mask, verbose)
    elif mask is not None and not rem_membrane:
        if mask.any():
            X = mask_img(X, mask)

    return X


def img_to_3d(img) -> np.array:
    """
    Simple function to reformat 2D image to
    a single 3D Image. For example an image of
    input (255 x 255) will be returned as
    (1 x 255 x 255).


    Args:
        img: Image to convert

    Returns:
        Image with added dimension
    """
    img = np.array(img)
    return img.reshape((1,) + img.shape)


def generate_feature_stack(image, features_specification: Union[str, PredefinedFeatureSet] = None):
    """
    Creates a feature stack from a given image.

    Parameters
    ----------
    image : ndarray
        2D or 3D image to generate a feature stack from
    features_specification : str or PredefinedFeatureSet
        a space-separated list of features, e.g.
        original gaussian=4 sobel_of_gaussian=4 or a
        PredefinedFeatureSet

    See Also
    --------
    https://github.com/haesleinhuepf/apoc

    Returns
    -------
    a list of OCLarray images
    """

    image = cle.push(image)

    # default features
    if features_specification is None:
        blurred = cle.gaussian_blur(image, sigma_x=2, sigma_y=2, sigma_z=2)
        edges = cle.sobel(blurred)
        stack = [
            image,
            blurred,
            edges
        ]

        return stack
    if isinstance(features_specification, PredefinedFeatureSet):
        features_specification = features_specification.value

    while "  " in features_specification:
        features_specification = features_specification.replace("  ", " ")
    while "\t" in features_specification:
        features_specification = features_specification.replace("\t", " ")

    features_specs = features_specification.split(" ")
    generated_features = {}

    result_features = []

    for spec in features_specs:
        if spec.lower() == 'original':
            generated_features['original'] = image
            result_features.append(image)
        elif "=" in spec:
            temp = spec.split("=")
            operation = temp[0]
            numeric_parameter = float(temp[1])

            if not hasattr(cle, operation) and "_of_" in operation:
                temp = operation.split("_of_")
                outer_operation = temp[0]
                inner_operation = temp[1]

                if (inner_operation + "=" + str(numeric_parameter)) not in generated_features.keys():
                    new_image = cle.create_like(image)
                    _apply_operation(inner_operation, image, new_image, numeric_parameter)
                    generated_features[inner_operation + "=" + str(numeric_parameter)] = new_image

                if (operation + "=" + str(numeric_parameter)) not in generated_features.keys():
                    new_image2 = cle.create_like(image)
                    _apply_operation(outer_operation,
                                     generated_features[inner_operation + "=" + str(numeric_parameter)], new_image2,
                                     numeric_parameter)
                    generated_features[operation + "=" + str(numeric_parameter)] = new_image2
            else:
                if (operation + "=" + str(numeric_parameter)) not in generated_features:
                    new_image = cle.create_like(image)
                    _apply_operation(operation, image, new_image, numeric_parameter)
                    generated_features[operation + "=" + str(numeric_parameter)] = new_image
            result_features.append(cle.pull(generated_features[operation + "=" + str(numeric_parameter)]))
        elif not hasattr(cle, spec.lower()):
            raise (AttributeError("module 'pyclesperanto_prototype' has no attribute '{}'".format(spec)))

    result_features = np.moveaxis(result_features, 0, -1)
    if not np.any(result_features):
        raise MemoryError("Dataset exceeded memory, please use a subset of the dataset")

    return result_features


def _apply_operation(operation, input_image, output_image, numeric_parameter):
    """Apply a given image-filter to an image and save the result into another new_image.

    Parameters
    ----------
    operation: callable
    input_image: ndimage
    output_image: ndimage
    numeric_parameter: float or int
        The filters typically have numeric parameters, such as radius or sigma.

    See Also
    --------
    https://github.com/haesleinhuepf/apoc
    """
    func = getattr(cle, operation)
    sig = inspect.signature(func)
    if len(sig.parameters.keys()) == 2:
        func(input_image, output_image)
    elif len(sig.parameters.keys()) == 3:
        func(input_image, output_image, numeric_parameter)
    elif len(sig.parameters.keys()) == 4:
        func(input_image, output_image, numeric_parameter, numeric_parameter)
    elif len(sig.parameters.keys()) == 5:
        func(input_image, output_image, numeric_parameter, numeric_parameter, numeric_parameter)
    elif len(sig.parameters.keys()) == 8:
        # e.g. difference_of_gaussian
        func(input_image, output_image, numeric_parameter * 0.9, numeric_parameter * 0.9, numeric_parameter * 0.9,
             numeric_parameter * 1.1, numeric_parameter * 1.1, numeric_parameter * 1.1)
    else:
        func(input_image, output_image, numeric_parameter, numeric_parameter, numeric_parameter)


def predict_iou(y_true,
                y_pred,
                average: Optional[str] = 'binary'
                ):
    """

    Args:
        y_true:
        y_pred:
        average:

    Returns:

    """

    return jaccard_score(y_true.flatten(), y_pred.flatten(), average=average)
