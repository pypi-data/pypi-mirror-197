from typing import Any, Dict, List, Union

from pai.api.base import PaginatedResult, WorkspaceScopedResourceAPI
from pai.common.consts import DEFAULT_PAGE_NUMBER, DEFAULT_PAGE_SIZE, PAIServiceName
from pai.libs.alibabacloud_aiworkspace20210204.client import Client
from pai.libs.alibabacloud_aiworkspace20210204.models import (
    ListImagesRequest,
    ListImagesResponseBody,
)


class ImageLabel(object):

    # Unofficial Image Label
    UNOFFICIAL_LABEL = "system.official=false"
    # Official Image Label
    OFFICIAL_LABEL = "system.official=true"

    # PAI Image Label
    ORIGIN_PAI_LABEL = "system.origin=PAI"
    # Community Image Label
    ORIGIN_COMMUNITY_LABEL = "system.origin=Community"

    # DLC Image Label
    DLC_LABEL = "system.supported.dlc=true"
    # DSW Image Label
    DSW_LABEL = "system.supported.dsw=true"

    # Accelerator: Use GPU
    CHIP_TYPE_GPU = "system.chipType=GPU"
    CHIP_TYPE_CPU = "system.chipType=CPU"


class ImageAPI(WorkspaceScopedResourceAPI):
    """Class which provide API to operate CodeSource resource."""

    BACKEND_SERVICE_NAME = PAIServiceName.AIWORKSPACE

    _list_method = "list_images_with_options"
    _create_method = "create_image_with_options"
    _delete_method = "add_image_with_options"

    def list(
        self,
        name=None,
        creator_id=None,
        verbose=False,
        labels: Union[Dict[str, Any], List[str]] = ImageLabel.UNOFFICIAL_LABEL,
        sort_by=None,
        order="DESC",
        page_number=DEFAULT_PAGE_NUMBER,
        page_size=DEFAULT_PAGE_SIZE,
        **kwargs,
    ) -> PaginatedResult:
        """List image resources."""
        workspace_id = kwargs.pop("workspace_id", None)
        if isinstance(labels, dict):
            labels = ",".join(["{}={}".format(k, v) for k, v in labels.items()])
        elif isinstance(labels, list):
            labels = ",".join([item for item in labels])

        req = ListImagesRequest(
            labels=labels,
            name=name,
            operator_create=creator_id,
            sort_by=sort_by,
            order=order,
            verbose=verbose,
            page_size=page_size,
            page_number=page_number,
            workspace_id=workspace_id,
        )

        return self._list(request=req)

    def _list(self, request) -> PaginatedResult:
        resp: ListImagesResponseBody = self._do_request(
            self._list_method, request=request
        )

        return self.make_paginated_result(resp)
