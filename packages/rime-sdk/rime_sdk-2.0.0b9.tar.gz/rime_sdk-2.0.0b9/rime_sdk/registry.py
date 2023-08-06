"""Library that defines the interface to the Registry."""
import json
import logging
from typing import Dict, Iterator, List, Optional, cast

from rime_sdk.internal.config_parser import (
    convert_model_info_to_swagger,
    convert_single_data_info_to_swagger,
    convert_single_pred_info_to_swagger,
)
from rime_sdk.internal.rest_error_handler import RESTErrorHandler
from rime_sdk.swagger import swagger_client
from rime_sdk.swagger.swagger_client import ApiClient
from rime_sdk.swagger.swagger_client.models import (
    DatasetProjectIdUuidBody,
    ModelIdUuidDatasetIdBody,
    ModelProjectIdUuidBody,
    RimeListDatasetsResponse,
    RimeListModelsResponse,
    RimeRegisterDatasetResponse,
    RimeRegisterModelResponse,
    RimeUUID,
    SchemaregistryMetadata,
)

logger = logging.getLogger(__name__)


class Registry:
    """An interface to a RIME Registry."""

    def __init__(self, api_client: ApiClient) -> None:
        """Create a new Registry object.

        Arguments:
            api_client: ApiClient
                The client used to query the RIME cluster.
        """
        self._api_client = api_client

    def register_dataset(
        self,
        project_id: str,
        name: str,
        data_config: dict,
        integration_id: Optional[str] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[dict] = None,
    ) -> str:
        """Register a new dataset in a Project.

        Args:
            project_id: str
                The ID of the Project in which to register the dataset.
            name: str
                The chosen name of the dataset.
            data_config: dict
                A dictionary that contains the data configuration.
                The data configuration must match the API specification
                of the `data_info` field in the `RegisterDataset` request.
            integration_id: Optional[str] = None,
                Provide the integration ID for datasets that require an integration.
            tags: Optional[List[str]] = None,
                An optional list of tags to associate with the dataset.
            metadata: Optional[dict] = None,
                An optional dictionary of metadata to associate with the dataset.

        Returns:
            str:
                The ID of the newly registered dataset.

        Raises:
            ValueError
                This error is generated when the request to the Registry
                service fails.

        Example:
            .. code-block:: python

                dataset_id = registry.register_dataset(
                    name=DATASET_NAME,
                    data_config={
                        "connection_info": {"data_file": {"path": FILE_PATH}},
                        "data_params": {"label_col": LABEL_COL},
                    },
                    integration_id=INTEGRATION_ID,
                )
        """
        data_info_swagger = convert_single_data_info_to_swagger(data_config)
        req = DatasetProjectIdUuidBody(
            project_id=RimeUUID(uuid=project_id), name=name, data_info=data_info_swagger
        )

        metadata_str: Optional[str] = None
        if metadata is not None:
            metadata_str = json.dumps(metadata)
        if tags is not None or metadata_str is not None:
            req.metadata = SchemaregistryMetadata(tags=tags, extra_info=metadata_str)

        if integration_id is not None:
            req.integration_id = RimeUUID(uuid=integration_id)

        with RESTErrorHandler():
            api = swagger_client.RegistryServiceApi(self._api_client)
            res = api.registry_service_register_dataset(
                body=req, project_id_uuid=project_id,
            )

            res = cast(RimeRegisterDatasetResponse, res)

        return res.dataset_id

    def register_model(
        self,
        project_id: str,
        name: str,
        model_config: Optional[dict] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[dict] = None,
        external_id: Optional[str] = None,
    ) -> str:
        """Register a new model in a Project.

        Args:
            project_id: str
                The ID of the Project in which to register the model.
            name: str
                The chosen name of the model.
            model_config: Optional[dict] = None,
                A dictionary that contains the model configuration.
                Any model configuration that is provided must match the API
                specification for the `model_info` field of the `RegisterModel`
                request.
            tags: Optional[List[str]] = None,
                An optional list of tags to associate with the model.
            metadata: Optional[dict] = None,
                An optional dictionary of metadata to associate with the model.
            external_id: Optional[str] = None,
                An optional external ID that can be used to identify the model.

        Returns:
            str:
                The ID of the newly registered model.

        Raises:
            ValueError
                This error is generated when the request to the Registry
                service fails.

        Example:
            .. code-block:: python

                model_id = registry.register_model(
                    name=MODEL_NAME,
                    model_config={
                        "hugging_face": {
                            "model_uri": URI,
                            "kwargs": {
                                "tokenizer_uri": TOKENIZER_URI,
                                "class_map": MAP,
                                "ignore_class_names": True,
                            },
                        }
                    },
                    tags=[MODEL_TAG],
                    metadata={KEY: VALUE},
                    external_id=EXTERNAL_ID,
                )
        """
        req = ModelProjectIdUuidBody(project_id=RimeUUID(uuid=project_id), name=name,)

        if model_config is not None:
            # When the `model_path` key is provided to the dictionary, the value
            # must be a dictionary whose `path` value points to a python
            # file that holds a `predict_dict` or `predict_df` function.
            # When the `model_loading` key is provided to the dictionary, the value
            # must be a dictionary whose `path` value points to a python
            # file that holds a `get_predict_df` or `get_predict_dict` function and
            # whose value for the `params` key is a dictionary of parameters to
            # pass to the function.
            # When the `hugging_face` key is provided to the dictionary, the value must
            # be a dictionary whose `model_uri` value points to a
            # hugging face model and whose value for the `params` key is a dictionary
            # of parameters that hugging face model requires.
            model_info = convert_model_info_to_swagger(model_config)
            req.model_info = model_info

        metadata_str: Optional[str] = None
        if metadata:
            metadata_str = json.dumps(metadata)
        if tags or metadata_str:
            req.metadata = SchemaregistryMetadata(tags=tags, extra_info=metadata_str)
        if external_id:
            req.external_id = external_id

        with RESTErrorHandler():
            api = swagger_client.RegistryServiceApi(self._api_client)
            res = api.registry_service_register_model(
                body=req, project_id_uuid=project_id,
            )

            res = cast(RimeRegisterModelResponse, res)

        return cast(RimeUUID, res.model_id).uuid

    def register_predictions(
        self,
        project_id: str,
        dataset_id: str,
        model_id: str,
        pred_config: dict,
        integration_id: Optional[str] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[dict] = None,
    ) -> None:
        """Register a new set of predictions for a model on a dataset.

        Args:
            project_id: str
                The ID of the Project to which the models belong.
            dataset_id: str,
                The ID of the dataset used to generate the predictions.
            model_id: str,
                The ID of the model used to generate the predictions.
            pred_config: dict,
                A dictionary that contains the prediction configuration.
                The prediction configuration must match the API specification
                for the `pred_info` field of the `RegisterPredictions` request.
            integration_id: Optional[str] = None,
                Provide the integration ID for predictions that require an
                integration to use.
            tags: Optional[List[str]] = None,
                An optional list of tags to associate with the predictions.
            metadata: Optional[dict] = None,
                An optional dictionary of metadata to associate with the predictions.

        Returns:
            None

        Raises:
            ValueError
                This error is generated when the request to the Registry
                service fails.

        Example:
            .. code-block:: python

                registry.register_predictions(
                    dataset_id=DATASET_ID,
                    model_id=MODEL_ID,
                    pred_config={
                        "connection_info": {
                            "delta_lake": {
                                # Unix timestamp equivalent to 02/08/2023
                                "start_time": 1675922943,
                                # Unix timestamp equivalent to 03/08/2023
                                "end_time": 1678342145,
                                "table_name": TABLE_NAME,
                                "time_col": TIME_COL,
                            },
                        },
                        "pred_params": {"pred_col": PREDS},
                    },
                    tags=[TAG],
                    metadata={KEY: VALUE},
                )
        """
        pred_info_swagger = convert_single_pred_info_to_swagger(pred_config)

        req = ModelIdUuidDatasetIdBody(
            project_id=RimeUUID(uuid=project_id),
            model_id=RimeUUID(uuid=model_id),
            pred_info=pred_info_swagger,
        )

        metadata_str: Optional[str] = None
        if metadata is not None:
            metadata_str = json.dumps(metadata)
        if tags is not None or metadata_str is not None:
            req.metadata = SchemaregistryMetadata(tags=tags, extra_info=metadata_str)

        if integration_id is not None:
            req.integration_id = RimeUUID(uuid=integration_id)

        with RESTErrorHandler():
            api = swagger_client.RegistryServiceApi(self._api_client)
            _ = api.registry_service_register_prediction_set(
                body=req,
                project_id_uuid=project_id,
                model_id_uuid=model_id,
                dataset_id=dataset_id,
            )

    def list_datasets(self, project_id: str) -> Iterator[Dict]:
        """Return a list of datasets.

        Args:
            project_id: str
                The ID of the Project to which the datasets belong.

        Returns:
            Iterator[Dict]:
                Iterator of dictionaries: each dictionary represents a
                dataset.

        Raises:
            ValueError
                This error is generated when the request to the Registry
                service fails.
        """
        api = swagger_client.RegistryServiceApi(self._api_client)
        # Iterate through the pages of datasets and break at the last page.
        page_token = ""
        with RESTErrorHandler():
            while True:
                if page_token == "":
                    res: RimeListDatasetsResponse = api.registry_service_list_datasets(
                        project_id_uuid=project_id
                    )
                else:
                    res = api.registry_service_list_datasets(
                        project_id_uuid=project_id, page_token=page_token
                    )
                if res.datasets is not None:
                    for dataset in res.datasets:
                        yield dataset.to_dict()
                # Advance to the next page of datasets.
                page_token = res.next_page_token
                # we've reached the last page of datasets.
                if not res.has_more:
                    break

    def list_models(self, project_id: str) -> Iterator[Dict]:
        """Return a list of models.

        Args:
            project_id: str
                The ID of the Project to which the models belong.

        Returns:
            Iterator[Dict]:
                Iterator of dictionaries: each dictionary represents a
                model.

        Raises:
            ValueError
                This error is generated when the request to the Registry
                service fails.
        """
        api = swagger_client.RegistryServiceApi(self._api_client)
        # Iterate through the pages of datasets and break at the last page.
        page_token = ""
        with RESTErrorHandler():
            while True:
                if page_token == "":
                    res: RimeListModelsResponse = api.registry_service_list_models(
                        project_id_uuid=project_id
                    )
                else:
                    res = api.registry_service_list_models(
                        project_id_uuid=project_id, page_token=page_token
                    )
                if res.models is not None:
                    for model in res.models:
                        yield model.model.to_dict()
                # Advance to the next page of models.
                page_token = res.next_page_token
                # we've reached the last page of models.
                if not res.has_more:
                    break
