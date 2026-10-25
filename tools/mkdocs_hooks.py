"""MkDocs hook: pack every starter project projects/urok-NN/ into docs/downloads/urok-NN.zip.

The archives are built before each build, so lessons can link to ../downloads/urok-NN.zip.
They are reproducible (fixed timestamps) and rewritten only when their content changes,
otherwise `mkdocs serve` would see a change in docs/ and rebuild forever.
"""
import io
import pathlib
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
PROJECTS = ROOT / "projects"
DOWNLOADS = ROOT / "docs" / "downloads"


def _pack(project):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(project.rglob("*")):
            relative = path.relative_to(project.parent)
            if any(part.startswith(".") or part == "__pycache__" for part in relative.parts):
                continue
            name = relative.as_posix() + ("/" if path.is_dir() else "")
            info = zipfile.ZipInfo(name, date_time=(2025, 1, 1, 0, 0, 0))
            info.external_attr = (0o40755 << 16 | 0x10) if path.is_dir() else (0o644 << 16)
            archive.writestr(info, b"" if path.is_dir() else path.read_bytes())
    return buffer.getvalue()


def on_pre_build(config):
    DOWNLOADS.mkdir(exist_ok=True)
    for project in sorted(PROJECTS.glob("urok-*")):
        target = DOWNLOADS / f"{project.name}.zip"
        data = _pack(project)
        if not target.exists() or target.read_bytes() != data:
            target.write_bytes(data)
