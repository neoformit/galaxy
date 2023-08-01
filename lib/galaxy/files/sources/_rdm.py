import logging
from typing import (
    cast,
    List,
    NamedTuple,
    Optional,
)

from typing_extensions import Unpack

from galaxy.files import ProvidesUserFileSourcesUserContext
from galaxy.files.sources import (
    BaseFilesSource,
    FilesSourceProperties,
    PluginKind,
    RemoteDirectory,
    RemoteFile,
)

log = logging.getLogger(__name__)

OptionalUserContext = Optional[ProvidesUserFileSourcesUserContext]


class RDMFilesSourceProperties(FilesSourceProperties):
    url: str


class RecordFilename(NamedTuple):
    record_id: str
    filename: str


class RDMRepositoryInteractor:
    """Base class for interacting with an external RDM repository.

    This class is not intended to be used directly, but rather to be subclassed
    by file sources that interact with RDM repositories.
    """

    def __init__(self, repository_url: str, plugin: BaseFilesSource):
        self._repository_url = repository_url
        self._plugin = plugin

    @property
    def plugin(self) -> BaseFilesSource:
        """Returns the plugin associated with this repository interactor."""
        return self._plugin

    @property
    def repository_url(self) -> str:
        """Returns the base URL of the repository.

        Example: https://zenodo.org
        """
        return self._repository_url

    def to_plugin_uri(self, record_id: str, filename: Optional[str] = None) -> str:
        """Creates a valid plugin URI to reference the given record_id.

        If a filename is provided, the URI will reference the specific file in the record."""
        raise NotImplementedError()

    def get_records(self, writeable: bool, user_context: OptionalUserContext = None) -> List[RemoteDirectory]:
        """Returns the list of records in the repository.

        If writeable is True, only records that the user can write to will be returned.
        The user_context might be required to authenticate the user in the repository.
        """
        raise NotImplementedError()

    def get_files_in_record(
        self, record_id: str, writeable: bool, user_context: OptionalUserContext = None
    ) -> List[RemoteFile]:
        """Returns the list of files contained in the given record.

        If writeable is True, we are signaling that the user intends to write to the record.
        """
        raise NotImplementedError()

    def create_draft_record(self, title: str, user_context: OptionalUserContext = None):
        """Creates a draft record (directory) in the repository with basic metadata.

        The metadata is usually just the title of the record and the user that created it.
        Some plugins might also provide additional metadata defaults in the user settings."""
        raise NotImplementedError()

    def upload_file_to_draft_record(
        self,
        record_id: str,
        filename: str,
        file_path: str,
        user_context: OptionalUserContext = None,
    ) -> None:
        """Uploads a file with the provided filename (from file_path) to a draft record with the given record_id.

        The draft record must have been created in advance with the `create_draft_record` method.
        The file must exist in the file system at the given file_path.
        The user_context might be required to authenticate the user in the repository.
        """
        raise NotImplementedError()

    def download_file_from_record(
        self,
        record_id: str,
        filename: str,
        file_path: str,
        user_context: OptionalUserContext = None,
    ) -> None:
        """Downloads a file with the provided filename from the record with the given record_id.

        The file will be downloaded to the file system at the given file_path.
        The user_context might be required to authenticate the user in the repository if the
        file is not publicly available.
        """
        raise NotImplementedError()


class RDMFilesSource(BaseFilesSource):
    """Base class for Research Data Management (RDM) file sources.

    This class is not intended to be used directly, but rather to be subclassed
    by file sources that interact with RDM repositories.

    A RDM file source is similar to a regular file source, but instead of tree of
    files and directories, it provides a (one level) list of records (representing directories)
    that can contain only files (no subdirectories).

    In addition, RDM file sources might need to create a new record (directory) in advance in the
    repository, and then upload a file to it. This is done by calling the `create_entry`
    method.

    """

    plugin_kind = PluginKind.rdm

    def __init__(self, **kwd: Unpack[FilesSourceProperties]):
        props = self._parse_common_config_opts(kwd)
        base_url = props.get("url", None)
        if not base_url:
            raise Exception("URL for RDM repository must be provided in configuration")
        self._repository_url = base_url
        self._props = props
        self._repository_interactor = self.get_repository_interactor(base_url)

    @property
    def repository(self) -> RDMRepositoryInteractor:
        return self._repository_interactor

    def get_repository_interactor(self, repository_url: str) -> RDMRepositoryInteractor:
        """Returns an interactor compatible with the given repository URL.

        This must be implemented by subclasses."""
        raise NotImplementedError()

    def parse_path(self, source_path: str) -> RecordFilename:
        # source_path has always the format: '/{record_id}/{file_name}'
        record_id = source_path.split("/")[1]
        filename = source_path.split("/")[-1]
        return RecordFilename(record_id=record_id, filename=filename)

    def _serialization_props(self, user_context: OptionalUserContext = None) -> RDMFilesSourceProperties:
        effective_props = {}
        for key, val in self._props.items():
            effective_props[key] = self._evaluate_prop(val, user_context=user_context)
        effective_props["url"] = self._repository_url
        return cast(RDMFilesSourceProperties, effective_props)
