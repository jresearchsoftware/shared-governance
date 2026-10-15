"""Producer convenience entry; consumers invoke the same tool from their pinned slot."""
from pathlib import Path
import runpy

if __name__ == "__main__":
    runpy.run_path(str(Path(__file__).resolve().parents[1]
                      / "packages/development-governance/tools/chatgpt/project.py"), run_name="__main__")
