from pathlib import Path
import shutil
from conversion import markdown_to_html_node, html_nodes_finito

static = Path("./static")
public = Path("./public")
source_path = Path("./content")
html_template_path = Path("template.html")


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


def extract_title(markdown: str) -> str:
    split_content = markdown.split("\n")
    clean_split_content = [line for line in split_content if line != "" or line != "\n"]
    breakpoint()
    if clean_split_content[0].startswith("# "):
        return clean_split_content[0].lstrip("# ")
    raise Exception("HeaderNotFound")


def generate_page(from_path: Path, template_path: Path, dest_path: Path) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with from_path.open("r") as f:
        content = f.read()
    with template_path.open("r") as f:
        template = f.read()
    title = extract_title(content)
    if title is None:
        return
    content_transformed = html_nodes_finito(markdown_to_html_node(content))

    split_by_title = template.split("{{ Title }}")
    html_with_title = "".join(split_by_title[0] + title + split_by_title[1])
    split_by_content = html_with_title.split("{{ Content }}")
    html_with_content = "".join(
        split_by_content[0] + content_transformed + split_by_content[1]
    )

    if not dest_path.exists():
        dest_path.mkdir()
    result_file_path = dest_path / "index.html"
    with result_file_path.open("w") as f:
        f.write(html_with_content)


def generate_pages_recursive(
    from_path: Path, template_path: Path, dest_path: Path
) -> None:
    sufix = from_path.relative_to("content")
    public_subfolder = dest_path / sufix

    if not public_subfolder.exists():
        public_subfolder.mkdir()

    files = [file for file in from_path.iterdir() if file.is_file()]
    for file in files:
        generate_page(file, html_template_path, public_subfolder)

    directories = [directory for directory in from_path.iterdir() if directory.is_dir()]
    for directory in directories:
        generate_pages_recursive(directory, template_path, dest_path)


if __name__ == "__main__":
    shutil.rmtree(public)
    static_to_public()

    generate_pages_recursive(source_path, html_template_path, public)
