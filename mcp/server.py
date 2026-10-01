"""Campaign MCP server: read-only tools over summaries, codex, and transcripts.

Run:  CAMPAIGN_TOKENS="steve=<secret>,alice=<secret>" uvicorn server:app --port 8000
"""
print("DEBUG: server.py module loading...")
import hmac
import os
import re
from typing import Optional

from pydantic import BaseModel
from mcp.server import Server
from mcp.types import Tool, TextContent, ListToolsResult

import index

print("DEBUG: Creating Server instance")
mcp = Server("campaign")
print("DEBUG: Server instance created")


def _slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def _fmt(results):
    if not results:
        return "No matches."
    return "\n\n".join(
        f"[{r['kind']}] {r['path']} — {r['heading']}\n{r['text']}" for r in results
    )


# Tool implementation functions
def _search_campaign(query: str, include_transcripts: bool = False, limit: int = 8) -> str:
    kinds = ("summary", "codex") + (("transcript",) if include_transcripts else ())
    return _fmt(index.search(query, kinds=kinds, limit=min(limit, 20)))


def _get_session_summary(session: int) -> str:
    for kind, p in index.files():
        if kind == "summary" and index.session_of(kind, p) == str(session):
            return p.read_text(encoding="utf-8")
    return f"No summary found for session {session}."


def _get_codex_entry(name: str) -> str:
    want = _slug(name)
    entries = [p for kind, p in index.files() if kind == "codex"]
    for p in entries:
        if _slug(p.stem) == want:
            return f"# {p.relative_to(index.ROOT).as_posix()}\n\n" + p.read_text(encoding="utf-8")
    close = [p.stem for p in entries if want in _slug(p.stem)]
    return f"No codex file named '{name}'. Close matches: {close or 'none'}. Try list_codex."


def _list_codex() -> str:
    names = [p.relative_to(index.ROOT).as_posix() for k, p in index.files() if k == "codex"]
    return "\n".join(names) or "Codex is empty."


def _get_transcript_excerpt(session: int, query: str, max_passages: int = 3) -> str:
    hits = index.search(
        query, kinds=("transcript",), session=session, limit=min(max_passages, 5), full=True
    )
    if not hits:
        return f"No transcript passages found in session {session}."
    return "\n\n---\n\n".join(f"(session {session}, {h['heading']})\n{h['text']}" for h in hits)


# Request parameter models
class EmptyParams(BaseModel):
    pass


class SearchCampaignParams(BaseModel):
    query: str
    include_transcripts: bool = False
    limit: int = 8


class GetSessionSummaryParams(BaseModel):
    session: int


class GetCodexEntryParams(BaseModel):
    name: str


class GetTranscriptExcerptParams(BaseModel):
    session: int
    query: str
    max_passages: int = 3


# Handler functions for initialize
async def handle_initialize(_: EmptyParams):
    print("DEBUG: handle_initialize called")
    return {
        "protocolVersion": "2024-11-05",
        "capabilities": {
            "tools": {}
        },
        "serverInfo": {
            "name": "campaign",
            "version": "1.0.0"
        }
    }


# Handler functions for tools/list
async def handle_list_tools(_: EmptyParams):
    print("DEBUG: handle_list_tools called")
    try:
        tools = [
            {
                "name": "search_campaign",
                "description": "Search session summaries and codex entries (NPCs, locations, threads, loot). Set include_transcripts=True only when exact wording is needed.",
                "inputSchema": SearchCampaignParams.model_json_schema(),
            },
            {
                "name": "get_session_summary",
                "description": "Return the summary for one session number.",
                "inputSchema": GetSessionSummaryParams.model_json_schema(),
            },
            {
                "name": "get_codex_entry",
                "description": "Return a codex file by name, e.g. 'npcs', 'locations', or a character name.",
                "inputSchema": GetCodexEntryParams.model_json_schema(),
            },
            {
                "name": "list_codex",
                "description": "List all codex files.",
                "inputSchema": EmptyParams.model_json_schema(),
            },
            {
                "name": "list_open_threads",
                "description": "Return the open quests, mysteries, grudges, and promises.",
                "inputSchema": EmptyParams.model_json_schema(),
            },
            {
                "name": "get_transcript_excerpt",
                "description": "Return the best-matching raw transcript passages from one session, for when exact wording matters.",
                "inputSchema": GetTranscriptExcerptParams.model_json_schema(),
            },
        ]
        print("DEBUG: tools list created")
        result = {"tools": tools}
        print("DEBUG: returning tools dict")
        return result
    except Exception as e:
        print(f"DEBUG: Error in handle_list_tools: {e}")
        import traceback
        traceback.print_exc()
        raise


class CallToolParams(BaseModel):
    name: str
    arguments: dict


