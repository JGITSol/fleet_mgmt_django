# Security Protocol & Checklist: Non-VPN Online Authentication

This document outlines the security protocols and checklist for the Fleet Management Flutter Application when operating over the public internet (non-VPN).

## 1. Transport Layer Security (Data in Transit)

- [ ] **Enforce HTTPS**: Ensure all API calls use `https://` only. HTTP traffic must be rejected or redirected by the backend.
- [ ] **SSL/TLS Certificate**: Verify the backend has a valid, up-to-date SSL certificate (e.g., Let's Encrypt, AWS ACM).
- [ ] **Certificate Pinning (Recommended)**: Implement certificate pinning in the Flutter app to prevent Man-in-the-Middle (MITM) attacks.
    - *Tools*: `dio` HTTP client supports certificate pinning.
- [ ] **Disable Cleartext Traffic**: In Android `AndroidManifest.xml`, ensure `android:usesCleartextTraffic="false"` (default in Android 9+).

## 2. Authentication & Session Management

- [ ] **JWT Implementation**:
    - [ ] **Access Tokens**: Short-lived (e.g., 5-15 minutes).
    - [ ] **Refresh Tokens**: Long-lived (e.g., 1-7 days), used *only* to obtain new access tokens.
- [ ] **Secure Storage**:
    - **NEVER** store tokens in `SharedPreferences` or `NSUserDefaults` (cleartext).
    - [ ] **Implementation**: Use `flutter_secure_storage` to store Access and Refresh tokens.
        - *Android*: Uses EncryptedSharedPreferences (Keystore).
        - *iOS*: Uses Keychain.
- [ ] **Token Rotation**:
    - [ ] Implement secure interceptors in the API client (e.g., Dio Interceptor) to automatically refresh tokens on `401 Unauthorized` errors.
    - [ ] If refresh fails, force logout and clear local storage.
- [ ] **Logout Mechanism**:
    - [ ] Ensure "Logout" clears tokens from `flutter_secure_storage`.
    - [ ] Call backend logout endpoint to blacklist/revoke the refresh token if supported.

## 3. Data Protection (Data at Rest)

- [ ] **Sensitive Data**: Avoid storing sensitive user PII locally unless necessary.
- [ ] **Local Database Encryption**:
    - If using `sqflite` or `hive` for offline caching (future roadmap), ensure encryption keys are stored in `flutter_secure_storage`.

## 4. Application Hardening

- [ ] **Code Obfuscation**:
    - Build release APKs/Bundles with obfuscation enabled.
    - Command: `flutter build apk --obfuscate --split-debug-info=/<project-name>/<directory>`
- [ ] **API Keys**:
    - Do not hardcode API keys (e.g., Google Maps) in the repo. Use strict restrictions (SHA-1 fingerprint restriction for Android) in the Google Cloud Console.

## 5. Network Security Best Practices

- [ ] **Timeouts**: Configure reasonable connection and receive timeouts (e.g., 10-30 seconds) to prevent hanging requests.
- [ ] **Error Handling**:
    - Generic error messages for login failures (e.g., "Invalid credentials" instead of "User not found").
    - Do not display raw stack traces or backend 500 errors to the user.

## 6. Pre-Release Security Checklist

- [ ] Run `flutter doctor -v` and ensure no issues.
- [ ] Verify `android/app/src/main/AndroidManifest.xml` permissions are minimal (only what is needed).
- [ ] Test login flow on a physical device over a standard 4G/5G connection.
- [ ] Test token refresh by manually expiring the token or waiting.
- [ ] Verify app behavior when internet connection is lost.
