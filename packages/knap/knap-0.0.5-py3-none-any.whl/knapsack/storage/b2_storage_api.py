

class B2StorageApi(CloudStorageApi):
    def __init__(
        self,
        capabilities_to_accounts: Dict[str, Any],
    ) -> None:
        self.capabilities_to_accounts = capabilities_to_accounts

    def upload_file():
        pass

    def to_dict(self) -> Dict[str, Any]:
        return self.capabilities_to_accounts

    def __str__(self):
        return str(self.to_dict())

    def __repr__(self):
        return self.__str__()

    def to_json(self):
        return self.to_dict()

    @staticmethod
    def from_json(json_dict: dict):
        return B2StorageApi(capabilities_to_accounts=json_dict["capabilities_to_accounts"])
