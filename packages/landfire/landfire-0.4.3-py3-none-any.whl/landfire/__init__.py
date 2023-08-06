"""Landfire data accessor."""
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import requests
from attrs import AttrsInstance, define, field, validators
from requests import Response
from tqdm import tqdm

from landfire.product.search import ProductSearch


__all__ = ["landfire"]

# URLs for making requests to LANDFIRE ArcGIS Rest Service
BASE_URL = "https://lfps.usgs.gov/arcgis/rest/services/LandfireProductService/GPServer/LandfireProductService"
REQUEST_URL = BASE_URL + "/submitJob?"
JOB_URL = BASE_URL + "/jobs/"


@define
class Landfire:
    """Accessor for LANDFIRE data.

    Args:
        bbox: Bounding box with form `min_x min_y max_x max_y`. For example, `-107.70894965 46.56799094 -106.02718124 47.34869094`. Use geospatial util func `get_bbox_from_polygon()` to convert a GeoJSON Polygon object or get_bbox_from_file() to convert a file to a suitable bounding box if needed.
        output_crs: Output coordinate reference system in well-known integer ID (WKID) format (EPSG). Defaults to None to preserve localized Albers projection from LANDFIRE needed for most fire models (FlamMap, FARSITE, etc.). A commonly used value for other purposes is `4326` for WGS84. See https://epsg.io for a full list of EPSG WKIDs.
        resample_res: Resolution in meters for resampling output data. Defaults to 30 meters. Acceptable values are 30 to 9999 meters.
    """

    bbox: str = field(validator=validators.instance_of(str))
    resample_res: int = field(default=30, validator=validators.instance_of(int))
    output_crs: Union[str, None] = field(
        default=None,
        validator=validators.optional(validators.instance_of(str)),
    )
    # Private attrs that will be set in post_init()
    _search = field(init=False, validator=validators.instance_of(ProductSearch))
    _all_layers = field(init=False, validator=validators.instance_of(list))
    _base_params = field(init=False, validator=validators.instance_of(dict))
    _session = field(init=False, validator=validators.instance_of(requests.Session))

    def __attrs_post_init__(self) -> None:
        """Post initialization setup."""
        # instantiate products for searching
        self._search = ProductSearch()

        # for validation
        self._all_layers = self._search.get_layers()

        # base param payload
        self._base_params = {
            "Area_Of_Interest": self.bbox,
            "Output_Projection": self.output_crs,
            "f": "JSON",
        }

        # api will fail if 30 is provided to Resample_Resolution. Handle here instead of confusing  user to provide None when they want 30m.
        if self.resample_res != 30:
            self._base_params["Resample_Resolution"] = self.resample_res

    @resample_res.validator
    def _resample_range_check(self, attribute: AttrsInstance, value: int) -> None:
        """Ensure resampling resolution is within allowable range."""
        if not 30 <= value <= 9999:
            raise ValueError("resample_res must be between 30 and 9999 meters.")

    def _write_status(
        self, msg: str, progress_bar: tqdm, show_status: bool = True
    ) -> None:
        """Write progress bar status.

        Args:
            msg: Message to write.
            progress_bar: tqdm progress bar instance.
            show_status: Whether to log message.
        """
        if show_status:
            progress_bar.write(msg)

    def _validate_layers(self, layers: List[str]) -> None:
        """Validate user provided layers are available for download.

        Args:
            layers: List of user provided layers to validate.

        Raises:
            RuntimeError: If user provided layers do not match possible layers available for download.

        """
        try:
            assert all(layer in self._all_layers for layer in layers)
        except AssertionError:
            raise RuntimeError(
                "Specified layers do not match available layers from the LANDFIRE API. Please check your layer list and try again!"
            )

    def _validate_user_output_path(self, output_path: str) -> Path:
        """Validate user provided output_path is valid.

        Args:
            output_path: User provided output path.

        Returns:
            output_path as a Path object.

        Raises:
            RuntimeError: If user provided path parent directory doesn't exist or the file name doesn't have the `.zip` extension.
        """
        try:
            path_obj = Path(output_path)
            assert path_obj.suffix == ".zip"
        except AssertionError:
            raise RuntimeError(
                f"{output_path} is not valid! Verify the path exists and the file name ends in `.zip`."
            )
        return path_obj

    def _write_resp_to_file(self, response: Response, final_path: Path) -> None:
        """Write final .zip output to user provided path.

        Args:
            response: Response object from API
            final_path: Path object to write file to

        """
        # Write to provided output path
        with open(final_path, "wb") as fd:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                fd.write(chunk)

    def _submit_request(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        stream: Optional[bool] = None,
    ) -> Response:
        """Tiny wrapper around requests.get() since we need to make four calls.

        Args:
            url: Request url.
            params: Request parameters payload.
            stream: Whether to stream the response.

        Returns:
            Response object.
        """
        submit_req = requests.get(url=url, params=params, stream=stream, timeout=600)
        submit_req.raise_for_status()
        return submit_req

    def request_data(
        self,
        layers: List[str],
        output_path: str,
        show_status: bool = True,
        backoff_base_value: int = 5,
    ) -> None:
        """Request particular layers from Landfire to be output as a zipped .tif.

        NOTE: this function has no return, data will simply be downloaded to the specified `output_path`.

        NOTE: this function implements a linear backoff strategy, polling for job status every 5 seconds by default. Depending on the size of your job, it may take several seconds or minutes to process. You may change this with the `backoff_base_value`.

        Args:
            layers: List of product layers.
            output_path: Path-like string where data will be downloaded to. Include 'empty' file name and .zip extension. For example, `~/tmp/my_landfire_data/output.zip`.
            show_status: Whether to write (True) or suppress (False) progress bar and status update output for data request.
            backoff_base_value: Base time in seconds for linear backoff strategy. This is used to query the job API periodically for status while avoiding making too many requests. Please be courteous with this parameter as it will directly affect the number of calls to the LANDFIRE API!

        Raises:
            RuntimeError: If provided layers are not valid, if output_path does not exist, or if an unexpected error occurs when processing requested data.
        """
        # User input validation
        self._validate_layers(layers)
        final_path: Path = self._validate_user_output_path(output_path)

        # Add layer list to base_params
        self._base_params["Layer_List"] = ";".join(layers)

        # Init progress
        if show_status:
            pbar = tqdm(
                total=100,
                desc="Job Status",
                file=sys.stdout,
                bar_format="{l_bar}{bar} [Total Duration: {elapsed}]",
            )
        else:
            pbar = tqdm(total=100, disable=True)

        # Submit initial request for layers
        self._write_status("Submitting job...", pbar, show_status)
        submit_job_req = self._submit_request(
            REQUEST_URL, params=self._base_params, stream=False
        ).json()

        # Get job id, check status of processing with backoff
        if "jobId" in submit_job_req:
            job_id = submit_job_req["jobId"]
            status = submit_job_req["jobStatus"]

            pbar.update(25)
            self._write_status(
                "Job submitted! Processing layers... ⏱️", pbar, show_status
            )

            job_url = JOB_URL + job_id
            n = 0
            while status == "esriJobSubmitted" or status == "esriJobExecuting":
                # Backoff logic
                n += 1
                backoff_sec = backoff_base_value * n
                self._write_status(
                    f"Checking status of job again in {backoff_sec} seconds... 💤",
                    pbar,
                    show_status,
                )
                time.sleep(backoff_sec)

                # Get job status
                status_job_req = self._submit_request(
                    url=job_url, params={"f": "json"}, stream=False
                ).json()

                if "jobStatus" in status_job_req:
                    status = status_job_req["jobStatus"]
                    # Get latest processing status
                    if status_job_req["messages"]:
                        latest_status_msg = status_job_req["messages"][-1][
                            "description"
                        ]
                    else:
                        latest_status_msg = "No message yet!"

                    # Obtain data results url
                    if status == "esriJobSucceeded":
                        data_path = status_job_req["results"]["Output_File"]["paramUrl"]
                        results_url = job_url + "/" + data_path

                        pbar.update(25)
                        self._write_status(
                            "Job complete! Getting path to .zip file... 🙏",
                            pbar,
                            show_status,
                        )

                        # Get zip file url
                        data_job_req = self._submit_request(
                            results_url, params={"f": "json"}, stream=False
                        ).json()
                        zip_url = data_job_req["value"]["url"]

                        pbar.update(25)
                        self._write_status(
                            "Downloading data as .zip file... 🤞",
                            pbar,
                            show_status,
                        )

                        # Last request to get the zip file
                        zip_job_req = self._submit_request(zip_url, stream=True)
                        # Write data to user path
                        self._write_resp_to_file(zip_job_req, final_path)

                        pbar.update(25)
                        self._write_status(
                            f"Data written successfully to {output_path}! 🎉",
                            pbar,
                            show_status,
                        )
                        pbar.close()

                    # Still executing, display most recent processing step
                    elif status in (
                        "esriJobExecuting",
                        "esriJobSubmitted",
                        "esriJobWaiting",
                    ):
                        self._write_status(
                            f"Most recent message is `{latest_status_msg}`",
                            pbar,
                            show_status,
                        )

                    # Fail if processing error
                    else:
                        raise RuntimeError(
                            f"Encountered an error during job processing! Status was `{status}` and message was `{latest_status_msg}`."
                        )
                # Fail if no job status
                else:
                    raise RuntimeError(
                        "Could not obtain job status for job ID. Please try again! If this problem continues, please raise an issue at https://github.com/FireSci/landfire/issues."
                    )
        # Fail if no job id
        else:
            raise RuntimeError(
                "Unable to obtain job ID for request! Please verify your request parameters and try again! If this problem continues, please raise an issue at https://github.com/FireSci/landfire/issues."
            )
