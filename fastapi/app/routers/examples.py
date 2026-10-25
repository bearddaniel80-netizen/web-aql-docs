from .run_process import render, md_links_to_html
from ..security.api_key_check import verify_internal_key

from pathlib import Path
from fastapi import Header, APIRouter
from fastapi.responses import HTMLResponse

FOLDER = "examples"

router = APIRouter(prefix=f"/api/{FOLDER}")

@router.get("/list")
async def list_examples(
    x_internal_key: str | None = Header(default=None),
):
    verify_internal_key(x_internal_key)
    command = ["aql", "docs"]
    await render(command)
    command = ["ls", FOLDER]
    results = await render(command)
    clean_result = list(
        map(
            lambda f: str(Path(f).with_suffix("")),
            filter(None, results.split("\n"))
        )
    )
    return {"result": clean_result }
        
@router.get("/{filename}", response_class=HTMLResponse)
async def render_examples_file(
    filename:str,
    x_internal_key: str | None = Header(default=None),
):
    verify_internal_key(x_internal_key)
    input_file = str(Path.cwd() / FOLDER / f"{filename}.md")
    output_file = str(Path.cwd() / FOLDER / f"{filename}.html")
    md_links_to_html( input_file, FOLDER )
    command = ["pandoc", "-f", "markdown-yaml_metadata_block", input_file, "-o", output_file]
    await render(command)
    with open(output_file, "r") as f:
        html = f.read()
    return HTMLResponse(content=html)