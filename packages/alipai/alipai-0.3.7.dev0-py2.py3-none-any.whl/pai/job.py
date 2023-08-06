import copy
import functools
import logging
import os.path
import posixpath
import shlex
import textwrap
import time
from datetime import datetime
from typing import Callable, Dict, List, Optional, Sequence, Tuple, Union

import six

from .base import EntityBaseMixin
from .code_source import CodeSourceConfig
from .common.consts import DEFAULT_WORKER_ECS_SPEC, DataSourceType, JobType, WorkerType
from .common.oss_utils import OssUriObj, upload_data
from .common.utils import random_str
from .dataset import Dataset, DataSourceConfig
from .decorator import config_default_session
from .schema.job_schema import JobSchema, JobSpecSchema
from .session import Session

logger = logging.getLogger(__name__)

_PAI_JOB_CONSOLE_URL_PATTERN = (
    "{console_uri}/?regionId={region_id}&"
    "workspaceId={workspace_id}#/job/detail?jobId={job_id}"
)


class ResourceConfig(object):
    """A class that specific the resource used by a job node.

    Examples::

    # A ResourceConfig instance that request 8 CPU core and 32Gi memory for each node.
    resource_config = ResourceConfig(
        cpu=8,
        memory=32,
    )

    """

    def __init__(
        self,
        cpu: str,
        memory: str,
        gpu: int = None,
        shared_memory: str = None,
        gpu_type: str = None,
    ):
        self.cpu = str(cpu)
        self.memory = self._patch_memory_unit(memory=memory)
        self.gpu = str(gpu) if gpu else None
        self.shared_memory = self._patch_memory_unit(memory=shared_memory)
        self.gpu_type = gpu_type

    @classmethod
    def _patch_memory_unit(cls, memory):
        if not memory:
            return

        if isinstance(memory, six.string_types):
            memory = memory.strip()
            if memory.endswith("Gi"):
                return memory
        memory = int(memory)
        return "{}Gi".format(memory)

    def __repr__(self):
        return (
            f"<ResourceConfig:cpu={self.cpu} memory={self.memory} gpu={self.gpu or 0}"
            f" gpu_type={self.gpu_type}>"
        )


