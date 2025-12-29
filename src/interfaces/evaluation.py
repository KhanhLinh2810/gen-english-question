from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any

from src.enums import QuestionTypeEnum
from src.interfaces.choice import IChoice

@dataclass
class GeneratedQuestion:
    num_ans_per_question: int
    num_question: int
    type: QuestionTypeEnum

    paragraph: Optional[str] = None
    content: Optional[str] = None
    list_words: List[str] = field(default_factory=list)
    choices: List[IChoice] = field(default_factory=list)

    # tags: List[str] = field(default_factory=list)
    
    # Tùy chọn: meta khác (CEFR level, grade, ... )
    # metadata: Dict[str, Any] = field(default_factory=dict)