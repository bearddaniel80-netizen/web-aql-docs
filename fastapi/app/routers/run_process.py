from pathlib import Path
import asyncio
import subprocess
import re

def md_links_to_html(input_file, source):
    pattern = r'\[([^\]]+)\]\(([^)]+)\.md\)'
    with open(input_file, "r") as _in:
        text = _in.read()

    def replace(match):
        label = match.group(1)
        slug = match.group(2)
        return f'<b>{label.title()}</b>'
        #return f'<a href="/api/{source}/{slug}">{label.title()}</a>'
    
    new_text = re.sub(pattern, replace, text)
    
    with open(input_file, "w") as out:
        out.write(new_text)

async def render(command):
    try:
        result = await asyncio.to_thread(
            subprocess.run,
            command,
            capture_output=True,
            text=True
        )
        return result.stdout
    except:
        return result