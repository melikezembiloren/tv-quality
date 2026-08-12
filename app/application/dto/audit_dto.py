from dataclasses import dataclass, field


@dataclass
class FindingInput:
    description: str
    severity: str


@dataclass
class CreateAuditInput:
    production_line_id: int
    audited_by_user_id: int
    audit_month: str
    findings: list[FindingInput] = field(default_factory=list)


@dataclass
class FindingOutput:
    id: int
    description: str
    severity: str


@dataclass
class AuditOutput:
    id: int
    production_line_id: int
    audited_by_user_id: int
    audit_month: str
    findings: list[FindingOutput] = field(default_factory=list)


@dataclass
class ListAuditsInput:
    production_line_id: int | None = None
    audit_month: str | None = None


@dataclass
class AuditSummaryOutput:
    id: int
    production_line_id: int
    audit_month: str
    finding_count: int
