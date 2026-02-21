# Project Roadmap

This document outlines the future development path for the Fleet Management System, including the Flutter mobile application and Django backend.

## Phase 1: MVP & Core Security (Current Focus)

- [ ] **Non-VPN Online Authentication**
    - Implement secure JWT checks (Access + Refresh tokens).
    - Enforce HTTPS and disable cleartext traffic.
    - [Reference: SECURITY_PROTOCOL.md](SECURITY_PROTOCOL.md)
- [ ] **Flutter App Core**
    - Implement Login Screen.
    - Implement Dashboard with vehicle stats.
    - Implement Emergency Reporting.
- [ ] **Documentation Standards**
    - Ensure all new code components have Dart/Python docstrings.
    - Maintain `FLUTTER_FULL_SPEC.MD` as the source of truth.

## Phase 2: Enhanced Security & Connectivity

- [ ] **VPN Infrastructure Setup**
    - **Goal**: Restrict backend API access to a private network.
    - **Actions**:
        - Deploy backend to a private VPC (AWS/GCP/Azure) or on-premise server.
        - Setup simple VPN (e.g., WireGuard, OpenVPN) or Tailscale for mobile clients.
        - Update mobile app config to point to internal IP or VPN-resolved domain.
- [ ] **Advanced Authentication**
    - Biometric Login (FaceID / Fingerprint) for the Flutter app.
    - 2FA (Two-Factor Authentication) for Admin web access.

## Phase 3: Offline-First Architecture

- [ ] **Local Data Persistence**
    - **Goal**: Allow drivers to view schedules and report emergencies without internet.
    - **Tech Stack**:
        - Use `hive` or `isar` for high-performance NoSQL local storage, or `sqflite` for relational data.
        - Store JWT tokens securely to allow "offline login" (session validity check).
- [ ] **Data Synchronization (Sync Engine)**
    - **Queueing System**: Capture offline actions (e.g., "Report Emergency", "Complete Maintenance") in a local queue.
    - **Background Sync**: Use `workmanager` or `background_fetch` to push queued data when connectivity is restored.
    - **Conflict Resolution**: Define rules for server-side vs. client-side data conflicts (Server Wins policy recommended).

## Phase 4: Production Readiness & Optimization

- [ ] **Refine Documentation**
    - Auto-generate API docs (Swagger/OpenAPI) and keep them in sync.
    - Create user guides for Drivers and Fleet Managers.
- [ ] **Performance Monitoring**
    - Integrate Crashlytics/Sentry for error application tracking.
    - Monitor API latency and optimize slow Django queries.
