# @title Imports
import os
import asyncio
import html
import json, random, time, threading
import openai
from openai import OpenAI
from pathlib import Path
from typing import Dict, Any
from dataclasses import dataclass
from typing import List, Optional, Dict, Literal
from jsonschema import validate as js_validate, ValidationError
from fastmcp import FastMCP
from contextlib import AsyncExitStack
from pydantic import BaseModel, Field, ValidationError
from agents import (
    Agent,
    Runner,
    WebSearchTool,
    function_tool,
    SQLiteSession,
    ModelSettings,
    FunctionTool
)
from agents.agent_output import AgentOutputSchemaBase
from agents.mcp import MCPServerStreamableHttp
from agents.exceptions import ModelBehaviorError
from agents.items import ToolCallItem, ToolCallOutputItem

from IPython.display import HTML, Markdown
import warnings
warnings.filterwarnings('ignore')

import logging
logging.getLogger("openai.agents").setLevel(logging.ERROR)
