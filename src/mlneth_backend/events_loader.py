#!/usr/bin/env python
# -*- coding: utf-8 -*-
from eth_utils.abi import event_abi_to_log_topic
from web3.utils.events import get_event_data
from web3 import Web3, HTTPProvider, IPCProvider
from web3.contract import ConciseContract
from web3.auto import w3

web3 = Web3(HTTPProvider('https://mainnet.infura.io/5GyJwkluzWFwhA7RI9XY'))
contract_addr = u'0x15dbdB25f870f21eaf9105e68e249E0426DaE916'
abi = [{"constant": False, "inputs": [{"name": "newDelayInSeconds", "type": "uint32"}, {"name": "newCharityAddress", "type": "address"},{"name":"newImagePlacementPriceInWei","type":"uint256"}],"name":"adminContractSettings","outputs":[],"payable":False,"type":"function"},{"constant":False,"inputs":[],"name":"emergencyRefund","outputs":[],"payable":False,"type":"function"},{"constant":False,"inputs":[{"name":"fromX","type":"uint8"},{"name":"fromY","type":"uint8"},{"name":"toX","type":"uint8"},{"name":"toY","type":"uint8"},{"name":"priceForEachBlockInWei","type":"uint256"}],"name":"sellBlocks","outputs":[{"name":"","type":"bool"}],"payable":False,"type":"function"},{"constant":True,"inputs":[{"name":"fromX","type":"uint8"},{"name":"fromY","type":"uint8"},{"name":"toX","type":"uint8"},{"name":"toY","type":"uint8"}],"name":"getAreaPrice","outputs":[{"name":"","type":"uint256"}],"payable":False,"type":"function"},{"constant":True,"inputs":[{"name":"x","type":"uint8"},{"name":"y","type":"uint8"}],"name":"getBlockInfo","outputs":[{"name":"landlord","type":"address"},{"name":"imageID","type":"uint256"},{"name":"sellPrice","type":"uint256"}],"payable":False,"type":"function"},{"constant":False,"inputs":[{"name":"fromX","type":"uint8"},{"name":"fromY","type":"uint8"},{"name":"toX","type":"uint8"},{"name":"toY","type":"uint8"},{"name":"imageSourceUrl","type":"string"},{"name":"adUrl","type":"string"},{"name":"adText","type":"string"}],"name":"placeImage","outputs":[{"name":"","type":"uint256"}],"payable":True,"type":"function"},{"constant":False,"inputs":[{"name":"fromX","type":"uint8"},{"name":"fromY","type":"uint8"},{"name":"toX","type":"uint8"},{"name":"toY","type":"uint8"}],"name":"buyBlocks","outputs":[{"name":"","type":"uint256"}],"payable":True,"type":"function"},{"constant":True,"inputs":[{"name":"userAddress","type":"address"}],"name":"getUserInfo","outputs":[{"name":"referal","type":"address"},{"name":"handshakes","type":"uint8"},{"name":"balance","type":"uint256"},{"name":"activationTime","type":"uint32"},{"name":"banned","type":"bool"},{"name":"userID","type":"uint256"},{"name":"refunded","type":"bool"},{"name":"investments","type":"uint256"}],"payable":False,"type":"function"},{"constant":True,"inputs":[{"name":"userID","type":"uint256"}],"name":"getUserAddressByID","outputs":[{"name":"userAddress","type":"address"}],"payable":False,"type":"function"},{"constant":True,"inputs":[],"name":"getMyInfo","outputs":[{"name":"balance","type":"uint256"},{"name":"activationTime","type":"uint32"}],"payable":False,"type":"function"},{"constant":True,"inputs":[],"name":"getStateInfo","outputs":[{"name":"_numUsers","type":"uint256"},{"name":"_blocksSold","type":"uint16"},{"name":"_totalWeiInvested","type":"uint256"},{"name":"_numImages","type":"uint256"},{"name":"_setting_imagePlacementPriceInWei","type":"uint256"},{"name":"_numNewStatus","type":"uint256"},{"name":"_setting_delay","type":"uint32"}],"payable":False,"type":"function"},{"constant":False,"inputs":[],"name":"withdrawAll","outputs":[],"payable":False,"type":"function"},{"constant":False,"inputs":[{"name":"referal","type":"address"}],"name":"signIn","outputs":[{"name":"","type":"uint256"}],"payable":False,"type":"function"},{"constant":True,"inputs":[{"name":"imageID","type":"uint256"}],"name":"getImageInfo","outputs":[{"name":"fromX","type":"uint8"},{"name":"fromY","type":"uint8"},{"name":"toX","type":"uint8"},{"name":"toY","type":"uint8"},{"name":"imageSourceUrl","type":"string"},{"name":"adUrl","type":"string"},{"name":"adText","type":"string"}],"payable":False,"type":"function"},{"constant":True,"inputs":[],"name":"charityBalance","outputs":[{"name":"","type":"uint256"}],"payable":False,"type":"function"},{"constant":True,"inputs":[],"name":"charityAddress","outputs":[{"name":"","type":"address"}],"payable":False,"type":"function"},{"constant":False,"inputs":[{"name":"violator","type":"address"},{"name":"banViolator","type":"bool"},{"name":"pauseContract","type":"bool"},{"name":"refundInvestments","type":"bool"}],"name":"adminContractSecurity","outputs":[],"payable":False,"type":"function"},{"inputs":[],"type":"constructor"},{"payable":False,"type":"fallback"},{"anonymous":False,"inputs":[{"indexed":False,"name":"ID","type":"uint256"},{"indexed":False,"name":"newUser","type":"address"},{"indexed":False,"name":"invitedBy","type":"address"},{"indexed":False,"name":"activationTime","type":"uint32"}],"name":"NewUser","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"name":"ID","type":"uint256"},{"indexed":False,"name":"fromX","type":"uint8"},{"indexed":False,"name":"fromY","type":"uint8"},{"indexed":False,"name":"toX","type":"uint8"},{"indexed":False,"name":"toY","type":"uint8"},{"indexed":False,"name":"price","type":"uint256"}],"name":"NewAreaStatus","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"name":"ID","type":"uint256"},{"indexed":False,"name":"fromX","type":"uint8"},{"indexed":False,"name":"fromY","type":"uint8"},{"indexed":False,"name":"toX","type":"uint8"},{"indexed":False,"name":"toY","type":"uint8"},{"indexed":False,"name":"imageSourceUrl","type":"string"},{"indexed":False,"name":"adUrl","type":"string"},{"indexed":False,"name":"adText","type":"string"}],"name":"NewImage","type":"event"}]
mln_eth_contract = web3.eth.contract(address=contract_addr, abi=abi)

