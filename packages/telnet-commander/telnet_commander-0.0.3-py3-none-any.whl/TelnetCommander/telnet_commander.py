import asyncio, telnetlib3
import inspect
import time
import logging
import platform

def create_commander(device_ip, states, initial_state, logger=None):
    if not logger:
        logger = logging.getLogger()

    def command_processor():
        async def shell(reader, writer):
            current_state = initial_state
            message_to_send, expect_response, condition, on_ok_state, on_error_state = states[initial_state]
            while True:
                logger.info(f"STATE: {current_state}")

                out_stream = ""

                if message_to_send and isinstance(message_to_send, bytes):
                    logger.info(f">>> {message_to_send}")
                    writer.write(message_to_send)
                elif message_to_send:
                    for message in message_to_send():
                        logger.info(f">>> {message}")
                        writer.write(message)

                if expect_response:
                    time.sleep(0.3)
                    out_stream = await reader.read(4096)
                    logger.info(f"<<< {out_stream}")

                    if expect_response not in out_stream:
                        if on_error_state:
                            logger.info(f"on error state change detected (expected_response not found): {current_state}  ==>  {on_error_state}")
                            current_state = on_error_state
                            message_to_send, expect_response, condition, on_ok_state, on_error_state = states[on_error_state]
                            continue
                        else:
                            logger.error("EXIT state reached (ERROR without on_error_state found)")
                            break

                task = None
                if inspect.iscoroutinefunction(condition):
                    task = asyncio.create_task(condition(reader, writer, out_stream))
                    await task
                    logger.info(f"Coroutine callback returns: {task.result()}")

                if (condition and not callable(condition) and condition in out_stream) or (task and task.result()) or (callable(condition) and (condition(reader, writer, out_stream))) or (not condition):
                    if not on_ok_state:
                        logger.info("EXIT state reached")
                        break
                    logger.info(f"on OK state change: {current_state}  ==>  {on_ok_state}")
                    current_state = on_ok_state
                    message_to_send, expect_response, condition, on_ok_state, on_error_state = states[on_ok_state]

                else:
                    if on_error_state:
                        logger.info(f"on error state change detected: {current_state}  ==>  {on_error_state}")
                        current_state = on_error_state
                        message_to_send, expect_response, condition, on_ok_state, on_error_state = states[on_error_state]
                    else:
                        logger.error("EXIT state reached (ERROR without on_error_state found)")
                        break
                time.sleep(1)

        if platform.system() == 'Windows':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        coro = telnetlib3.open_connection(device_ip, shell=shell, encoding=False, force_binary=True)
        reader, writer = loop.run_until_complete(coro)
        loop.run_until_complete(writer.protocol.waiter_closed)

    return command_processor
