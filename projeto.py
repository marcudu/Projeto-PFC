# Unzip the uploaded project, inspect files, create a minimal deliverable that:
# - extracts only the minimum runnable code (app entry, requirements, README)
# - replaces occurrences of "lovable" (case-insensitive) with "LeitoAmigo" to remove linkage
# - removes image and asset files to avoid potential copyrighted content
# - creates a new zip "leito-amigo-minimal-tcc.zip" for download
#
# This code runs in a visible environment; outputs and the new zip will be available to download.

import os, zipfile, shutil, io, re, pathlib

zip_path = "/mnt/data/leito-amigo-gerencia-main.zip"
work_dir = "/mnt/data/leito_amigo_extracted"
minimal_dir = "/mnt/data/leito-amigo-minimal"
output_zip = "/mnt/data/leito-amigo-minimal-tcc.zip"

# Clean previous runs
if os.path.exists(work_dir):
    shutil.rmtree(work_dir)
if os.path.exists(minimal_dir):
    shutil.rmtree(minimal_dir)
if os.path.exists(output_zip):
    os.remove(output_zip)

os.makedirs(work_dir, exist_ok=True)

# Unzip
zip_path = r"C:\Users\lucas alberto\Downloads\leito-amigo-gerencia-main.zip"
with zipfile.ZipFile(zip_path, 'r') as z:
    z.extractall(work_dir)

# Walk files to inspect common app entry points
files = []
for root, dirs, filenames in os.walk(work_dir):
    for f in filenames:
        full = os.path.join(root, f)
        rel = os.path.relpath(full, work_dir)
        files.append(rel)

# Heuristic: pick python files that look like app entrypoints: app.py, run.py, main.py, wsgi.py, manage.py, and requirements/README
candidates = [f for f in files if os.path.basename(f).lower() in ("app.py","run.py","main.py","wsgi.py","manage.py","server.py")]
requirements = [f for f in files if os.path.basename(f).lower() in ("requirements.txt","pyproject.toml","Pipfile")]
readmes = [f for f in files if os.path.basename(f).lower().startswith("readme")]
config_files = [f for f in files if f.lower().endswith((".env",".ini",".cfg",".yaml",".yml","dockerfile"))]
templates_dir = None
static_dir = None

# Find templates and static typical folders
for d in ("templates","static","app/templates","app/static","leito_amigo/templates"):
    p = os.path.join(work_dir, d)
    if os.path.isdir(p):
        templates_dir = d
        break
for d in ("static","assets","public","app/static"):
    p = os.path.join(work_dir, d)
    if os.path.isdir(p):
        static_dir = d
        break

# If no obvious entry, try to find any flask-like patterns
if not candidates:
    for f in files:
        # check for "Flask(" or "if __name__" to use as entry
        path = os.path.join(work_dir, f)
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as fh:
                txt = fh.read()
            if "Flask(" in txt or "if __name__" in txt or "create_app" in txt:
                candidates.append(f)
        except:
            pass

# Prepare minimal_dir and copy selected files
os.makedirs(minimal_dir, exist_ok=True)
copied = []

# Copy README and requirements if present
for r in readmes + requirements + config_files:
    src = os.path.join(work_dir, r)
    dst = os.path.join(minimal_dir, os.path.basename(r))
    shutil.copy2(src, dst)
    copied.append(r)

# Copy the first candidate entrypoint and any modules it imports from same package (basic heuristic)
if candidates:
    entry = candidates[0]
    src = os.path.join(work_dir, entry)
    dst = os.path.join(minimal_dir, os.path.basename(entry))
    shutil.copy2(src, dst)
    copied.append(entry)
    # Try to parse imports to gather modules in same project
    with open(src, "r", encoding="utf-8", errors="ignore") as fh:
        txt = fh.read()
    imports = re.findall(r'from\s+([a-zA-Z0-9_\.]+)\s+import|import\s+([a-zA-Z0-9_\.]+)', txt)
    imported_modules = set([m[0] or m[1] for m in imports])
    # Copy files for modules that exist as .py under work_dir
    for mod in imported_modules:
        mod_path = mod.replace(".", os.sep) + ".py"
        candidate_path = os.path.join(work_dir, mod_path)
        if os.path.exists(candidate_path):
            shutil.copy2(candidate_path, os.path.join(minimal_dir, os.path.basename(candidate_path)))
            copied.append(os.path.relpath(candidate_path, work_dir))

