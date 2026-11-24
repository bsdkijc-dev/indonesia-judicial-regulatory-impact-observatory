# IJRIO v1.0 — Data Dictionary & Kaggle Package Documentation

* **Update Date**: 2026-11-24
* **License**: `CC-BY-4.0` (metadata, schema, and analytical tables); `MIT` (validation/analysis scripts). Official PERMA legal texts are linked to `peraturan.bpk.go.id` and `peraturan.go.id` rather than redistributed.
* **Disclaimer**: Independent academic research dataset. **Not** an official Mahkamah Agung RI database.

## 13 Master Tables
1. `perma_registry.csv` / `.jsonl` (57 rows): `perma_id`, `perma_number`, `year`, `official_title`, `issuing_institution`, `promulgation_date`, `effective_date`, `berita_negara`, `official_source_url`, `subject_matter`, `regulatory_objective`, `legal_basis`, `related_regulations`, `document_type`, `amendment_history`, `repeal_or_replacement_status`, `current_legal_status`, `verification_status`, `verification_date`.
2. `perma_legal_status.csv` (57 rows): `status_id`, `perma_id`, `current_legal_status`, `document_type`, `amendment_history`, `repeal_or_replacement_status`, `verification_status`, `source_url`, `verification_date`.
3. `legal_coherence.csv` (20 rows): `coherence_id`, `perma_id`, `superior_law_consistency`, `regulatory_overlaps`, `contradictions_or_gaps`, `subsequent_context_changes`, `evidence_status`, `source_url`, `retrieval_date`.
4. `source_registry.csv` (15 rows): `source_id`, `source_name`, `hierarchy_level`, `source_type`, `base_url`, `access_status`, `publication_date`, `retrieval_date`, `notes`.
5. `regulatory_problems.csv` (5 rows): `problem_id`, `perma_id`, `pre_regulation_problem`, `establishing_evidence`, `affected_groups`, `problem_definition_quality`, `evidence_status`, `source_url`, `retrieval_date`.
6. `regulatory_objectives.csv` (5 rows): `objective_id`, `perma_id`, `stated_objective`, `is_specific_measurable`, `indicators_established`, `implementing_unit`, `evidence_status`, `source_url`, `retrieval_date`.
7. `implementation_evidence.csv` (8 rows): `impl_id`, `perma_id`, `court_tier`, `region`, `guidance_available`, `resources_provided`, `implementation_finding`, `evidence_type`, `evidence_status`, `source_url`, `retrieval_date`.
8. `impact_indicators.csv` (9 rows): `indicator_id`, `perma_id`, `indicator_name`, `dimension`, `baseline_value`, `post_value`, `unit`, `observation_period`, `causal_design`, `evidence_status`, `source_url`, `retrieval_date`.
9. `stakeholder_impacts.csv` (8 rows): `stakeholder_impact_id`, `perma_id`, `stakeholder_group`, `impact_direction`, `impact_summary`, `evidence_type`, `evidence_status`, `source_url`, `retrieval_date`.
10. `unintended_consequences.csv` (4 rows): `consequence_id`, `perma_id`, `consequence_description`, `cost_transfer_or_inequality`, `institutional_burden`, `evidence_status`, `source_url`, `retrieval_date`.
11. `ria_assessments.csv` (50 rows): `assessment_id`, `perma_id`, `dimension_code`, `dimension_name`, `score_1_to_5_or_NA`, `evidence_status`, `data_limitations`, `reviewer_comments`, `assessment_date`.
12. `recommendations.csv` (5 rows): `recommendation_id`, `perma_id`, `option_code`, `option_label`, `rationale`, `evidence_status`, `human_review_status`, `review_date`.
13. `reviewer_log.csv` & `review_log.csv`: QA and human legal review audit trails.

## Limitations
- Digital coverage focuses on **2009–2025**; pre-2008 archival PERMA are not yet systematically harvested.
- Impact indicators reflect descriptive trends (`DESCRIPTIVE_TREND`, `DESCRIPTIVE_CASE_STUDY`); causal inference requires court-level panel microdata.
- All analytical recommendations are `PENDING_HUMAN_LEGAL_REVIEW`.
