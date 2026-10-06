// Winning Ads Creator — Drive uploader
// Lets the ads pipeline save images and reports to YOUR Google Drive folder
// without passing them through the chat (which would cost a lot of tokens).
//
// Setup (the skill's guided setup walks you through it):
//   1. script.google.com → New project → paste this whole file.
//   2. The skill fills in ROOT_FOLDER_ID and TOKEN below for you.
//   3. Deploy → New deployment → type "Web app" → Execute as: Me →
//      Who has access: Anyone → Deploy → authorize → copy the Web app URL.
//
// Only requests carrying TOKEN are accepted, and only files inside
// ROOT_FOLDER_ID can be read. Keep the URL and token private.

const ROOT_FOLDER_ID = 'PASTE_ROOT_FOLDER_ID';
const TOKEN = 'PASTE_TOKEN';

function doPost(e) {
  const p = JSON.parse(e.postData.contents);
  if (p.token !== TOKEN) return out_({ ok: false, error: 'bad token' });
  const folder = ensurePath_(DriveApp.getFolderById(ROOT_FOLDER_ID), p.subpath || '');
  const blob = Utilities.newBlob(Utilities.base64Decode(p.base64), p.mimeType, p.name);
  const old = folder.getFilesByName(p.name);
  while (old.hasNext()) old.next().setTrashed(true);
  const f = folder.createFile(blob);
  return out_({ ok: true, id: f.getId(), url: f.getUrl(), folderUrl: folder.getUrl() });
}

function doGet(e) {
  const q = e.parameter;
  if (q.token !== TOKEN) return out_({ ok: false, error: 'bad token' });
  const root = DriveApp.getFolderById(ROOT_FOLDER_ID);
  if (q.action === 'list') {
    const folder = ensurePath_(root, q.subpath || '');
    const files = [];
    const it = folder.getFiles();
    while (it.hasNext()) { const f = it.next(); files.push({ id: f.getId(), name: f.getName() }); }
    return out_({ ok: true, folderUrl: folder.getUrl(), files: files });
  }
  if (q.action === 'get') {
    const f = DriveApp.getFileById(q.id);
    if (!insideRoot_(f)) return out_({ ok: false, error: 'outside root folder' });
    return out_({ ok: true, name: f.getName(), mimeType: f.getMimeType(),
                  base64: Utilities.base64Encode(f.getBlob().getBytes()) });
  }
  return out_({ ok: true, alive: true });
}

function ensurePath_(parent, path) {
  path.split('/').filter(String).forEach(function (name) {
    const it = parent.getFoldersByName(name);
    parent = it.hasNext() ? it.next() : parent.createFolder(name);
  });
  return parent;
}

function insideRoot_(file) {
  const queue = [];
  const p = file.getParents();
  while (p.hasNext()) queue.push(p.next());
  for (let depth = 0; queue.length && depth < 50; depth++) {
    const f = queue.shift();
    if (f.getId() === ROOT_FOLDER_ID) return true;
    const up = f.getParents();
    while (up.hasNext()) queue.push(up.next());
  }
  return false;
}

function out_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
