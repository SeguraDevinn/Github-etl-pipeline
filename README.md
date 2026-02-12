# GitHub Pull Request ETL Pipeline

## Project Overview

This project is a modular ETL pipeline that extracts pull request data from the GitHub API, transforms and enriches it, validates the results, and loads the data into a SQLite warehouse.

The purpose of this project is to simulate a production-style data engineering workflow. It focuses on incremental ingestion, safe upsert logic, clean warehouse modeling, and orchestration readiness. The next phase of the project is integrating the pipeline into Apache Airflow for scheduled and monitored execution.

This is not a simple script-based extractor. The architecture is structured to reflect real-world data pipeline design patterns.

---

## Project Goals

The primary objectives of this project are:

- Build a modular ETL pipeline from scratch.
- Implement incremental loading using a watermark strategy.
- Design a warehouse schema for pull request analytics.
- Prevent duplicate records using upsert logic.
- Prepare the pipeline for orchestration with Apache Airflow.
- Establish a foundation for analytics and reporting.

---

## Architecture Overview

The pipeline follows a layered architecture:

```
Extract → Transform → Enrich → Validate → Load
```

### Extract
- Fetches issues from the GitHub API.
- Filters for pull requests.
- Supports pagination.
- Supports incremental loading using the `since` parameter based on `updated_at`.

### Transform
- Normalizes raw API responses.
- Selects and restructures relevant fields.
- Prepares records for warehouse insertion.

### Enrich
- Fetches additional pull request metadata (additions, deletions, changed files, etc.).
- Adds ingestion and enrichment timestamps.

### Validate
- Ensures required fields are present.
- Filters out malformed or incomplete records.
- Protects the warehouse from bad data.

### Load
- Inserts records into the SQLite warehouse.
- Uses `INSERT ... ON CONFLICT DO UPDATE` logic.
- Enforces uniqueness using `pr_number`.
- Implements incremental behavior via watermark tracking.

---

## Warehouse Design

### Table: `pull_requests`

Key fields include:

- `pr_id`
- `pr_number` (unique identifier)
- `title`
- `author_login`
- `state`
- `created_at`
- `updated_at`
- `closed_at`
- `merged`
- `merged_at`
- `additions`
- `deletions`
- `changed_files`
- `review_comments`
- `repo`
- `ingested_at`
- `enriched_at`

The schema supports:

- Incremental ingestion
- Safe upserts
- Update tracking
- Analytics-ready structure

---

## Incremental Loading Strategy

The pipeline uses a watermark approach:

1. Retrieve the latest `updated_at` timestamp from the warehouse.
2. Pass that timestamp to the GitHub API using the `since` parameter.
3. Fetch only records updated after that watermark.
4. Upsert records safely into the database.

This ensures:

- No duplicate pull requests.
- No unnecessary full refreshes.
- Efficient API usage.
- Production-style incremental behavior.

Testing confirmed that:

- Primary key constraints prevent duplicates.
- Upsert logic works correctly.
- Incremental runs only insert new or updated records.

---

## Running the Pipeline

From the project root directory:

```bash
py -m src.pipeline.run_pipeline
```

The pipeline will:

- Initialize the database if necessary.
- Retrieve the latest warehouse watermark.
- Fetch incremental pull request data.
- Transform and enrich records.
- Validate records.
- Insert them safely into the warehouse.
- Print a structured run summary.

---

## What Has Been Accomplished

- Built a modular ETL pipeline with clear separation of concerns.
- Implemented incremental ingestion using a watermark strategy.
- Designed a normalized warehouse schema.
- Implemented safe upsert logic using conflict resolution.
- Validated duplicate prevention using SQL tests.
- Debugged live-update edge cases from the GitHub API.
- Created a production-style pipeline entry point.
- Structured execution logging and run summaries.

The pipeline is stable and ready for orchestration.

---

## Next Phase: Apache Airflow Integration

The next step is to orchestrate this pipeline using Apache Airflow.

Planned enhancements:

- Convert pipeline steps into Airflow tasks.
- Build a DAG with explicit task dependencies.
- Schedule automated incremental runs.
- Add retry and failure handling logic.
- Record pipeline run metadata.
- Monitor execution through the Airflow UI.

This will transform the project from a standalone ETL script into a fully orchestrated data workflow.

---

## Future Improvements

- Add a `pipeline_runs` metadata tracking table.
- Create analytical views (e.g., average time to merge, contributor activity).
- Support multiple repositories dynamically.
- Add automated tests.
- Containerize the project with Docker.
- Integrate with BI tools for visualization.

---

## Technical Stack

- Python
- SQLite
- GitHub REST API
- Structured logging
- Incremental ETL design patterns
- Apache Airflow (planned)

---

## Summary

This project demonstrates practical data engineering concepts including API ingestion, incremental loading, warehouse modeling, upsert conflict handling, and orchestration readiness. It reflects real-world pipeline architecture rather than a simple scripted extractor and serves as a foundation for scalable data workflows.