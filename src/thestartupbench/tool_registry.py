"""Built-in tool metadata for the reference scaffold."""

from __future__ import annotations


_TOOL_CATALOG = {
    "metrics.query": {
        "description": "Query business metrics over a time range.",
        "request_schema_ref": "tsb_tool_call.schema.json",
        "response_schema_ref": "tsb_tool_response.schema.json",
        "mutability": "read",
        "approval_sensitivity": "low",
        "budget_sensitive": False,
    },
    "metrics.report": {
        "description": "Generate a structured business report.",
        "request_schema_ref": "tsb_tool_call.schema.json",
        "response_schema_ref": "tsb_tool_response.schema.json",
        "mutability": "read",
        "approval_sensitivity": "low",
        "budget_sensitive": False,
    },
    "product.roadmap.read": {
        "description": "Read roadmap items and planning metadata.",
        "request_schema_ref": "tsb_tool_call.schema.json",
        "response_schema_ref": "tsb_tool_response.schema.json",
        "mutability": "read",
        "approval_sensitivity": "low",
        "budget_sensitive": False,
    },
    "product.roadmap.write": {
        "description": "Update roadmap priorities and sequencing.",
        "request_schema_ref": "tsb_tool_call.schema.json",
        "response_schema_ref": "tsb_tool_response.schema.json",
        "mutability": "write",
        "approval_sensitivity": "medium",
        "budget_sensitive": True,
    },
    "product.launch": {
        "description": "Trigger or schedule a product launch.",
        "request_schema_ref": "tsb_tool_call.schema.json",
        "response_schema_ref": "tsb_tool_response.schema.json",
        "mutability": "write",
        "approval_sensitivity": "medium",
        "budget_sensitive": True,
    },
    "growth.experiment.create": {
        "description": "Create a growth or activation experiment.",
        "request_schema_ref": "tsb_tool_call.schema.json",
        "response_schema_ref": "tsb_tool_response.schema.json",
        "mutability": "write",
        "approval_sensitivity": "low",
        "budget_sensitive": True,
    },
    "growth.experiment.review": {
        "description": "Review experiment outcomes and recommendations.",
        "request_schema_ref": "tsb_tool_call.schema.json",
        "response_schema_ref": "tsb_tool_response.schema.json",
        "mutability": "read",
        "approval_sensitivity": "low",
        "budget_sensitive": False,
    },
    "sales.pipeline.read": {
        "description": "Read the active commercial pipeline.",
        "request_schema_ref": "tsb_tool_call.schema.json",
        "response_schema_ref": "tsb_tool_response.schema.json",
        "mutability": "read",
        "approval_sensitivity": "low",
        "budget_sensitive": False,
    },
    "sales.pipeline.update": {
        "description": "Update opportunity status or commercial next steps.",
        "request_schema_ref": "tsb_tool_call.schema.json",
        "response_schema_ref": "tsb_tool_response.schema.json",
        "mutability": "write",
        "approval_sensitivity": "medium",
        "budget_sensitive": False,
    },
    "sales.pricing.propose": {
        "description": "Propose pricing or packaging changes.",
        "request_schema_ref": "tsb_tool_call.schema.json",
        "response_schema_ref": "tsb_tool_response.schema.json",
        "mutability": "write",
        "approval_sensitivity": "high",
        "budget_sensitive": True,
    },
    "finance.plan.read": {
        "description": "Read current financial plan, runway, and obligations.",
        "request_schema_ref": "tsb_tool_call.schema.json",
        "response_schema_ref": "tsb_tool_response.schema.json",
        "mutability": "read",
        "approval_sensitivity": "low",
        "budget_sensitive": False,
    },
    "finance.plan.write": {
        "description": "Update planning assumptions and budget allocations.",
        "request_schema_ref": "tsb_tool_call.schema.json",
        "response_schema_ref": "tsb_tool_response.schema.json",
        "mutability": "write",
        "approval_sensitivity": "high",
        "budget_sensitive": True,
    },
    "finance.raise.propose": {
        "description": "Propose a fundraising plan or financing action.",
        "request_schema_ref": "tsb_tool_call.schema.json",
        "response_schema_ref": "tsb_tool_response.schema.json",
        "mutability": "write",
        "approval_sensitivity": "high",
        "budget_sensitive": False,
    },
    "people.hiring.read": {
        "description": "Read open roles, candidates, and hiring funnel state.",
        "request_schema_ref": "tsb_tool_call.schema.json",
        "response_schema_ref": "tsb_tool_response.schema.json",
        "mutability": "read",
        "approval_sensitivity": "low",
        "budget_sensitive": False,
    },
    "people.hiring.update": {
        "description": "Advance or modify the hiring process.",
        "request_schema_ref": "tsb_tool_call.schema.json",
        "response_schema_ref": "tsb_tool_response.schema.json",
        "mutability": "write",
        "approval_sensitivity": "medium",
        "budget_sensitive": True,
    },
    "people.org.propose": {
        "description": "Propose reporting-line or org changes.",
        "request_schema_ref": "tsb_tool_call.schema.json",
        "response_schema_ref": "tsb_tool_response.schema.json",
        "mutability": "write",
        "approval_sensitivity": "high",
        "budget_sensitive": True,
    },
    "ops.incident.read": {
        "description": "Read operational incidents and queue state.",
        "request_schema_ref": "tsb_tool_call.schema.json",
        "response_schema_ref": "tsb_tool_response.schema.json",
        "mutability": "read",
        "approval_sensitivity": "low",
        "budget_sensitive": False,
    },
    "ops.incident.respond": {
        "description": "Take an incident response action.",
        "request_schema_ref": "tsb_tool_call.schema.json",
        "response_schema_ref": "tsb_tool_response.schema.json",
        "mutability": "write",
        "approval_sensitivity": "high",
        "budget_sensitive": True,
    },
    "board.read": {
        "description": "Read board requests, obligations, and prior updates.",
        "request_schema_ref": "tsb_tool_call.schema.json",
        "response_schema_ref": "tsb_tool_response.schema.json",
        "mutability": "read",
        "approval_sensitivity": "low",
        "budget_sensitive": False,
    },
    "board.update": {
        "description": "Issue a formal board update artifact.",
        "request_schema_ref": "tsb_tool_call.schema.json",
        "response_schema_ref": "tsb_tool_response.schema.json",
        "mutability": "write",
        "approval_sensitivity": "high",
        "budget_sensitive": False,
    },
    "research.market.read": {
        "description": "Read external market and competitor research artifacts.",
        "request_schema_ref": "tsb_tool_call.schema.json",
        "response_schema_ref": "tsb_tool_response.schema.json",
        "mutability": "read",
        "approval_sensitivity": "low",
        "budget_sensitive": False,
    },
    "notes.read": {
        "description": "Read persistent operator notes.",
        "request_schema_ref": "tsb_tool_call.schema.json",
        "response_schema_ref": "tsb_tool_response.schema.json",
        "mutability": "read",
        "approval_sensitivity": "low",
        "budget_sensitive": False,
    },
    "notes.write": {
        "description": "Write persistent operator notes.",
        "request_schema_ref": "tsb_tool_call.schema.json",
        "response_schema_ref": "tsb_tool_response.schema.json",
        "mutability": "write",
        "approval_sensitivity": "low",
        "budget_sensitive": False,
    },
    "sim.advance": {
        "description": "Advance simulation time and process due events.",
        "request_schema_ref": "tsb_tool_call.schema.json",
        "response_schema_ref": "tsb_tool_response.schema.json",
        "mutability": "write",
        "approval_sensitivity": "low",
        "budget_sensitive": False,
    },
}


def tool_manifest_for_names(tool_names: list[str]) -> dict:
    tools = []
    for tool_name in tool_names:
        if tool_name not in _TOOL_CATALOG:
            raise KeyError(f"Unknown tool in scenario: {tool_name}")
        tool = {"tool_name": tool_name, **_TOOL_CATALOG[tool_name]}
        tools.append(tool)
    return {
        "manifest_version": "0.1.0",
        "tools": tools,
    }


__all__ = ["tool_manifest_for_names"]

