import logging
import re
from collections import namedtuple
from typing import List, Optional

from semantic_version import Version

from pai.api.image_api import ImageLabel
from pai.common.utils import make_list_resource_iterator
from pai.decorator import config_default_session
from pai.session import Session

logger = logging.getLogger(__name__)

_SUPPORTED_RETRIEVE_FRAMEWORK = [
    "xgboost",
    "tensorflow",
    "pytorch",
    "oneflow",
    "modelscope",
]

# Regex expression pattern for PAI Docker Image Tag.
_PAI_IMAGE_TAG_PATTERN = re.compile(
    r"([\w._-]+)-(gpu|cpu|mkl-cpu)-(py\d+)(?:-(cu\d+))?-([\S]+)"
)
# Regex expression pattern for PAI Docker Image URI.
_PAI_IMAGE_URI_PATTERN = re.compile(r"([\S]+)/([\S]+)/([\S]+):([\S]+)")


_ImageProperties = namedtuple(
    "ImageProperties",
    [
        "image_uri",
        "repo_name",
        "framework_name",
        "framework_version",
        "accelerator_type",
        "py_version",
        "cuda_version",
        "os_version",
    ],
)


def _make_image_properties(framework_name, image_uri) -> Optional[_ImageProperties]:
    """Make a ImageProperties object by parsing the image_uri."""
    match = _PAI_IMAGE_URI_PATTERN.match(image_uri)
    if not match:
        logger.warning(
            "Could not recognize the given image uri, ignore the image:"
            f" image_uri={image_uri}"
        )
        return
    host, namespace, repo_name, tag = match.groups()
    tag_match = _PAI_IMAGE_TAG_PATTERN.match(tag)
    if not tag_match:
        logger.warning(
            f"Could not recognize the given image tag, ignore the image:"
            f" image_uri={image_uri}."
        )
        return
    fw_version, cpu_or_gpu, py_version, cuda_version, os_version = tag_match.groups()
    return _ImageProperties(
        image_uri=image_uri,
        repo_name=repo_name,
        framework_name=framework_name,
        framework_version=fw_version,
        accelerator_type=cpu_or_gpu,
        py_version=py_version,
        cuda_version=cuda_version,
        os_version=os_version,
    )


def _list_images(name: str, labels: List[str], session: Session):
    iterator = make_list_resource_iterator(
        session.image_api.list,
        name=name,
        labels=labels,
        # set the workspace_id manually, prevent using the default workspace of the
        # session.
        workspace_id=0,
        order="DESC",
        sort_by="GmtCreateTime",
        page_size=50,
    )
    return [item for item in iterator]


@config_default_session
def retrieve(
    framework_name: str,
    framework_version: Optional[str] = None,
    accelerator_type: Optional[str] = None,
    session: Optional[Session] = None,
) -> str:
    """Retrieve a PAI public image URI that satisfy the requirements.

    Examples::

        # get a TensorFlow image with specific version.
        retrieve(framework_name="TensorFlow", framework_version="2.3")

        # get the latest PyTorch image supports GPU.
        retrieve(framework_name="PyTorch", accelerator="GPU")

    Args:
        framework_name (str): The name of the framework, could be TensorFlow,
            XGBoost, PyTorch, OneFlow, etc.
        framework_version (Optional[str]): A framework version. If not provided, the
            latest framework version that PAI supported is used.
        accelerator_type (Optional[str]): Name of accelerator supported by the image, If
            not provided, use CPU image by default.
        session (:class:`pai.session.Session`): A session object used to interact with
            the PAI Service. If not provided, a default session is used.

    Returns:
        str: A image uri that satisfy the requirements.
    """
    framework_name = framework_name.lower()
    if framework_name not in _SUPPORTED_RETRIEVE_FRAMEWORK:
        raise ValueError(
            f"The framework ({framework_name}) is not supported by the"
            f" retrieve method, only XGBoost, TensorFlow, PyTorch, and OneFlow"
            f" are supported."
        )

    # label filter used to list all PAI DLC official images.
    labels = [
        ImageLabel.DLC_LABEL,
        ImageLabel.OFFICIAL_LABEL,
    ]

    # if accelerator_type is not specified, use CPU image by default.
    if not accelerator_type or accelerator_type.lower() == "cpu":
        labels.append(ImageLabel.CHIP_TYPE_CPU)
    elif accelerator_type.lower() == "gpu":
        labels.append(ImageLabel.CHIP_TYPE_GPU)
    else:
        raise ValueError(
            f"Given accelerator type ({accelerator_type}) is not supported, only"
            f" CPU and GPU is supported."
        )

    resp = _list_images(name=framework_name, labels=labels, session=session)

    # currently, only training scope is supported.
    scope = "training"

    # extract image properties, such as framework version, py_version, os_version, etc,
    # from image tag.
    candidates = []
    for image_item in resp:
        image_property = _make_image_properties(
            framework_name=framework_name, image_uri=image_item["ImageUri"]
        )

        # PAI DLC Image repo name should be '{framework}' or '{framework}-{scope}'.
        if image_property.repo_name not in [
            framework_name,
            f"{framework_name}-{scope}",
        ]:
            continue
        candidates.append(image_property)

    if not candidates:
        raise RuntimeError(
            f"Not found any image that satisfy the requirements: framework_name="
            f"{framework_name}, accelerator={accelerator_type}"
        )

    if framework_version:
        # find the image with the specific framework version.
        img_uri = next(
            (
                img.image_uri
                for img in candidates
                if img.framework_version == framework_version
            ),
            None,
        )
        if not img_uri:
            supported_versions = [img.framework_version for img in candidates]
            raise RuntimeError(
                f"Not found the specific framework: framework_name={framework_name}, "
                f"framework_version={framework_version}, supported versions for the"
                f" framework are {','.join(supported_versions)} "
            )
        else:
            return img_uri
    else:
        # select the latest framework version.
        def to_semantic_version(version_str) -> Version:
            try:
                return Version.coerce(version_str)
            except ValueError:
                # some version_str from image tag could not be converted to semantic
                # version, for example 'deeprec202212' for tensorflow.
                return Version.coerce("0.0.0")

        candidates = sorted(
            candidates,
            key=lambda img: to_semantic_version(img.framework_version),
            reverse=True,
        )
        return candidates[0].image_uri


@config_default_session
def list_pai_images(
    name: Optional[str] = None, session: Optional[Session] = None
) -> List[str]:
    """List available PAI images.

    Args:
        name: Name of the image, support fuzzy searching.
        session (:class:`pai.session.Session`): A session object used to interact with
            the PAI Service. If not provided, a default session is used.

    Returns:
        List[str]: A list of image_uris.

    """

    labels = [
        ImageLabel.DLC_LABEL,
        ImageLabel.OFFICIAL_LABEL,
        ImageLabel.ORIGIN_PAI_LABEL,
    ]
    images = _list_images(name=name, labels=labels, session=session)
    return [item["ImageUri"] for item in images]


@config_default_session
def list_community_images(
    name=Optional[None], session: Optional[Session] = None
) -> List[str]:
    """List available community images.

    Args:
        name: Name of the image, support fuzzy searching.
        session (:class:`pai.session.Session`): A session object used to interact with
            the PAI Service. If not provided, a default session is used.

    Returns:
        List[str]: A list of image_uris.

    """

    labels = [
        ImageLabel.DLC_LABEL,
        ImageLabel.OFFICIAL_LABEL,
        ImageLabel.ORIGIN_COMMUNITY_LABEL,
    ]

    images = _list_images(name=name, labels=labels, session=session)
    return [item["ImageUri"] for item in images]
