#
# Copyright 2021-2023 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
import os
from typing import Any, List, Optional

import trafaret as t

from datarobot.enums import DEFAULT_MAX_WAIT
from datarobot.models.api_object import APIObject
from datarobot.utils import get_id_from_location, pagination
from datarobot.utils.waiters import wait_for_async_resolution


class DataMatching(APIObject):
    """
    Retrieves the closest data points for the input data.

    This functionality is more than the simple lookup. In order to retrieve the closest data
    points data matching functionality will leverage DataRobot preprocessing pipeline first
    and then search for the closest data points. The returned values will be the closest data
    points at the point of entry to the model.

    There are three sets of methods supported:
        1.  Methods to build the index (for project, model, featurelist). The index needs to be
            built first in order to search for the closest data points. Once the index is built
            it will be reused.
        2.  Methods to search for the closest data points (for project, model, featurelist).
            These methods will initialize the query, await its completion and then save the result
            as csv file with in the specified location.
        3.  Additional methods to manually list history of queries and retrieve results for them.

    """

    _build_index_path = "projects/{project_id}/prepareDataMatching/"
    _build_index_model_path = "projects/{project_id}/models/{model_id}/prepareDataMatching/"
    _build_index_featurelist_path = (
        "projects/{project_id}/featurelists/{featurelist_id}/prepareDataMatching/"
    )

    _get_closest_data_path = "projects/{project_id}/dataMatching/"
    _get_closest_data_model_path = "projects/{project_id}/models/{model_id}/dataMatching/"
    _get_closest_data_featurelist_path = (
        "projects/{project_id}/featurelists/{featurelist_id}/dataMatching/"
    )

    def __init__(self, project_id: str) -> None:
        self.project_id = project_id

    def __repr__(self) -> str:
        return f"DataMatching(project_id={self.project_id})"

    def get_query_url(self, url: str, number_of_data: Optional[int] = None) -> str:
        """Returns formatted data matching query url"""
        return f"{url}?numberOfData={number_of_data}" if number_of_data else url

    def _get_closest_data(
        self, url: str, query_file_path: str, result_file_path: str, max_wait: int
    ) -> str:
        """Makes the data matching query and saves the result.

        Parameters
        ----------
        url: str
            Data matching query url to make request to
        query_file_path: str
            Path to file with the data point to search closest data points
        result_file_path: str
            Path where to save the result file
        max_wait: int
            Number of seconds to wait for the result

        Returns
        -------
        Path where to the result was saved
        """
        fname = os.path.basename(query_file_path)
        response = self._client.build_request_with_file(
            method="POST",
            url=url,
            fname=fname,
            file_path=query_file_path,
        )
        location = wait_for_async_resolution(self._client, response.headers["Location"], max_wait)
        data_matching_query = DataMatchingQuery(
            project_id=self.project_id, data_matching_id=get_id_from_location(location)
        )
        data_matching_query.save_result(result_file_path)
        return result_file_path

    def get_closest_data(
        self,
        query_file_path: str,
        result_file_path: str,
        number_of_data: Optional[int] = None,
        max_wait: int = DEFAULT_MAX_WAIT,
    ) -> str:
        """Retrieves closest data points to the data point in input file.

        Parameters
        ----------
        query_file_path: str
            Path to file with the data point to search closest data points
        result_file_path: str
            Path where to save the result file
        number_of_data: int or None
            Number of results to search for. If no value specified, the default is 10.
        max_wait: int
            Number of seconds to wait for the result. Default is 600.

        Returns
        -------
        Path where the result was saved
        """
        url = self._get_closest_data_path.format(project_id=self.project_id)
        result_file_path = self._get_closest_data(
            url=self.get_query_url(url, number_of_data),
            query_file_path=query_file_path,
            result_file_path=result_file_path,
            max_wait=max_wait,
        )
        return result_file_path

    def get_closest_data_for_model(
        self,
        model_id: str,
        query_file_path: str,
        result_file_path: str,
        number_of_data: Optional[int] = None,
        max_wait: int = DEFAULT_MAX_WAIT,
    ) -> str:
        """Retrieves closest data points to the data point in input file.

        Parameters
        ----------
        model_id: str
            Id of the model to search for the closest data points
        query_file_path: str
            Path to file with the data point to search closest data points
        result_file_path: str
            Path where to save the result file
        number_of_data: int or None
            Number of results to search for. If no value specified, the default is 10.
        max_wait: int
            Number of seconds to wait for the result. Default is 600.

        Returns
        -------
        Path where the result was saved
        """
        url = self._get_closest_data_model_path.format(
            project_id=self.project_id, model_id=model_id
        )
        self._get_closest_data(
            url=self.get_query_url(url, number_of_data),
            query_file_path=query_file_path,
            result_file_path=result_file_path,
            max_wait=max_wait,
        )
        return result_file_path

    def get_closest_data_for_featurelist(
        self,
        featurelist_id: str,
        query_file_path: str,
        result_file_path: str,
        number_of_data: Optional[int] = None,
        max_wait: int = DEFAULT_MAX_WAIT,
    ) -> str:
        """Retrieves closest data points to the data point in input file.

        Parameters
        ----------
        featurelist_id: str
            Id of the featurelist to search for the closest data points
        query_file_path: str
            Path to file with the data point to search closest data points
        result_file_path: str
            Path where to save the result file
        number_of_data: int or None
            Number of results to search for. If no value specified, the default is 10.
        max_wait: int
            Number of seconds to wait for the result. Default is 600.

        Returns
        -------
        Path where the result was saved
        """
        url = self._get_closest_data_featurelist_path.format(
            project_id=self.project_id, featurelist_id=featurelist_id
        )
        self._get_closest_data(
            url=self.get_query_url(url, number_of_data),
            query_file_path=query_file_path,
            result_file_path=result_file_path,
            max_wait=max_wait,
        )
        return result_file_path

    def build_index(self, max_wait: int = DEFAULT_MAX_WAIT) -> None:
        """Builds data matching index and waits for its completion.

        Parameters
        ----------
        max_wait: int or None
            Seconds to wait for the completion of build index operation.
            Default is 600. When the 0 or None value is passed then
            the method will exit without awaiting for the build index
            operation to complete.
        """
        url = self._build_index_path.format(project_id=self.project_id)
        response = self._client.post(url)
        if max_wait:
            wait_for_async_resolution(self._client, response.headers["Location"], max_wait)

    def build_index_for_featurelist(
        self, featurelist_id: str, max_wait: int = DEFAULT_MAX_WAIT
    ) -> None:
        """Builds data matching index for featurelist and waits for its completion.

        Parameters
        ----------
        featurelist_id: str
            Id of the featurelist to build the index for
        max_wait: int or None
            Seconds to wait for the completion of build index operation.
            Default is 600. When the 0 or None value is passed then
            the method will exit without awaiting for the build index
            operation to complete.
        """
        url = self._build_index_featurelist_path.format(
            project_id=self.project_id, featurelist_id=featurelist_id
        )
        response = self._client.post(url)
        if max_wait:
            wait_for_async_resolution(self._client, response.headers["Location"], max_wait)

    def build_index_for_model(self, model_id: str, max_wait: int = DEFAULT_MAX_WAIT) -> None:
        """Builds data matching index for feature list and waits for its completion.

        Parameters
        ----------
        model_id: str
            Id of the model to build index for
        max_wait: int or None
            Seconds to wait for the completion of build index operation.
            Default is 600. When the 0 or None value is passed then
            the method will exit without awaiting for the build index
            operation to complete.
        """
        url = self._build_index_model_path.format(project_id=self.project_id, model_id=model_id)
        response = self._client.post(url)
        if max_wait:
            wait_for_async_resolution(self._client, response.headers["Location"], max_wait)

    def list(self) -> List["DataMatchingQuery"]:
        """Lists all data matching queries for the project. Results are sorted in descending order
        starting from the latest to the oldest.

        Returns
        -------
        List[DataMatchingQuery]
        """
        return DataMatchingQuery.list(self.project_id)