class JobSpec(object):
    """Class representing a worker pool config used by a job.

    A job receive a list of ``JobSpec`` to represent resource and worker config for the
    job.

    A PyTorch Distributed-Data-Parallel job spec example::

    job_specs = [
        JobSpec(
            pod_count=2,
            image="<tensorflow-image-uri>",
            instance_type="ecs.c6.xlarge",
            type=WorkerType.WORKER,
        )
    ]


    A PS-Worker Job Examples::

    job_specs = [
        JobSpec(
            pod_count=2,
            image="<tensorflow-image-uri>",
            instance_type="ecs.c6.xlarge",
            type=WorkerType.PS,
        ),
        JobSpec(
            pod_count=2,
            image="<tensorflow-image-uri>",
            instance_type="ecs.c6.xlarge",
            type=WorkerType.WORKER,
        ),
    ]


    """

    def __init__(
        self,
        pod_count: int,
        image: Optional[str] = None,
        instance_type: Optional[str] = None,
        resource_config: Optional[ResourceConfig] = None,
        type: str = WorkerType.WORKER,
        use_spot_instance: bool = False,
    ):
        """A class representing a worker pool config.

        Args:
            pod_count (int): The number of worker in the worker pool.
            image (str): Image used in the worker pool.
            instance_type (str, optional): The machine instance type used.
            resource_config (ResourceConfig, optional): Resource allocation config for
                the worker pool.
            type (str): Worker type of the worker pool. Type is closely related to Job
                Type, and different Job Types support different Worker Types.

                - TFJob : supports Chief, PS, Worker, Evaluator, GraphLearn
                - PyTorchJob : supports Worker, Master
                - XGBoostJob : Support Worker, Master

                The Master in PyTorchJob and XGBoostJob is optional; if the Master is
                not specified, the system will automatically regard the first Worker
                node (RANK=0) as the Master node.

            use_spot_instance (bool): Whether to use spot instances.
        """
        self.instance_type = instance_type
        self.type = type
        self.pod_count = pod_count
        self.resource_config = resource_config
        self.image = image
        self.use_spot_instance = use_spot_instance

    @classmethod
    def from_resource_config(
        cls,
        worker_cpu,
        worker_memory,
        worker_count,
        worker_image,
        worker_gpu=0,
        worker_shared_memory=None,
        ps_count=0,
        ps_cpu=None,
        ps_memory=None,
        ps_image=None,
        ps_gpu=None,
        ps_shared_memory=None,
    ) -> List["JobSpec"]:
        """A convenient method to build a list of job spec."""
        specs = []
        if worker_count > 0:
            worker_spec = JobSpec(
                pod_count=worker_count,
                type=WorkerType.WORKER,
                resource_config=ResourceConfig(
                    cpu=worker_cpu,
                    memory=worker_memory,
                    gpu=worker_gpu,
                    shared_memory=worker_shared_memory,
                ),
                image=worker_image,
            )
            specs.append(worker_spec)

        if ps_count > 0:
            ps_spec = JobSpec(
                pod_count=ps_count,
                type=WorkerType.PS,
                resource_config=ResourceConfig(
                    cpu=ps_cpu,
                    memory=ps_memory,
                    gpu=ps_gpu,
                    shared_memory=ps_shared_memory,
                ),
                image=ps_image,
            )
            specs.append(ps_spec)

        return specs

    @classmethod
    def from_instance_type(
        cls,
        worker_count=1,
        worker_instance_type=DEFAULT_WORKER_ECS_SPEC,
        worker_image=None,
        ps_image=None,
        ps_count=None,
        ps_instance_type=None,
        master_image=None,
        master_count=None,
        master_instance_type=None,
    ) -> List["JobSpec"]:
        """A convenient method to build a list of job spec that request resource by
        machine instance type"""
        job_specs = []
        if worker_count and worker_count > 0:
            job_specs.append(
                JobSpec(
                    instance_type=worker_instance_type,
                    type=WorkerType.WORKER,
                    pod_count=worker_count,
                    image=worker_image,
                ),
            )

        if ps_count:
            job_specs.append(
                JobSpec(
                    instance_type=ps_instance_type,
                    type=WorkerType.PS,
                    pod_count=ps_count,
                    image=ps_image,
                ),
            )

        if master_count:
            job_specs.append(
                JobSpec(
                    instance_type=master_instance_type,
                    type=WorkerType.MASTER,
                    pod_count=master_count,
                    image=master_image,
                )
            )

        return job_specs

    def to_api_object(self):
        return JobSpecSchema().dump(self)

    def to_dict(self):
        return self.to_api_object()


class JobStatus(object):
    """Represent PAI-DLC Job status"""

    Creating = "Creating"
    Queuing = "Queuing"
    Dequeued = "Dequeued"
    Running = "Running"
    Restarting = "Restarting"
    Succeeded = "Succeeded"
    Failed = "Failed"
    Stopping = "Stopping"
    Stopped = "Stopped"

    @classmethod
    def completed_status(cls):
        return [
            cls.Succeeded,
            cls.Failed,
            cls.Stopped,
        ]

    @classmethod
    def failed_status(cls):
        return [
            cls.Failed,
            cls.Stopped,
        ]


def require_submitted(f: Callable) -> Callable:
    """Decorator on method/property which requires the job has been submitted."""

    @functools.wraps(f)
    def _(self, *args, **kwargs):
        if not self.job_id:
            raise ValueError(
                "Job is not submitted, the method/property is not available."
            )

        return f(self, *args, **kwargs)

    return _


class JobPod(EntityBaseMixin):
    """Class that represent Job Pod."""

    def __init__(
        self,
        pod_id: str,
        status: str,
        type: str,
        pod_uid: Optional[str] = None,
        ip: Optional[str] = None,
        create_time: datetime = None,
        start_time: datetime = None,
        finish_time: datetime = None,
    ):
        super(JobPod, self).__init__()
        self.create_time = create_time
        self.finish_time = finish_time
        self.start_time = start_time
        self.ip = ip  # type: str
        self.pod_id = pod_id  # type: str
        self.pod_uid = pod_uid  # type: str
        self.status = status  # type: str
        self.type = type  # type: str

    @property
    def id(self):
        return self.pod_id

    def __repr__(self):
        return "Pod:type={} id={} status={}".format(self.type, self.id, self.status)


