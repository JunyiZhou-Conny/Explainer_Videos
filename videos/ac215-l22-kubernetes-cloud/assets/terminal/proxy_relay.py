#!/usr/bin/env python3
"""Capture-only helper, not part of the tutorial.

The recording sandbox reaches the internet only through an HTTPS proxy that listens on the host's
loopback (127.0.0.1), which containers on Docker's bridge network cannot see. This forwards
<listen_ip>:<listen_port> (the bridge gateway, e.g. 172.17.0.1) to that proxy, byte for byte, so the
nested Docker daemons of capture.sh (and the containers they start) can use it as HTTPS_PROXY.
Usage: proxy_relay.py <listen_ip> <listen_port> <proxy_host> <proxy_port>
"""
import asyncio
import sys


async def pipe(reader, writer):
    try:
        while data := await reader.read(65536):
            writer.write(data)
            await writer.drain()
    except (ConnectionError, asyncio.CancelledError):
        pass
    finally:
        writer.close()


async def main(listen_ip, listen_port, proxy_host, proxy_port):
    async def handle(c_reader, c_writer):
        try:
            p_reader, p_writer = await asyncio.open_connection(proxy_host, proxy_port)
        except OSError:
            c_writer.close()
            return
        await asyncio.gather(pipe(c_reader, p_writer), pipe(p_reader, c_writer))

    server = await asyncio.start_server(handle, listen_ip, listen_port)
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    ip, port, phost, pport = sys.argv[1:5]
    asyncio.run(main(ip, int(port), phost, int(pport)))
