# Stage 13 — Annual Update & Monitoring Protocol (IJRIO)

* **Effective Date**: 2026-11-24
* **Cadence**: Annual (Q1 post-Mahkamah Agung Annual Report / LAPTAH release), plus ad-hoc triggers on major statutory enactments (e.g., `UU 20/2025` KUHAP, `UU 1/2023` KUHP).

## Annual Cycle Checklist
1. **PERMA Harvest & Diff**: Query [JDIH BPK RI](https://peraturan.bpk.go.id/), [Peraturan.go.id](https://peraturan.go.id/), and [JDIH MA RI](https://jdih.mahkamahagung.go.id/) for newly promulgated PERMA and amendment/repeal notices.
2. **Coherence & Status Audit**: Re-verify `current_legal_status` and `legal_coherence.csv` flags (`UU 20/2025`, `UU 27/2022`, `UU 1/2023`, `UU 6/2023`).
3. **Indicator Refresh**: Extract updated annual e-Court, mediation, small-claims, and e-Berpadu metrics from the latest LAPTAH MA.
4. **Automated Monitoring & QA**: Run `python3 scripts/annual_monitoring_check.py`, `python3 scripts/validate_registry.py`, and `python3 scripts/validate_sources.py`.
5. **Versioned Release**: Tag release (`v1.x.0`), push to GitHub, and update Kaggle (`kaggle datasets version`) after human sign-off.
