# P4 deviation / incident template

**Purpose:** One card per technical or protocol incident.  
**Acceptance:** All fields filled before any resume/restart decision.

```markdown
# Deviation / incident: <slug>

- UTC start:
- UTC end:
- Gate:
- Host (no secrets in public copy):
- Operator:
- Command SHA-256 / argv class:
- PID:
- Input paths + SHA:
- Output paths:
- Observed **safe** symptom (finite/path/hash; no BPB):
- Official steps completed (0 / N / unknown):
- Outcomes accessed? (yes/no):
- Quarantine path:
- Disposition: repair-and-repreflight / clean restart from C0 / protocol_stop / other (describe)
- Why this is not outcome-informed arm or budget change:
- Authority sign-off:
- Follow-up artifact:
```

Public run cards **MUST** omit SSH, passcodes, and lockbox plaintext.
