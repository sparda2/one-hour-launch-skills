#!/usr/bin/env python3
"""Move files between this computer and the Drive folder through the
Drive uploader web app, so file bytes never pass through the chat.

Usage (UPLOADER_URL and UPLOADER_TOKEN come from the Settings tab):
  drive_sync.py ping
  drive_sync.py upload <local_file> <drive/sub/path>
  drive_sync.py list   <drive/sub/path>
  drive_sync.py get    <file_id> <local_file>
  drive_sync.py pull   <drive/sub/path> <local_dir>   # download a whole folder

Every command prints ONE line of JSON.
"""
import base64, json, mimetypes, os, sys, urllib.parse, urllib.request

URL = os.environ.get("UPLOADER_URL", "")
TOKEN = os.environ.get("UPLOADER_TOKEN", "")


def _call(method, params=None, body=None):
    if method == "GET":
        req = urllib.request.Request(URL + "?" + urllib.parse.urlencode({**params, "token": TOKEN}))
    else:
        data = json.dumps({**body, "token": TOKEN}).encode()
        req = urllib.request.Request(URL, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:  # follows Apps Script's redirect
        return json.loads(r.read().decode())


def upload(path, subpath):
    mime = mimetypes.guess_type(path)[0] or "application/octet-stream"
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    return _call("POST", body={"subpath": subpath, "name": os.path.basename(path),
                               "mimeType": mime, "base64": b64})


def get(file_id, dest):
    r = _call("GET", {"action": "get", "id": file_id})
    if r.get("ok"):
        os.makedirs(os.path.dirname(dest) or ".", exist_ok=True)
        with open(dest, "wb") as f:
            f.write(base64.b64decode(r.pop("base64")))
        r["saved"] = dest
    return r


def pull(subpath, local_dir):
    listing = _call("GET", {"action": "list", "subpath": subpath})
    if not listing.get("ok"):
        return listing
    saved = [get(f["id"], os.path.join(local_dir, f["name"])).get("saved") for f in listing["files"]]
    return {"ok": True, "saved": [s for s in saved if s]}


def main(argv):
    if not URL or not TOKEN:
        return {"ok": False, "error": "set UPLOADER_URL and UPLOADER_TOKEN first"}
    cmd, args = argv[0], argv[1:]
    if cmd == "ping":
        return _call("GET", {})
    if cmd == "upload":
        return upload(*args)
    if cmd == "list":
        return _call("GET", {"action": "list", "subpath": args[0]})
    if cmd == "get":
        return get(*args)
    if cmd == "pull":
        return pull(*args)
    return {"ok": False, "error": "unknown command " + cmd}


if __name__ == "__main__":
    try:
        print(json.dumps(main(sys.argv[1:])))
    except Exception as e:  # one line, never a stack trace into the chat
        print(json.dumps({"ok": False, "error": f"{type(e).__name__}: {e}"}))
