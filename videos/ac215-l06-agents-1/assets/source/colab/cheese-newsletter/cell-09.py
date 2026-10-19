# @title Imports
import asyncio
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from html import escape
import json
from pathlib import Path
import re
from urllib.parse import urlsplit
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field
from pydantic import ValidationError

from agent_framework import Agent, FunctionInvocationContext, tool
from agent_framework.openai import OpenAIChatClient
