# Nano Banana Output Storage

Store generated images and their decision trail here.

## Required Capture Per Image
- the PNG output
- the exact prompt text used
- the source brief filename
- a short version note
- whether the image is `workbench` or `approved`

## Recommended Naming
Workbench example:

```text
2026-04-20_university-site-plan_v01.png
2026-04-20_university-site-plan_v01.prompt.md
2026-04-20_university-site-plan_v01.notes.md
```

Approved example:

```text
university-site-plan_master_v01.png
university-site-plan_master_v01.prompt.md
university-site-plan_master_v01.decision.md
```

## Generation Order
1. `01-campus`
2. `02-archives`
3. `03-hollows`
4. `04-mains`
5. `05-mews`
6. `06-medica`
7. `07-fishery`
8. `08-haven`
9. `09-underthing`
10. `interiors`

Freeze the approved campus image first, then keep every later prompt aligned to that anchor.
