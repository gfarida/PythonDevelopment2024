import asyncio
import cowsay

clients = {}

async def chat(reader, writer):
    me = ""
    queue = asyncio.Queue()
    receive = asyncio.create_task(queue.get())
    send_cmd = asyncio.create_task(reader.readline())
    is_reg = False
    while not reader.at_eof():
        done, pending = await asyncio.wait([send_cmd, receive], return_when=asyncio.FIRST_COMPLETED)
        for q in done:
            if q is send_cmd:
                send_cmd = asyncio.create_task(reader.readline())
                cur_cmd = q.result().decode().strip().split()

                args = None
                if len(cur_cmd) > 1:
                    args = cur_cmd[1:]

                if cur_cmd[0] == 'who':
            
                    if args:
                        writer.write(f"*** {args[0]} {','.join(clients.keys())}\n".encode())
                    else:
                        writer.write(f"Registered users: {clients.keys()}\n".encode())
                    await writer.drain()

                elif cur_cmd[0] == 'cows':
                    available = set(cowsay.list_cows()) - set(clients.keys())
                    if args:
                        writer.write(f"*** {args[0]} {','.join(available)}\n".encode())
                    else:
                        writer.write(f"Free user names: {available}\n".encode())
                    await writer.drain()

                elif cur_cmd[0] == 'login':
                    if len(cur_cmd) != 2:
                        writer.write(f"Usage: login cow_name\n".encode())
                        await writer.drain()
                    else:
                        cur_cow = cur_cmd[1]
                        if cur_cow not in cowsay.list_cows():
                            writer.write(f"Cow name is not allowed! \n".encode())
                            await writer.drain()
                        else:
                            if cur_cow in clients:
                                writer.write(f"Cow name is already in use \n".encode())
                                await writer.drain()
                            else:
                                is_reg = True
                                clients[cur_cow] = queue
                                me = cur_cow

                elif cur_cmd[0] == 'yield':
                    if len(cur_cmd) != 2:
                        writer.write(f"Usage: yield message \n".encode())
                        await writer.drain()
                    else:
                        if not is_reg:
                            writer.write(f"Please sign in \n".encode())
                            await writer.drain()
                        else:
                            message = cur_cmd[1]
                            for out in clients.values():
                                if out is not clients[me]:
                                    await out.put(f"{cowsay.cowsay(message, cow=me)}\n")
                
                elif cur_cmd[0] == 'quit':
                    if len(cur_cmd) != 1:
                        writer.write(f"Usage: quit \n".encode())
                        await writer.drain()
                    else:
                        send_cmd.cancel()
                        receive.cancel()
                        print(me, "DONE")
                        del clients[me]
                        writer.close()
                        await writer.wait_closed()
                
                elif cur_cmd[0] == 'say':
                    if len(cur_cmd) != 3:
                        writer.write(f"Usage: say cow_name message \n".encode())
                        await writer.drain()
                    else:
                        send_to = cur_cmd[1]
                        message = cur_cmd[2]
                        if send_to not in clients:
                            writer.write(f"Cow-reciever is not registered  \n".encode())
                            await writer.drain()
                        else:
                            await clients[send_to].put(f"{cowsay.cowsay(message, cow=me)}\n")
                            await writer.drain()
                    
            elif q is receive:
                receive = asyncio.create_task(clients[me].get())
                writer.write(f"{q.result()}\n".encode())
                await writer.drain()

    

async def main():
    server = await asyncio.start_server(chat, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())