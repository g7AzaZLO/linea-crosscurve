from web3 import Web3, HTTPProvider


class Client:
    def __init__(self, private_key: str, rpc: str, proxy: str = None):
        """
        Инициализирует клиента с подключением к RPC через прокси и настройкой аккаунта на основе приватного ключа.

        :param private_key: Приватный ключ в шестнадцатеричном формате (с или без префикса '0x').
        :param rpc: URL RPC-сервера.
        :param proxy: URL прокси-сервера (например '312.123.43.43:8080').
        :raises ConnectionError: Если не удается подключиться к RPC.
        """
        print(f"Initializing client with proxy {proxy}")

        self.rpc = rpc
        self.proxy = proxy

        # Настройка провайдера с учетом прокси
        if self.proxy:
            provider = HTTPProvider(self.rpc, {"proxies": {"http": self.proxy}})
        else:
            provider = HTTPProvider(self.rpc)

        self.connection = Web3(provider)

        # Проверка подключения к RPC
        if not self.connection.is_connected():
            print(f"Failed to connect to the RPC at {self.rpc}")
            raise ConnectionError(f"Failed to connect to the RPC at {self.rpc}")

        self.chain_id = self.connection.eth.chain_id

        # Обработка приватного ключа
        self.private_key = bytes.fromhex(private_key[2:] if private_key.startswith('0x') else private_key)
        self.account = self.connection.eth.account.from_key(self.private_key)
        self.public_key = self.account.address

        print(f"Client initialized with public_key={self.public_key}")

    def __del__(self) -> None:
        """
        Сообщает, что клиент был удален.
        """
        print(f"Client with public_key={self.public_key} was deleted")

    def __str__(self) -> str:
        """
        Возвращает строковое представление клиента.
        """
        return (
            f"Client(\n"
            f"  public_key={self.public_key},\n"
            f"  private_key={'0x' + self.private_key.hex()},\n"
            f"  rpc={self.rpc},\n"
            f"  proxy={self.proxy},\n"
            f")"
        )

    def get_nonce(self, address: str = None) -> int | None:
        """
        Получает текущий nonce для учетной записи.

        :param address: Адрес учетной записи. Если не указан, используется публичный ключ клиента.
        :return: Nonce для учетной записи.
        """
        if address is None:
            address = self.public_key
        print(f"Getting nonce for address {address}")
        try:
            nonce = self.connection.eth.get_transaction_count(address)
            print(f"Nonce for address {address}: {nonce}")
            return nonce
        except Exception as e:
            print(f"Error occurred while getting nonce for address {address}: {e}")
            return None