async def handle_call_tool(params: CallToolParams):
    print(f"DEBUG: handle_call_tool called with {params}")
    name = params.name
    arguments = params.arguments
    try:
        print(f"DEBUG: Calling tool '{name}' with args: {arguments}")
        if name == "search_campaign":
            p = SearchCampaignParams(**arguments)
            result = _search_campaign(p.query, p.include_transcripts, p.limit)
        elif name == "get_session_summary":
            p = GetSessionSummaryParams(**arguments)
            result = _get_session_summary(p.session)
        elif name == "get_codex_entry":
            p = GetCodexEntryParams(**arguments)
            result = _get_codex_entry(p.name)
        elif name == "list_codex":
            result = _list_codex()
        elif name == "list_open_threads":
            result = _get_codex_entry("open-threads")
        elif name == "get_transcript_excerpt":
            p = GetTranscriptExcerptParams(**arguments)
            result = _get_transcript_excerpt(p.session, p.query, p.max_passages)
        else:
            result = f"Unknown tool: {name}"

        print("DEBUG: Tool completed successfully")
        return {"content": [{"type": "text", "text": result}]}
    except Exception as e:
        print(f"DEBUG: Tool error: {e}")
        import traceback
        traceback.print_exc()
        return {"content": [{"type": "text", "text": f"Tool error: {e}"}]}


# Register the handlers
print("DEBUG: Registering tools/list handler")
mcp.add_request_handler("tools/list", EmptyParams, handle_list_tools)
print("DEBUG: Registering tools/call handler")
mcp.add_request_handler("tools/call", CallToolParams, handle_call_tool)
print("DEBUG: Handlers registered successfully")


# ---------- auth ----------
# Per-player tokens: CAMPAIGN_TOKENS="steve=abc123,alice=def456".
# Accepted as a URL prefix (/t/<token>/mcp) or an "Authorization: Bearer" header.
# The URL form exists because custom connector setup screens may not let players
# add headers. Don't log request paths at the proxy, or tokens end up in logs.

def _load_tokens():
    raw = os.environ.get("CAMPAIGN_TOKENS", "")
    return dict(kv.split("=", 1) for kv in raw.split(",") if "=" in kv)


class TokenAuth:
    def __init__(self, app, tokens):
        self.app, self.tokens = app, tokens

    def _valid(self, candidate):
        ok = False
        for t in self.tokens.values():  # check all, no early exit
            ok |= hmac.compare_digest(candidate.encode(), t.encode())
        return ok

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":  # lifespan etc. pass straight through
            return await self.app(scope, receive, send)
        token = None
        m = re.match(r"^/t/([^/]+)(/.*)?$", scope["path"])
        if m:
            token, rest = m.group(1), m.group(2) or "/"
            scope = dict(scope, path=rest, raw_path=rest.encode())
        else:
            auth = dict(scope["headers"]).get(b"authorization", b"").decode()
            if auth.lower().startswith("bearer "):
                token = auth[7:].strip()
        if not token or not self._valid(token):
            await send({"type": "http.response.start", "status": 401,
                        "headers": [(b"content-type", b"text/plain")]})
            await send({"type": "http.response.body", "body": b"Unauthorized"})
            return
        await self.app(scope, receive, send)


_tokens = _load_tokens()
if not _tokens and os.environ.get("CAMPAIGN_ALLOW_NO_AUTH") != "1":
    raise RuntimeError("Set CAMPAIGN_TOKENS (or CAMPAIGN_ALLOW_NO_AUTH=1 for local testing).")

print("DEBUG: Ensuring index is fresh")
index.ensure_fresh()

# Custom stateless HTTP endpoint (bypass MCP's session-based transport)
import json
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

async def mcp_handler(request):
    try:
        body = await request.json()
        method = body.get("method")
        params = body.get("params", {})
        request_id = body.get("id")

        if method == "initialize":
            result = await handle_initialize(EmptyParams())
        elif method == "tools/list":
            result = await handle_list_tools(EmptyParams())
        elif method == "tools/call":
            result = await handle_call_tool(CallToolParams(**params))
        else:
            return JSONResponse({
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32601, "message": f"Method not found: {method}"}
            }, status_code=400)

        return JSONResponse({
            "jsonrpc": "2.0",
            "id": request_id,
            "result": result
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse({
            "jsonrpc": "2.0",
            "id": body.get("id") if 'body' in locals() else None,
            "error": {"code": -32603, "message": f"Internal error: {str(e)}"}
        }, status_code=500)

print("DEBUG: Creating stateless HTTP app")
app = Starlette(routes=[Route("/mcp", mcp_handler, methods=["POST"])])
print(f"DEBUG: App created: {type(app)}")

if _tokens:
    print("DEBUG: Wrapping app with TokenAuth")
    app = TokenAuth(app, _tokens)
print("DEBUG: Server module fully loaded")