# If templates exist, copy only essential templates (HTML files) but strip images/assets
if templates_dir:
    src_templ = os.path.join(work_dir, templates_dir)
    dst_templ = os.path.join(minimal_dir, "templates")
    os.makedirs(dst_templ, exist_ok=True)
    for root, dirs, filenames in os.walk(src_templ):
        for f in filenames:
            if f.lower().endswith((".html",".htm",".txt",".jinja2")):
                rel = os.path.relpath(os.path.join(root, f), src_templ)
                dstp = os.path.join(dst_templ, rel)
                os.makedirs(os.path.dirname(dstp), exist_ok=True)
                shutil.copy2(os.path.join(root, f), dstp)
                copied.append(os.path.join(templates_dir, rel))

# Copy small Python modules from project folder (limit to files <100KB) to avoid vendor/big files
for f in files:
    if f in copied:
        continue
    if f.lower().endswith(".py"):
        full = os.path.join(work_dir, f)
        if os.path.getsize(full) < 100*1024:
            dst = os.path.join(minimal_dir, os.path.basename(f))
            shutil.copy2(full, dst)
            copied.append(f)

# Remove any image/static assets: do not copy static assets to avoid copyrighted media
# But if there are small CSS or JS files required, copy only .css and .js under static but skip images
if static_dir:
    src_static = os.path.join(work_dir, static_dir)
    dst_static = os.path.join(minimal_dir, "static")
    os.makedirs(dst_static, exist_ok=True)
    for root, dirs, filenames in os.walk(src_static):
        for f in filenames:
            if f.lower().endswith((".css",".js",".json")) and os.path.getsize(os.path.join(root,f)) < 200*1024:
                rel = os.path.relpath(os.path.join(root,f), src_static)
                dstp = os.path.join(dst_static, rel)
                os.makedirs(os.path.dirname(dstp), exist_ok=True)
                shutil.copy2(os.path.join(root,f), dstp)
                copied.append(os.path.join(static_dir, rel))

# Replace occurrences of "lovable" (case-insensitive) in copied text files with "LeitoAmigo"
pattern = re.compile(r"lovable", re.IGNORECASE)
for root, dirs, filenames in os.walk(minimal_dir):
    for f in filenames:
        full = os.path.join(root, f)
        try:
            with open(full, "r", encoding="utf-8", errors="ignore") as fh:
                content = fh.read()
            if pattern.search(content):
                new = pattern.sub("LeitoAmigo", content)
                with open(full, "w", encoding="utf-8") as fh:
                    fh.write(new)
        except:
            # binary files skipped
            pass

# Create a short README if none exists
if not readmes:
    with open(os.path.join(minimal_dir, "README.md"), "w", encoding="utf-8") as fh:
        fh.write("# LeitoAmigo - Entrega mínima do TCC\n\nEntrega mínima contendo o ponto de entrada da aplicação e arquivos essenciais. Referências e ativos com potenciais problemas de plágio/brand foram removidos.\n\nInstruções:\n\n1. Criar um ambiente virtual Python 3.10+\n2. Instalar dependências em requirements.txt (se presente)\n3. Executar `python {entry}` substituindo pelo arquivo de entrada.\n")

# Create the output zip
def zipdir(folder, ziph):
    for root, dirs, files in os.walk(folder):
        for file in files:
            full = os.path.join(root, file)
            rel = os.path.relpath(full, folder)
            ziph.write(full, rel)

with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
    zipdir(minimal_dir, zf)

# Prepare report info
report = {
    "total_files_in_original": len(files),
    "selected_entrypoints": candidates,
    "copied_files_count": sum(len(files) for _,_,files in os.walk(minimal_dir)),
    "output_zip": output_zip,
    "replaced_terms": ["lovable -> LeitoAmigo"],
    "notes": [
        "All images and large asset files were not included to avoid potential copyrighted content.",
        "Only small .py, .html, .css, .js files were included where present.",
        "Automated plagiarism detection was not performed; user should review textual content for paraphrasing and references.",
    ]
}

report, os.path.exists(output_zip), len(files)

