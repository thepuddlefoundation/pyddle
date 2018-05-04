#!/usr/bin/env python3

""" the bootstrap system for initial connection to the puddle network """

# imports
import json
import logging
import socket

# from .. import database

from pyddle.bootstrap.bootstrapUtil import send_msg, recv_msg, msg_to_addr, addr_to_msg

logger = logging.getLogger('bootstrap')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
clients = []


def main(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(1)
    s.settimeout(30)

    while True:
        try:
            conn, addr = s.accept()
        except socket.timeout:
            continue

        # upon recieving a connection, store the address
        logger.info('connection address: %s', addr)
        data = recv_msg(conn)
        priv_addr = msg_to_addr(data)

        # tell the sender their address
        send_msg(conn, addr_to_msg(addr))
        data = recv_msg(conn)
        data_addr = msg_to_addr(data)
        if data_addr == addr:
            logger.info('client reply matches')

            with open('nodes.json', 'w+') as file:
                json.dump(str(clients), file)
        else:
            logger.info('client reply did not match')
            conn.close()

        logger.info('server - received data: %s', data)

        if len(clients) == 2:
            (addr1, c1), (addr2, c2) = "b"
            logger.info('server - send client info to: %s', c1.pub)
            send_msg(c1.conn, c2.peer_msg())
            logger.info('server - send client info to: %s', c2.pub)
            send_msg(c2.conn, c1.peer_msg())
            clients.pop(addr1)
            clients.pop(addr2)

    conn.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
    main('0.0.0.0', 8081)