def event_abi(event_name):
    if event_name == 'NewImage':
        return mln_eth_contract.events.NewImage().abi
    else:
        print ("No events, named {} found".format(event_name))
        return None

def event_signature(event_name):
    abi = event_abi(event_name)
    if abi is None:
        return None
    return web3.toHex(event_abi_to_log_topic(abi))

def load_events_logs(event_name, from_block, to_block):
    event_signature_topic = event_signature(event_name)
    if event_signature_topic is None:
        return []

    found_logs = web3.eth.getLogs(
        {
            'address': contract_addr,
            'fromBlock': from_block,
            'toBlock': to_block,
            'topics': [event_signature_topic]
        })
    return found_logs


def decode_log(event_name, log):
    event_log = get_event_data(event_abi(event_name), log)
    decoded_logs = dict(event_log.args)
    decoded_logs["block_number"] = event_log.blockNumber
    decoded_logs["transaction_index"] = event_log.transactionIndex
    decoded_logs["event"] = event_log.event
    return decoded_logs

def map_log(unmapped_log):
    # validate keyss TODO
    mapped_log = {}
    if unmapped_log["event"] == 'NewImage':
        mapped_log["id"] = unmapped_log["ID"]
        mapped_log["x1"] = unmapped_log["fromX"]
        mapped_log["y1"] = unmapped_log["fromY"]
        mapped_log["x2"] = unmapped_log["toX"]
        mapped_log["y2"] = unmapped_log["toY"]
        mapped_log["src"] = unmapped_log["imageSourceUrl"]
        mapped_log["href"] = unmapped_log["adUrl"]
        mapped_log["alt"] = unmapped_log["adText"]
        mapped_log["block_number"] = unmapped_log["block_number"]
        mapped_log["transaction_index"] = unmapped_log["transaction_index"]
    return mapped_log

def format_log(unformatted_log):
    # TODO transform coordinates format
    formatted_log = unformatted_log
    formatted_log["x1"] = (unformatted_log["x1"] - 1) * 10
    formatted_log["y1"] = (unformatted_log["y1"] - 1) * 10
    formatted_log["x2"] = unformatted_log["x2"] * 10
    formatted_log["y2"] = unformatted_log["y2"] * 10
    return formatted_log

def get_events_list(event_name, from_block, to_block):
    loaded_logs = load_events_logs(event_name, from_block, to_block)
    events = []
    for log in loaded_logs:
        decoded_log = decode_log(event_name, log)
        mapped_log = map_log(decoded_log)
        formatted_log = format_log(mapped_log)
        events.append(formatted_log)
    return events

def main():
    # 0x15dbdB25f870f21eaf9105e68e249E0426DaE916 blocks 2800200 - 5864031
    get_events_list('NewImage', 4315137, 4815137)

if __name__ == '__main__':
    # event_name, from_block, logger
    main()
