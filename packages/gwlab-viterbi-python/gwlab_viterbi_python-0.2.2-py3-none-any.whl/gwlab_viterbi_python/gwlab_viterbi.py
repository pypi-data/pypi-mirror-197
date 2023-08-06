import itertools
from dataclasses import asdict

from gwdc_python import GWDC
from gwdc_python.files import FileReference, FileReferenceList
from gwdc_python.helpers import TimeRange
from gwdc_python.utils import rename_dict_keys
from gwdc_python.logger import create_logger

from .viterbi_job import ViterbiJob
from .inputs import DataInput, DataParametersInput, SearchParametersInput
from .exceptions import custom_error_handler
from .utils.file_download import _download_files, _save_file_map_fn, _get_file_map_fn
from .settings import GWLAB_VITERBI_ENDPOINT, GWLAB_VITERBI_AUTH_ENDPOINT

logger = create_logger(__name__)


class GWLabViterbi:
    def __init__(self, token, auth_endpoint=GWLAB_VITERBI_AUTH_ENDPOINT, endpoint=GWLAB_VITERBI_ENDPOINT):
        self.client = GWDC(
            token=token,
            auth_endpoint=auth_endpoint,
            endpoint=endpoint,
            custom_error_handler=custom_error_handler
        )
        self.request = self.client.request

    def start_viterbi_job(
        self, job_name, job_description, private, data_input=None, data_params=None, search_params=None
    ):
        """Start a viterbi job from inputs

        Parameters
        ----------
        job_name : str
            Name of the job to be created
        job_description : str
            Description of the job to be created
        private : bool
            True if the job should be private, False if it should be public
        data_input : DataInput
            Data inputs for the job, by default None.
            If None, then default inputs will be used for these fields.
        data_params : DataParametersInput
            Data parameters inputs for the job, by default None.
            If None, then default inputs will be used for these fields.
        search_params : SearchParametersInput
            Search parameters inputs for the job, by default None.
            If None, then default inputs will be used for these fields.

        Returns
        -------
        ViterbiJob
            Created job
        """
        query = """
            mutation NewViterbiJob($input: ViterbiJobMutationInput!){
                newViterbiJob (input: $input) {
                    result {
                        jobId
                    }
                }
            }
        """

        data_inputs = DataInput() if data_input is None else data_input
        data_parameters_inputs = DataParametersInput() if data_params is None else data_params
        search_parameters_inputs = SearchParametersInput() if search_params is None else search_params

        variables = {
            "input": {
                "start": {
                    "name": job_name,
                    "description": job_description,
                    "private": private,
                },
                "data": asdict(data_inputs),
                "data_parameters": asdict(data_parameters_inputs),
                "search_parameters": asdict(search_parameters_inputs),
            }
        }

        data = self.request(query=query, variables=variables)

        job_id = data['new_viterbi_job']['result']['job_id']
        return self.get_job_by_id(job_id)

    def _get_job_model_from_query(self, query_data):
        if not query_data:
            return None

        return ViterbiJob(
            client=self,
            **rename_dict_keys(
                query_data,
                {'id': 'job_id'}
            )
        )

    def get_public_job_list(self, search="", time_range=TimeRange.ANY, number=100):
        """Obtains a list of public Viterbi jobs, filtering based on the search terms
        and the time range within which the job was created.

        Parameters
        ----------
        search : str, optional
            Search terms by which to filter public job list, by default ""
        time_range : .TimeRange or str, optional
            Time range by which to filter job list, by default TimeRange.ANY
        number : int, optional
            Number of job results to return in one request, by default 100

        Returns
        -------
        list
            List of ViterbiJob instances for the jobs corresponding to the search terms and in the specified time range
        """
        query = """
            query ($search: String, $timeRange: String, $first: Int){
                publicViterbiJobs (search: $search, timeRange: $timeRange, first: $first) {
                    edges {
                        node {
                            id
                            user
                            name
                            description
                            jobStatus {
                                name
                                date
                            }
                        }
                    }
                }
            }
        """

        variables = {
            "search": search,
            "time_range": time_range.value if isinstance(time_range, TimeRange) else time_range,
            "first": number
        }

        data = self.request(query=query, variables=variables)

        if not data['public_viterbi_jobs']['edges']:
            logger.info('Job search returned no results.')
            return []

        return [self._get_job_model_from_query(job['node']) for job in data['public_viterbi_jobs']['edges']]

    def get_job_by_id(self, job_id):
        """Get a Viterbi job instance corresponding to a specific job ID

        Parameters
        ----------
        job_id : str
            ID of job to obtain

        Returns
        -------
        ViterbiJob
            ViterbiJob instance corresponding to the input ID
        """
        query = """
            query ($id: ID!){
                viterbiJob (id: $id) {
                    id
                    name
                    user
                    description
                    jobStatus {
                        name
                        date
                    }
                }
            }
        """

        variables = {
            "id": job_id
        }

        data = self.request(query=query, variables=variables)

        if not data['viterbi_job']:
            logger.info('No job matching input ID was returned.')
            return None

        return self._get_job_model_from_query(data['viterbi_job'])

    def get_user_jobs(self, number=100):
        """Obtains a list of Viterbi jobs created by the user, filtering based on the search terms
        and the time range within which the job was created.

        Parameters
        ----------
        number : int, optional
            Number of job results to return in one request, by default 100

        Returns
        -------
        list
            List of ViterbiJob instances for the jobs corresponding to the search terms and in the specified time range
        """
        query = """
            query ($first: Int){
                viterbiJobs (first: $first){
                    edges {
                        node {
                            id
                            name
                            user
                            description
                            jobStatus {
                                name
                                date
                            }
                        }
                    }
                }
            }
        """

        variables = {
            "first": number
        }

        data = self.request(query=query, variables=variables)

        return [self._get_job_model_from_query(job['node']) for job in data['viterbi_jobs']['edges']]

    def _get_files_by_job_id(self, job_id):
        query = """
            query ($jobId: ID!) {
                viterbiResultFiles (jobId: $jobId) {
                    files {
                        path
                        isDir
                        fileSize
                        downloadToken
                    }
                }
            }
        """

        variables = {
            "job_id": job_id
        }

        data = self.request(query=query, variables=variables)

        file_list = FileReferenceList()
        for file_data in data['viterbi_result_files']['files']:
            if file_data['is_dir']:
                continue
            file_data.pop('is_dir')
            file_list.append(
                FileReference(
                    **file_data,
                    job_id=job_id,
                )
            )

        return file_list, False

    def get_files_by_reference(self, file_references):
        """Obtains file data when provided a FileReferenceList

        Parameters
        ----------
        file_references : FileReferenceList
            Contains the :class:`FileReference` objects for which to download the contents

        Returns
        -------
        list
            List of tuples containing the file path and file contents as a byte string
        """
        batched = file_references.batched

        file_ids = [
            self._get_download_ids_from_tokens(job_id, job_files.get_tokens())
            for job_id, job_files in batched.items()
        ]

        file_ids = list(itertools.chain.from_iterable(file_ids))
        batched_files = FileReferenceList(list(itertools.chain.from_iterable(batched.values())))

        file_paths = batched_files.get_paths()
        total_size = batched_files.get_total_bytes()

        files = _download_files(_get_file_map_fn, file_ids, file_paths, total_size)

        logger.info(f'All {len(file_ids)} files downloaded!')

        return files

    def save_files_by_reference(self, file_references, root_path, preserve_directory_structure=True):
        """Save files when provided a FileReferenceList and a root path

        Parameters
        ----------
        file_references : FileReferenceList
            Contains the :class:`FileReference` objects for which to save the associated files
        root_path : str or ~pathlib.Path
            Directory into which to save the files
        preserve_directory_structure : bool, optional
            Remove any directory structure for the downloaded files, by default True
        """
        batched = file_references.batched

        file_ids = [
            self._get_download_ids_from_tokens(job_id, job_files.get_tokens())
            for job_id, job_files in batched.items()
        ]

        file_ids = list(itertools.chain.from_iterable(file_ids))
        batched_files = FileReferenceList(list(itertools.chain.from_iterable(batched.values())))

        file_paths = batched_files.get_output_paths(root_path, preserve_directory_structure)
        total_size = batched_files.get_total_bytes()

        _download_files(_save_file_map_fn, file_ids, file_paths, total_size)

        logger.info(f'All {len(file_ids)} files saved!')

    def _get_download_id_from_token(self, job_id, file_token):
        """Get a single file download id for a file download token

        Parameters
        ----------
        job_id : str
            Job id which owns the file token

        file_token : str
            Download token for the desired file

        Returns
        -------
        str
            Download id for the desired file
        """
        return self._get_download_ids_from_tokens(job_id, [file_token])[0]

    def _get_download_ids_from_tokens(self, job_id, file_tokens):
        """Get many file download ids for a list of file download tokens

        Parameters
        ----------
        job_id : str
            Job id which owns the file token

        file_tokens : list
            Download tokens for the desired files

        Returns
        -------
        list
            List of download ids for the desired files
        """
        query = """
            mutation ResultFileMutation($input: GenerateFileDownloadIdsInput!) {
                generateFileDownloadIds(input: $input) {
                    result
                }
            }
        """

        variables = {
            "input": {
                "job_id": job_id,
                "download_tokens": file_tokens
            }
        }

        data = self.request(query=query, variables=variables)

        return data['generate_file_download_ids']['result']
