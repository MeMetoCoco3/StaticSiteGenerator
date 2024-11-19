from pathlib import Path
import shutil

static = Path("./static")
public = Path("./public")


def static_to_public() -> None:
    if not static.exists():
        print("static not found")
        return
    if not public.exists():
        public.mkdir()
        print("public not found")
    create_and_copy(static)


def create_and_copy(dir: Path) -> None:
    sufix = dir.relative_to("static")
    public_subfolder = public / sufix

    if not public_subfolder.exists():
        public_subfolder.mkdir()

    files = [file for file in dir.iterdir() if file.is_file()]
    for file in files:
        shutil.copy(file, public_subfolder)

    directories = [directory for directory in dir.iterdir() if directory.is_dir()]
    for directory in directories:
        create_and_copy(directory)


static_to_public()
