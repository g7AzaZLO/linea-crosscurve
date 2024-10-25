import random
import time
from classes.chain import chains
from classes.client import Client
from modules.crosscurve.logic import get_swap_route, get_estimate, create_swap_transaction, \
    send_crosscurve_swap_transaction
from utils.read_utils import read_file


def main():
    print("Выберите путь:")
    print("1. Arb to Linea")
    print("2. Linea to Arb")
    route = input("-> ")
    print("Введите количество эфира для свапа(по стандарту стоит 0.0051 arb->linea, 0.00495 linea->arb)")
    vol = input("-> ")
    pk = read_file("wallets.txt")
    if route == '1':
        for acc in pk:
            if vol == "":
                arb_to_linea(acc)
            else:
                arb_to_linea(acc, float(vol))
            time.sleep(random.randint(1, 300))
        print("ALL SWAP DONE")
    if route == '2':
        for acc in pk:
            if vol == "":
                linea_to_arb(acc)
            else:
                linea_to_arb(acc, float(vol))
            time.sleep(random.randint(1, 300))
        print("ALL SWAP DONE")


def arb_to_linea(pk: str, amount: float = 0.0051) -> None:
    client = Client(pk, chains["arbitrum"].rpc)
    route = get_swap_route(chains["arbitrum"], "ETH", chains["linea"], "ETH", amount, 0.1)["route"]
    estimate = get_estimate(route)
    swap_tnx = create_swap_transaction(client.public_key, route, estimate)
    send_crosscurve_swap_transaction(client, swap_tnx, estimate)


def linea_to_arb(pk: str, amount: float = 0.00495) -> None:
    client = Client(pk, chains["linea"].rpc)
    route = get_swap_route(chains["linea"], "ETH", chains["arbitrum"], "ETH", amount, 0.1)["route"]
    estimate = get_estimate(route)
    swap_tnx = create_swap_transaction(client.public_key, route, estimate)
    send_crosscurve_swap_transaction(client, swap_tnx, estimate)


main()
