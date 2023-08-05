from ..._protos.public.registry import RegistryService_pb2

from . import _TaskType


class Classification(_TaskType):
    """
    Classification task of the registered model.

    Examples
    --------
    .. code-block:: python

        from verta.registry import task_type
        reg_model = client.create_registered_model("My Model", workspace="my-org", task_type=task_type.Classification())

    """

    _TASK_TYPE = RegistryService_pb2.TaskTypeEnum.TaskType.CLASSIFICATION
