# @title Some Utils

SCHEMA_PATH = Path("quiz-schema.json")

with open("quiz-ui.html", "r") as f:
    QUIZ_UI = f.read()

class QuizAgentOutputSchema(AgentOutputSchemaBase):
    """
    Custom output schema that:
      - returns your JSON Schema (for Structured Outputs)
      - validates and parses the model's JSON into a Python object
    """

    def __init__(self, schema_path: Path = SCHEMA_PATH):
        self._schema_path = schema_path
        self._schema: Dict[str, Any] = json.loads(
            self._schema_path.read_text(encoding="utf-8")
        )
        # tip: assert top-level shape matches Structured Outputs support
        # (only supported/strict JSON Schema features) per docs:
        # https://platform.openai.com/docs/guides/structured-outputs/supported-schemas
        # The uploaded file uses only supported constructs (object/array/string/integer).

    # --- AgentOutputSchemaBase methods required by the SDK ---
    def is_plain_text(self) -> bool:
        return False

    def name(self) -> str:
        return "QuizJSON"

    def json_schema(self) -> Dict[str, Any]:
        # The SDK will pass this to the model as the response schema.
        return self._schema

    def is_strict_json_schema(self) -> bool:
        # Opt into strict mode so the SDK enforces the subset supported by Structured Outputs.
        return True

    def validate_json(self, json_str: str) -> Any:
        """
        Must return the validated object or raise ModelBehaviorError.
        """
        try:
            obj = json.loads(json_str)
        except Exception as e:
            raise ModelBehaviorError(f"Invalid JSON: {e}") from e

        try:
            js_validate(instance=obj, schema=self._schema)  # runtime guardrail
        except ValidationError as e:
            # Signal to the SDK that the model misbehaved.
            raise ModelBehaviorError(
                f"JSON failed schema validation: {e.message}"
            ) from e

        return obj


def render_quiz_html(
    quiz: Dict[str, Any],
    *,
    title: str | None = None,
    shuffle_questions: bool = False,
    shuffle_options: bool = False,
) -> str:

    topic = title or quiz.get("topic") or "Quiz"

    norm_questions = []
    for idx, q in enumerate(quiz.get("questions", []), start=1):
        # Try both shapes
        q_text = q.get("question") or q.get("text") or ""
        opts = q.get("choices") or q.get("options") or []
        # Keys/letters
        normalized_opts = []
        for opt in opts:
            key = opt.get("key") or opt.get("letter") or ""
            normalized_opts.append({"key": str(key), "text": opt.get("text", "")})
        answer_key = q.get("answer_key") or q.get("answer") or ""
        norm_questions.append(
            {
                "id": q.get("id") or idx,
                "text": q_text,
                "options": normalized_opts,
                "answer": str(answer_key),
            }
        )

    client_payload = {
        "title": topic,
        "questions": norm_questions,
        "settings": {
            "shuffleQuestions": bool(shuffle_questions),
            "shuffleOptions": bool(shuffle_options),
        },
    }

    # Escape + serialize once for safe embedding in a <script> tag
    data_json = json.dumps(client_payload, ensure_ascii=False)

    return QUIZ_UI.replace("{ data_json }", data_json)


# ───────────────────────────
# Shared types
# ───────────────────────────
class CheeseFact(BaseModel):
    statement: str
    source: Optional[str] = None

class QuizChoice(BaseModel):
    key: str
    text: str


class QuizQ(BaseModel):
    question: str
    choices: List[QuizChoice]
    answer_key: str
    source_note: Optional[str] = None


class QuizDraft(BaseModel):
    topic: str
    questions: List[QuizQ]


class ReviewResult(BaseModel):
    approved: bool
    notes: str = ""
    needs_revision_indices: List[int] = Field(default_factory=list)
    needs_user_opinion: bool = False


@dataclass
class GuildContext:
    fact_cache: dict[str, List[CheeseFact]]


@dataclass
class OrchestratorResult:
    response_text: str
    structured_json: dict
    formatted_md: str


# ───────────────────────────
# Helper tools
# ───────────────────────────


@function_tool
def ensure_unique_answers(question: str, choices: List[str]) -> bool:
    norm = [c.strip().lower() for c in choices]
    return len(set(norm)) == len(norm)


@function_tool
def ask_head_cheesemonger(prompt: str, default_decision: bool = True) -> bool:
    # In real UI, ask the user. Here we simulate.
    return default_decision