class DataMatchingQuery(APIObject):
    """
    Data Matching Query object.

    Represents single query for the closest data points. Once related query job is completed,
    its result can be retrieved and saved as csv file in specified location.
    """

    _list_path = "projects/{project_id}/dataMatchingRecords/"
    _retrieve_path = "projects/{project_id}/dataMatchingRecords/{data_matching_id}/"

    _converter = t.Dict(
        {
            t.Key("data_matching_id"): t.String(),
            t.Key("project_id"): t.String(),
            t.Key("dataset_id"): t.String(),
            t.Key("model_id", optional=True): t.String(),
            t.Key("user_id"): t.String(),
            t.Key("job_status_id"): t.String(),
            t.Key("number_of_data"): t.String(),
            t.Key("requested_at"): t.String(),
        }
    ).ignore_extra("*")

    def __init__(self, data_matching_id: str, project_id: str, **kwargs: Any) -> None:
        self.data_matching_id = data_matching_id
        self.project_id = project_id
        self.dataset_id = kwargs.get("dataset_id")
        self.model_id = kwargs.get("model_id")
        self.user_id = kwargs.get("user_id")
        self.job_status_id = kwargs.get("job_status_id")
        self.number_of_data = kwargs.get("number_of_data")
        self.requested_at = kwargs.get("requested_at")

    def __repr__(self) -> str:
        tokens = [f"{k}={v}" for k, v in self.__dict__.items() if v is not None]
        return f"DataMatchingQuery({','.join(tokens)})"

    @classmethod
    def list(cls, project_id: str) -> List["DataMatchingQuery"]:
        """Retrieves the list of queries.

        Parameters
        ----------
        project_id: str
            Project ID to retrieve data matching queries for

        Returns
        -------
        List[DataMatchingQuery]
        """
        path = cls._list_path.format(project_id=project_id)
        return [cls.from_server_data(x) for x in pagination.unpaginate(path, {}, cls._client)]

    def save_result(self, file_path: str) -> None:
        """Downloads the query result and saves it in file_path location.

        Parameters
        ----------
        file_path: str
            Path location where to save the query result

        """
        url = self._retrieve_path.format(
            project_id=self.project_id, data_matching_id=self.data_matching_id
        )
        response = self._client.get(url)
        with open(file_path, "wb") as f:
            f.write(response.content)
