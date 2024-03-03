from __future__ import annotations

import logging
from itertools import islice
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

from discord.utils import maybe_coroutine

from .exceptions import LunaError, ProcessError, StopError, WorkloadExceededError
from .interface import Adapter, Block
from .verb import Verb

__all__ = (
    "Interpreter",
    "AsyncInterpreter",
    "Context",
    "Response",
    "Node",
)

log = logging.getLogger(__name__)

AdapterMapping = Mapping[str, Adapter]


class Node:
    __slots__ = ("output", "verb", "coordinates")

    def __init__(
        self,
        coordinates: Tuple[int, int],
        verb: Optional[Verb] = None,
    ) -> None:
        self.output: Optional[str] = None
        self.verb = verb
        self.coordinates = coordinates

    def __str__(self) -> str:
        return str(self.verb) + " at " + str(self.coordinates)

    def __repr__(self) -> str:
        return f"<Node verb={self.verb!r} coordinates={self.coordinates!r} output={self.output!r}>"

    @classmethod
    def build_tree(cls, message: str) -> List[Node]:
        nodes = []
        previous = r""

        starts = []
        for i, ch in enumerate(message):
            if ch == "{" and previous != r"\\":
                starts.append(i)
            if ch == "}" and previous != r"\\":
                if not starts:
                    continue
                coords = (starts.pop(), i)
                n = cls(coords)
                nodes.append(n)

            previous = ch
        return nodes


