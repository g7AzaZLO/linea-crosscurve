class Chain:
    def __init__(self, name: str, chain_id: int, rpc: str, native_token: str, alternative_rpc: list[str]):
        self.name = name
        self.id = chain_id
        self.rpc = rpc
        self.native_token = native_token
        self.alternative_rpc = alternative_rpc
        self.current_rpc_index = 0

    def set_rpc_url(self, url: str) -> bool:
        self.rpc = url
        return True

    def switch_to_alternative_rpc(self) -> bool:
        if self.current_rpc_index < len(self.alternative_rpc):
            self.rpc = self.alternative_rpc[self.current_rpc_index]
            self.current_rpc_index += 1
            return True
        else:
            print(f"No more alternative RPCs available for chain {self.name}")
            return False

    @classmethod
    def get(cls, identifier: str | int) -> dict | None:
        """
        Получает информацию о сети по названию или идентификатору сети.

        :param identifier: Название сети (str) или идентификатор сети (int).
        :return: Словарь с информацией о сети, если найдена, иначе None.
        """
        for chain in chains.values():
            if (isinstance(identifier, str) and chain.name.lower() == identifier.lower()) or \
               (isinstance(identifier, int) and chain.id == identifier):
                return {
                    "name": chain.name,
                    "chain_id": chain.id,
                    "rpc": chain.rpc,
                    "native_token": chain.native_token,
                    "alternative_rpc": chain.alternative_rpc
                }
        print("Chain not found.")
        return None


chains = {
    "arbitrum": Chain(
        'arbitrum',
        42161,
        "https://arbitrum.llamarpc.com",
        "ETH",
        ["https://arbitrum.drpc.org", "https://1rpc.io/arb", "https://arb-pokt.nodies.app","https://arbitrum.meowrpc.com"]),
    "linea": Chain(
        'linea',
        59144,
        "https://linea-rpc.publicnode.com",
        "ETH",
        ["https://rpc.linea.build", "https://linea.blockpi.network/v1/rpc/public"]),
}
