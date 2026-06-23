"""Week 3 - signature layer: fast, readable rules for known attack patterns.

This is the cheap first stage of the hybrid: obvious known-bad flows are caught by
simple deterministic rules (no model needed), and only what passes is handed to the
ML / anomaly layer. Each rule reads one flow (a dict) and returns a label or None.
"""
from __future__ import annotations

from typing import Callable, Optional

Rule = Callable[[dict], Optional[str]]


def rule_port_scan_like(row: dict) -> Optional[str]:
    """Tiny connections with almost no payload in a scan-like state."""
    if (row.get("spkts", 0) or 0) <= 2 and (row.get("sbytes", 0) or 0) < 100 \
            and row.get("state") in {"INT", "REQ"}:
        return "PortScan(rule)"
    return None


def rule_brute_force_like(row: dict) -> Optional[str]:
    """High connection rate to an auth-style service."""
    if (row.get("rate", 0) or 0) > 1000 and row.get("service") in {"ftp", "ssh", "smtp"}:
        return "BruteForce(rule)"
    return None


def rule_data_exfil_like(row: dict) -> Optional[str]:
    """Large outbound transfer with tiny inbound = possible exfiltration."""
    if (row.get("sbytes", 0) or 0) > 1_000_000 and (row.get("dbytes", 0) or 0) < 1_000:
        return "DataExfil(rule)"
    return None


DEFAULT_RULES: list[Rule] = [rule_port_scan_like, rule_brute_force_like, rule_data_exfil_like]


def match(row: dict, rules: list[Rule] = DEFAULT_RULES) -> Optional[str]:
    """Return the first matching rule's label, or None if nothing matches."""
    for rule in rules:
        label = rule(row)
        if label:
            return label
    return None
