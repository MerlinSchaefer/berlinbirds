import os
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, BlobProperties

class BlobStorageHandler:
    """Class to handle blob storage operations for Azure."""

    def __init__(self, container_name: str, storage_account_name: str | None = None, connection_string: str | None = None) -> None:
        """Initialize BlobStorageHandler with Azure connection settings.
        
        Args:
            container_name (str): Name of the blob container.
            storage_account_name (str, optional): Name of the Azure Storage Account.
            connection_string (str, optional): Connection string for Azure Storage.
        
        Raises:
            ValueError: If neither connection_string nor storage_account_name is provided.
        """
        if connection_string:
            self.blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        elif storage_account_name:
            account_url = f"https://{storage_account_name}.blob.core.windows.net"
            default_credential = DefaultAzureCredential()
            self.blob_service_client = BlobServiceClient(account_url, credential=default_credential)
        else:
            raise ValueError("Either connection_string or storage_account_name must be provided.")
        
        self.container_name = container_name

    def upload_blob(self, filename: str, file_path: str) -> None:
        """Upload a file to an Azure Blob Storage container.
        
        Args:
            filename (str): Blob name under which to store the file.
            file_path (str): Local path to the file to upload.
        """
        blob_client = self.blob_service_client.get_blob_client(container=self.container_name, blob=filename)
        with open(file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)

    def download_blob(self, filename: str, download_file_path: str) -> None:
        """Download a blob from Azure Blob Storage.
        
        Args:
            filename (str): Name of the blob to download.
            download_file_path (str): Local path where the blob should be saved.
        """
        blob_client = self.blob_service_client.get_blob_client(container=self.container_name, blob=filename)
        with open(download_file_path, "wb") as download_file:
            download_file.write(blob_client.download_blob().readall())

    def delete_blob(self, filename: str) -> None:
        """Delete a blob from Azure Blob Storage.
        
        Args:
            filename (str): Name of the blob to delete.
        """
        blob_client = self.blob_service_client.get_blob_client(container=self.container_name, blob=filename)
        blob_client.delete_blob()

    def list_blobs(self) -> list[BlobProperties]:
        """List all blobs in the container.
        
        Returns:
            list[BlobProperties]: List of blobs in the container.
        """
        container_client = self.blob_service_client.get_container_client(self.container_name)
        return list(container_client.list_blobs())

    def update_blob(self, filename: str, file_path: str) -> None:
        """Replace an existing blob with a new file.
        
        Args:
            filename (str): Name of the blob to update.
            file_path (str): Local path of the new file to upload.
        """
        self.delete_blob(filename)
        self.upload_blob(filename, file_path)

