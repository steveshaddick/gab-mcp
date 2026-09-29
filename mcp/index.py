"""Build and query a SQLite FTS5 index over the campaign files."""
import os
import re
import sqlite3
from contextlib import closing
from pathlib import Path

ROOT = Path(os.environ.get("CAMPAIGN_DIR", "./campaign")).resolve()
DB_PATH = Path(os.environ.get("CAMPAIGN_DB", "./campaign.db")).resolve()

# Only these folders are ever indexed or served. Keep DM-only notes elsewhere
# (e.g. campaign/dm/) and they can never leak through the server.
SOURCES = {
    "summary": ("summaries", ".md"),
    "codex": ("codex", ".md"),
    "transcript": ("transcripts", ".txt"),
}

STOPWORDS = {
    "a", "an", "the", "of", "to", "in", "on", "and", "or", "is", "was", "did",
    "do", "does", "what", "who", "when", "where", "about", "say", "said", "me",
}


def files():
    for kind, (folder, ext) in SOURCES.items():
        base = ROOT / folder
        if base.is_dir():
            for p in sorted(base.rglob(f"*{ext}")):
                yield kind, p


def session_of(kind, path):
    if kind == "codex":
        return ""
    m = re.search(r"(\d+)", path.stem)
    return str(int(m.group(1))) if m else ""


# ---------- chunking ----------

def _chunk_markdown(text, title):
    chunks, heading, buf = [], title, []
    for line in text.splitlines():
        if line.startswith("#"):
            if "".join(buf).strip():
                chunks.append((heading, "\n".join(buf).strip()))
            heading, buf = (line.lstrip("# ").strip() or title), []
        else:
            buf.append(line)
    if "".join(buf).strip():
        chunks.append((heading, "\n".join(buf).strip()))
    return chunks


def _chunk_transcript(text, size=1200, overlap=200):
    chunks, buf, n = [], [], 0
    for line in text.splitlines():
        buf.append(line)
        n += len(line) + 1
        if n >= size:
            chunks.append("\n".join(buf))
            tail, t = [], 0
            for l in reversed(buf):
                t += len(l) + 1
                if t > overlap:
                    break
                tail.insert(0, l)
            buf, n = tail, sum(len(l) + 1 for l in tail)
    if "".join(buf).strip():
        chunks.append("\n".join(buf))
    return [(f"part {i + 1}", c) for i, c in enumerate(chunks)]


# ---------- index build ----------

def _stamp():
    fs = list(files())
    newest = max((p.stat().st_mtime_ns for _, p in fs), default=0)
    return f"{len(fs)}:{newest}"


def build():
    tmp = DB_PATH.with_suffix(".tmp")
    tmp.unlink(missing_ok=True)
    with closing(sqlite3.connect(tmp)) as c:
        c.execute(
            "CREATE VIRTUAL TABLE chunks USING fts5("
            "kind UNINDEXED, path UNINDEXED, session UNINDEXED, heading, body, "
            "tokenize='porter unicode61 remove_diacritics 2')"
        )
        c.execute("CREATE TABLE meta(k TEXT PRIMARY KEY, v TEXT)")
        for kind, p in files():
            text = p.read_text(encoding="utf-8", errors="replace")
            parts = (
                _chunk_transcript(text)
                if kind == "transcript"
                else _chunk_markdown(text, p.stem)
            )
            rel = p.relative_to(ROOT).as_posix()
            sess = session_of(kind, p)
            c.executemany(
                "INSERT INTO chunks VALUES (?,?,?,?,?)",
                [(kind, rel, sess, h, b) for h, b in parts],
            )
        c.execute("INSERT INTO meta VALUES ('stamp', ?)", (_stamp(),))
        c.commit()
    os.replace(tmp, DB_PATH)


def ensure_fresh():
    """Rebuild the index if any file was added, removed, or modified."""
    if DB_PATH.exists():
        try:
            with closing(sqlite3.connect(DB_PATH)) as c:
                row = c.execute("SELECT v FROM meta WHERE k='stamp'").fetchone()
            if row and row[0] == _stamp():
                return
        except sqlite3.DatabaseError:
            pass
    build()


# ---------- glossary aliases ----------

def _load_aliases():
    """codex/glossary.md lines like `Holda: Olda, Holdah` become spelling groups."""
    groups = {}
    g = ROOT / "codex" / "glossary.md"
    if not g.exists():
        return groups
    for line in g.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\s*[-*]?\s*([^:=#]+?)\s*[:=]\s*(.+)$", line)
        if not m:
            continue
        names = [m.group(1)] + [a.strip() for a in m.group(2).split(",")]
        names = [n.strip("*_ ") for n in names if n.strip("*_ ")]
        for n in names:
            groups.setdefault(n.lower(), set()).update(names)
    return groups


def _term(t):
    return '"' + t.replace('"', '""') + '"'


def _fts_queries(text):
    aliases = _load_aliases()
    groups = []
    for tok in re.findall(r"\w+", text):
        if tok.lower() in STOPWORDS:
            continue
        alts = {tok, *aliases.get(tok.lower(), ())}
        groups.append("(" + " OR ".join(_term(a) for a in sorted(alts)) + ")")
    if not groups:
        return []
    return [" AND ".join(groups), " OR ".join(groups)]  # strict first, then loose


# ---------- search ----------

def search(query, kinds=("summary", "codex"), session=None, limit=8, full=False):
    ensure_fresh()
    kinds = tuple(kinds)
    body = "body" if full else "snippet(chunks, 4, '[', ']', ' … ', 32)"
    sql = (
        f"SELECT kind, path, session, heading, {body} FROM chunks "
        f"WHERE chunks MATCH ? AND kind IN ({','.join('?' * len(kinds))})"
    )
    args = [None, *kinds]
    if session is not None:
        sql += " AND session = ?"
        args.append(str(session))
    sql += " ORDER BY bm25(chunks, 0.0, 0.0, 0.0, 3.0, 1.0) LIMIT ?"
    with closing(sqlite3.connect(DB_PATH)) as c:
        for q in _fts_queries(query):
            args[0] = q
            rows = c.execute(sql, [*args, limit]).fetchall()
            if rows:
                return [
                    dict(kind=k, path=p, session=s, heading=h, text=t)
                    for k, p, s, h, t in rows
                ]
    return []


if __name__ == "__main__":
    build()
    print(f"Indexed {sum(1 for _ in files())} files -> {DB_PATH}")
