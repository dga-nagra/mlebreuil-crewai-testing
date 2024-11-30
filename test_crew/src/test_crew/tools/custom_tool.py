from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from pcapkit import extract

class PcapToolInput(BaseModel):
    """Input schema for PcapTool."""
    file: str = Field(..., description="name of the file to be imported.")

class PcapTool(BaseTool):
    name: str = "pcaptool"
    description: str = (
        "Extract content of a pcap file as a json formated output."
    )
    args_schema: Type[BaseModel] = PcapToolInput

    def _run(self, file: str) -> str:
        json = extract(fin=file, fout='out.json', format='json', extension=False)
        return json
