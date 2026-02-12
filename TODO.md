# Project Roadmap & TODO

## High Priority
- [x] Complete UI/UX Overhaul and Theme System
- [ ] Implement Flutter Mobile Application (Start implementation phase)
- [ ] Stabilize Backend Tests (Fix authentication patching issues)

## Backend Refinement
- [ ] Improve test coverage to 80%+
- [ ] Finalize drf-spectacular integration for complete API docs
- [ ] Database migration to PostgreSQL for production

## Infrastructure
- [ ] Setup production deployment pipeline (GitHub Actions -> CD)
- [ ] Implement production monitoring and error tracking (Sentry/Prometheus)

---

### Previous Debug Log (Stale Tests Issue)
The `MaintenanceTestCase` issue regarding `__str__` and `days_until_scheduled` not reflecting code changes was identified as an environment/caching issue. 
Suggested fix: Recreate virtual environment and reinstall dependencies to ensure fresh code execution.