class Job(EntityBaseMixin):
    """Class represent PAI DLC job."""

    _schema_cls = JobSchema

    @config_default_session
    def __init__(
        self,
        user_command: Optional[Union[str, List[str]]],
        job_specs: List[JobSpec],
        job_type: str = JobType.TFJob,
        display_name: Optional[str] = None,
        environment_variables: Optional[Dict[str, str]] = None,
        max_running_time_minutes: Optional[int] = None,
        resource_id: Optional[str] = None,
        priority: Optional[int] = None,
        thirdparty_libs: Optional[List[str]] = None,
        thirdparty_lib_dir: Optional[str] = None,
        data_sources: Optional[List[DataSourceConfig]] = None,
        code_source: Optional[CodeSourceConfig] = None,
        description: Optional[str] = None,
        session: Optional[Session] = None,
        **kwargs,
    ):
        """Initialize a job instance.

        Args:
            user_command (Union[str, List[str]]): The command used to start the user
                program.
            display_name (str): Display name of the job.
            description (str): Description of the job.
            environment_variables (Dict[str, str], optional): Environment variables
                to be set for use.
            max_running_time_minutes (int, optional): The maximum running time of the
                job, in minutes.
            job_specs (List[JobSpec]): A list of JobSpec represent the config of worker
                in the job.
            job_type (str): Type of the job, could be TFJob, PyTorchJob, XGBoostJob,
                etc.
            resource_id (str, optional): ID of resource group used by the job. If not
                provided, the job will be running in the public resource group;
            priority (int, optional): The priority of the job, only valid if the job
                is running in the dedicated resource group. Valid range is 1~9
                (default: 1).
            thirdparty_libs (List[str], optional): A list of Python packages to be
                installed before user program started.
            data_sources (List[DataSourceConfig], optional): A list of data source used
                by the job.
            code_source (List[CodeSourceConfig], optional): CodeSource used by the job.
            session (Session, optional): A PAI session instance used for communicating
                with PAI service.
            **kwargs:
        """
        self.data_sources = data_sources or []
        self.code_source = code_source
        self.display_name = display_name
        self.environment_variables = environment_variables
        self.max_running_time_minutes = max_running_time_minutes
        self.job_specs = job_specs
        self.job_type = job_type
        self.resource_id = resource_id
        self.priority = priority
        self.user_command = (
            self._make_user_command(user_command)
            if isinstance(user_command, (list, tuple))
            else user_command
        )
        self.thirdparty_libs = thirdparty_libs
        self.thirdparty_lib_dir = thirdparty_lib_dir
        self.description = description

        # Read only fields from API response.
        self._job_id = kwargs.pop("job_id", None)
        self._workspace_id = kwargs.pop("workspace_id", None)
        self._create_time = kwargs.pop("create_time", None)
        self._status = kwargs.pop("status", None)
        self._reason_code = kwargs.pop("reason_code", None)
        self._reason_message = kwargs.pop("reason_message", None)
        super(Job, self).__init__(session=session)

        # self.user_vpc = user_vpc
        # self.debug_config = debugger_config
        # self.elastic_spec = elastic_spec
        # self.job_settings = job_settings

    @property
    def job_id(self) -> str:
        return self._job_id

    @property
    def workspace_id(self) -> str:
        return self._workspace_id

    def __repr__(self) -> str:
        return "{}:job_id={}:".format(
            type(self).__name__, self.job_id if self.job_id else "<NotSubmitted>"
        )

    @require_submitted
    def stop(self):
        """Stop the running Job."""
        self.session.job_api.stop(self.job_id)

    @classmethod
    @config_default_session
    def get(cls, job_id: str, session: Optional[Session] = None) -> "Job":
        """Get a submitted job using job_id.

        Args:
            job_id (str): ID of the specific job.
            session (:class:`pai.session.Session`): A PAI session instance used for
                communicating with PAI service.

        Returns:
            :class:`pai.job.Job`: Job instance.

        """
        return cls.from_api_object(session.job_api.get(job_id), session=session)

    def delete(self) -> None:
        """Delete the job from PAI service."""
        self.session.job_api.delete(self.job_id)

    @property
    def create_time(self):
        """Create time of the job"""
        return self._create_time

    @property
    @require_submitted
    def status(self) -> str:
        """Status of the submitted job."""
        return self._status

    @property
    @require_submitted
    def reason_code(self):
        """Reason code for the job status."""
        return self._reason_code

    @property
    @require_submitted
    def reason_message(self):
        """Reason message for the job status."""
        return self._reason_message

    @classmethod
    def _make_user_command(cls, command_in_list: Sequence[str]) -> str:
        return " ".join([shlex.quote(cmd) for cmd in command_in_list])

    def run(self, wait=False):
        """Submit the job to run in PAI.

        Args:
            wait (bool): If block until the job is completed.

        Returns:
            :class:`pai.job.Job`: The submitted job instance.
        """
        job_id = self.session.job_api.create(
            display_name=self.display_name,
            job_specs=self.job_specs,
            job_type=self.job_type,
            code_source_config=self.code_source,
            data_source_configs=self.data_sources,
            environment_variables=self.environment_variables,
            max_running_time_minutes=self.max_running_time_minutes,
            resource_id=self.resource_id,
            priority=self.priority,
            thirdparty_libs=self.thirdparty_libs,
            thirdparty_lib_dir=self.thirdparty_lib_dir,
            user_command=self.user_command,
            # user_vpc=self.,
        )

        # refresh Job instance attributes by request the PAI service.
        self.session.job_api.refresh_entity(entity=self, id_=job_id)
        print(
            "View the job detail by accessing the console URI: {}".format(
                self.console_uri
            )
        )
        if wait:
            self.wait_for_completion()

        return self

    @require_submitted
    def wait_for_completion(self, interval=10):
        """Block until the job is completed."""
        while True:
            self.session.job_api.refresh_entity(self.job_id, self)
            if self.status in JobStatus.failed_status():
                raise RuntimeError(
                    f"Job completed in error: id={self.job_id} "
                    f"status={self.status} "
                    f"reason_code={self.reason_code} "
                    f"reason_message={self.reason_message}"
                )
            elif self.status in JobStatus.completed_status():
                break
            time.sleep(interval)

    @property
    @require_submitted
    def console_uri(self):
        """Returns the web console uri of the job."""
        return _PAI_JOB_CONSOLE_URL_PATTERN.format(
            console_uri=self.session.console_uri,
            region_id=self.session.region_id,
            workspace_id=self.session.workspace_id,
            job_id=self._job_id,
        )

    @require_submitted
    def list_events(self, start_time=None, end_time=None, max_events_num=2000):
        """List events of the Job.

        Args:
            start_time: Start time of job events range.
            end_time: End time of job events range.
            max_events_num: Max event number return from the response.

        Returns:
            List[str]: List of job events.

        """

        return self.session.job_api.list_events(
            self.job_id,
            start_time=start_time,
            end_time=end_time,
            max_events_num=max_events_num,
        )

    @classmethod
    @config_default_session
    def from_script(
        cls,
        command: str,
        source_dir: str,
        job_specs: List[JobSpec],
        output_path: Optional[str] = None,
        display_name: Optional[str] = None,
        environment_variables: Optional[Dict[str, str]] = None,
        max_running_time_minutes: Optional[int] = None,
        job_type: str = JobType.TFJob,
        resource_id: Optional[str] = None,
        priority: Optional[int] = None,
        thirdparty_libs: Optional[List[str]] = None,
        data_sources: List[Union[DataSourceConfig]] = None,
        session: Optional[Session] = None,
        **kwargs,
    ) -> "Job":
        """Build a job run with given scripts.

        Examples::

            job: Job = Job.from_script(
                source_dir="./src/",
                entry_point="main.py",
                output_path="oss://<bucket>/path/to/output/,
                job_specs=JobSpec.from_instance_type(
                    worker_instance_type="ecs.c6.large",
                    worker_count=1,
                    worker_image=image_uri,
                ),
            )
            job.run()


        Args:
            command(str): Execute command .
            source_dir (str): The local source code directory used in the job. The
                directory will be packaged and uploaded to an OSS bucket, then
                downloaded to the `/ml/usercode` directory before job run.
            job_specs (List[JobSpec]): A list of JobSpec represent the config of worker
                in the job.
            output_path (str, optional): A OSS URI used to store the job output.
                It will be mounted to directory `/ml/output/` of the working container,
                to save the outputs of the job, user code should write the output to
                the directory.
            display_name (str, optional): Display name for the job.
            environment_variables (Dict[str, str], optional): Environment variables
                to be set to the working container.
            max_running_time_minutes (int, optional): The maximum running time of the
                job, in minutes.
            job_type (str): Type of the job, could be TFJob, PyTorchJob, XGBoostJob,
                etc.
            resource_id (str, optional): ID of resource group used by the job. If not
                provided, the job will be running in the public resource group;
            priority (int, optional): The priority of the job, only valid if the job
                is running in the dedicated resource group. Valid range is 1~9
                (default: 1).
            thirdparty_libs (List[str], optional): A list of Python packages to be
                installed before user program started.
            data_sources (List[DataSourceConfig], optional): A list of data source used
                by the job.
            session (Session, optional): A PAI session instance used for communicating
                with PAI service.
        Returns:
            Job: A Job instance wait for submitting.
        """
        job_name = display_name or cls._gen_script_job_name()

        # prepare DataSourceConfig and command for the job.
        (
            data_source_configs,
            user_command,
            thirdparty_lib_dir,
        ) = cls._prepare_for_scripts_job(
            data_sources=data_sources,
            source_dir=source_dir,
            output_path=output_path,
            command=command,
            session=session,
        )

        job = cls(
            user_command=user_command,
            display_name=job_name,
            # description=d,
            envs=environment_variables,
            max_running_time_minutes=max_running_time_minutes,
            job_specs=job_specs,
            job_type=job_type,
            resource_id=resource_id,
            priority=priority,
            thirdparty_libs=thirdparty_libs,
            thirdparty_lib_dir=thirdparty_lib_dir,
            data_sources=data_source_configs,
            session=session,
        )
        return job

    @classmethod
    def _gen_script_job_name(
        cls,
    ):
        return "Job-{}".format(datetime.now().isoformat(sep="-", timespec="seconds"))

    @classmethod
    def _prepare_for_scripts_job(
        cls,
        source_dir: str,
        output_path: str,
        data_sources: List[DataSourceConfig],
        command: str,
        session: Session,
    ) -> Tuple[List[DataSourceConfig], str, str]:

        base_dir = "/ml"
        work_dir = posixpath.join(base_dir, "usercode")
        # code_mount_path = posixpath.join(base_dir, "mount/code")
        output_mount_path = posixpath.join(base_dir, "output")

        res = copy.copy(data_sources) if data_sources else []

        # upload source code in local path to OSS bucket and mount the work container.
        (
            data_source_for_code,
            source_code_uri,
            requirements_exists,
        ) = cls._prepare_source_code(
            code_mount_path=work_dir,
            source_dir=source_dir,
            session=session,
        )
        res.append(data_source_for_code)
        thirdparty_lib_dir = work_dir if requirements_exists else None

        # build a temporary data source used for mount output_oss_uri.
        if output_path:
            dataset = Dataset.register(
                source=output_path,
                name="tmp-job-output-{}".format(random_str(12)),
                mount_path=output_mount_path,
                data_source_type=DataSourceType.OSS,
                session=session,
            )
            res.append(dataset.mount(mount_path=output_mount_path))

        exec_command = textwrap.dedent(
            f"""\
        set -e
        # source code: {source_code_uri}
        mkdir -p {work_dir} && cd {work_dir}
        # user command
        {command}
        """
        )

        return res, exec_command, thirdparty_lib_dir

    @classmethod
    def _prepare_source_code(
        cls, source_dir: str, code_mount_path: str, session: Session
    ):
        """Create dataset using for mount input code."""
        requirements_exists = (
            True
            if os.path.exists(os.path.join(source_dir, "requirements.txt"))
            else False
        )

        # tar the source files and upload to OSS bucket of the session.
        script_oss_path = session.get_oss_storage_path("job_scripts")
        source_code_uri = upload_data(
            source_path=source_dir,
            oss_path=script_oss_path,
            oss_bucket=session.oss_bucket,
            # is_tar=True,
        )
        # Dataset OSS URI should be a directory that can be mounted to the container.
        object_dir_uri = OssUriObj(source_code_uri).get_dir_uri()
        dataset = Dataset.register(
            source=session.patch_oss_endpoint(
                object_dir_uri,
            ),
            name="tmp-sourcefile-{}".format(random_str(12)),
            mount_path=code_mount_path,
        )

        return (
            dataset.mount(mount_path=code_mount_path),
            source_code_uri,
            requirements_exists,
        )