class Response:
    __slots__ = (
        "body",
        "actions",
        "variables",
        "extra_kwargs",
    )

    def __init__(
        self,
        *,
        variables: Optional[AdapterMapping] = None,
        extra_kwargs: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.body: Optional[str] = None
        self.actions: Dict[str, Any] = {}
        self.variables: AdapterMapping = variables if variables is not None else {}
        self.extra_kwargs: Dict[str, Any] = (
            extra_kwargs if extra_kwargs is not None else {}
        )

    def __repr__(self) -> str:
        return f"<Response body={self.body!r} actions={self.actions!r} variables={self.variables!r}>"


class Context:
    __slots__ = (
        "verb",
        "original_message",
        "interpreter",
        "response",
    )

    def __init__(
        self,
        verb: Verb,
        response: Response,
        interpreter: Interpreter,
        original_message: str,
    ) -> None:
        self.verb: Verb = verb
        self.original_message = original_message
        self.interpreter = interpreter
        self.response = response

    def __repr__(self) -> str:
        return f"<Context verb={self.verb!r}>"


class Interpreter:
    __slots__ = ("blocks",)

    def __init__(self, blocks: Sequence[Block]) -> None:
        self.blocks = blocks

    def __repr__(self) -> str:
        return f"<{type(self).__name__} blocks={self.blocks!r}>"

    def _get_context(
        self,
        node: Node,
        final: str,
        *,
        response: Response,
        original_message: str,
        verb_limit: int,
    ) -> Context:
        # Get the updated verb string from coordinates and make the context
        start, end = node.coordinates
        node.verb = Verb(final[start : end + 1], limit=verb_limit)
        return Context(node.verb, response, self, original_message)

    def _process_blocks(self, ctx: Context, node: Node) -> Optional[str]:
        for block in self.blocks:
            if not block.will_accept(ctx):
                continue
            value = block.process(ctx)
            if value is not None:  # Value found? We're done here.
                value = str(value)
                node.output = value
                return value

    @staticmethod
    def _check_workload(charlimit: Optional[int], total_work: int, output: str) -> int:
        if charlimit is None:
            return 0
        total_work += len(output)
        if total_work > charlimit:
            msg = (
                "The interpreter had its workload exceeded. The total characters "
                f"attempted were {total_work}/{charlimit}"
            )
            raise WorkloadExceededError(msg)
        return total_work

    @staticmethod
    def _text_deform(start: int, end: int, final: str, output: str) -> Tuple[str, int]:
        message_slice_len = (end + 1) - start
        replacement_len = len(output)
        differential = (
            replacement_len - message_slice_len
        )  # The change in size of `final` after the change is applied
        final = final[:start] + output + final[end + 1 :]
        return final, differential

    @staticmethod
    def _translate_nodes(
        node_ordered_list: List[Node], index: int, start: int, differential: int
    ) -> None:
        for future_n in islice(node_ordered_list, index + 1, None):
            new_start = None
            new_end = None
            if future_n.coordinates[0] > start:
                new_start = future_n.coordinates[0] + differential
            else:
                new_start = future_n.coordinates[0]

            new_end = (
                future_n.coordinates[1] + differential
                if future_n.coordinates[1] > start
                else future_n.coordinates[1]
            )

            future_n.coordinates = (new_start, new_end)

    def _solve(
        self,
        message: str,
        node_ordered_list: List[Node],
        response: Response,
        *,
        charlimit: Optional[int],
        verb_limit: int = 2000,
    ) -> str:
        final = message
        total_work = 0
        for index, node in enumerate(node_ordered_list):
            start, end = node.coordinates
            ctx = self._get_context(
                node,
                final,
                response=response,
                original_message=message,
                verb_limit=verb_limit,
            )
            log.debug("Processing context %r at (%r, %r)", ctx, start, end)
            try:
                output = self._process_blocks(ctx, node)
            except StopError as exc:
                log.debug("StopError raised on node %r", node, exc_info=exc)
                return final[:start] + exc.message
            if output is None:
                continue

            total_work = self._check_workload(charlimit, total_work, output)
            final, differential = self._text_deform(start, end, final, output)
            self._translate_nodes(node_ordered_list, index, start, differential)
        return final

    @staticmethod
    def _return_response(response: Response, output: str) -> Response:
        if response.body is None:
            response.body = output.strip()
        else:
            # Dont override an overridden response.
            response.body = response.body.strip()
        return response

    def process(
        self,
        message: str,
        seed_variables: Optional[AdapterMapping] = None,
        *,
        charlimit: Optional[int] = None,
        **kwargs,
    ) -> Response:
        response = Response(variables=seed_variables, extra_kwargs=kwargs)
        node_ordered_list = Node.build_tree(message)
        try:
            output = self._solve(
                message,
                node_ordered_list,
                response,
                charlimit=charlimit,
            )
        except LunaError:
            raise
        except Exception as error:
            raise ProcessError(error, response, self) from error
        return self._return_response(response, output)


class AsyncInterpreter(Interpreter):
    async def _get_acceptors(self, ctx: Context) -> List[Block]:
        return [
            block
            for block in self.blocks
            if await maybe_coroutine(block.will_accept, ctx)
        ]

    async def _process_blocks(self, ctx: Context, node: Node) -> Optional[str]:
        acceptors = await self._get_acceptors(ctx)
        for b in acceptors:
            value = await maybe_coroutine(b.process, ctx)
            if value is not None:
                value = str(value)
                node.output = value
                return value

    async def _solve(
        self,
        message: str,
        node_ordered_list: List[Node],
        response: Response,
        *,
        charlimit: Optional[int],
        verb_limit: int = 2000,
    ) -> str:
        final = message
        total_work = 0

        for index, node in enumerate(node_ordered_list):
            start, end = node.coordinates
            ctx = self._get_context(
                node,
                final,
                response=response,
                original_message=message,
                verb_limit=verb_limit,
            )
            try:
                output = await self._process_blocks(ctx, node)
            except StopError as exc:
                return final[:start] + exc.message
            if output is None:
                continue  # If there was no value output, no need to text deform.

            total_work = self._check_workload(charlimit, total_work, output)
            final, differential = self._text_deform(start, end, final, output)
            self._translate_nodes(node_ordered_list, index, start, differential)
        return final

    async def process(
        self,
        message: str,
        seed_variables: Optional[AdapterMapping] = None,
        *,
        charlimit: Optional[int] = None,
        **kwargs,
    ) -> Response:
        response = Response(variables=seed_variables, extra_kwargs=kwargs)
        node_ordered_list = Node.build_tree(message)
        try:
            output = await self._solve(
                message,
                node_ordered_list,
                response,
                charlimit=charlimit,
            )
        except LunaError:
            raise
        except Exception as error:
            raise ProcessError(error, response, self) from error
        return self._return_response(response, output)
