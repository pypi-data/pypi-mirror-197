import logging

logger = logging.getLogger(__name__)


class CodeSourceConfig(object):
    """Job input config."""

    def __init__(self, code_source_id, branch=None, commit=None, mount_path=None):
        self.code_source_id = code_source_id
        self.branch = branch
        self.commit = commit
        self.mount_path = mount_path

    def __str__(self):
        return "CodeSourceConfig: id={0} mount_path={1}".format(
            self.code_source_id, self.mount_path
        )
