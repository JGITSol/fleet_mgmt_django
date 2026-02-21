# Flutter Client API Interaction Format

This document specifies the required request format for interacting with the Fleet Management API, specifically for reporting emergencies and responses.

## Content-Type Support

The API now supports both `application/json` (standard for Flutter/Dio) and `multipart/form-data` (legacy support).

## Reporting an Emergency Incident

**Endpoint**: `POST /api/emergencies/`
**Auth Required**: Bearer Token (JWT)

### Recommended JSON Format (Standard JS/Flutter)

```json
{
  "vehicle": 1,
  "emergency_type": "ACCIDENT",
  "location": "123 Main St, New York",
  "latitude": 40.7128,
  "longitude": -74.0060,
  "description": "Minor fender bender at the intersection."
}
```

### Response (201 Created)

```json
{
  "id": 42,
  "vehicle": 1,
  "reported_by": 5,
  "emergency_type": "ACCIDENT",
  "status": "REPORTED",
  "location": "123 Main St, New York",
  "latitude": "40.712800",
  "longitude": "-74.006000",
  "description": "Minor fender bender at the intersection.",
  "reported_time": "2026-02-18T23:15:00Z",
  "resolved_time": null
}
```

## Field Specifications

- **`vehicle`**: Integer (ID of the vehicle).
- **`emergency_type`**: String enum (`ACCIDENT`, `BREAKDOWN`, `MEDICAL`, `THEFT`, `OTHER`).
- **`location`**: String.
- **`latitude` / `longitude`**: Optional decimal strings or numbers.
- **`description`**: String.

## Error Handling

- **415 Unsupported Media Type**: Ensure your `headers` include `"Content-Type": "application/json"`.
- **403 Forbidden**: Ensure your `Authorization` header includes `"Bearer <your_access_token>"`.
- **400 Bad Request**: Check the response body for field validation errors.

## Handling Media & Attachments (Images/Videos)

The API now supports media uploads for emergency incidents and responses.

### 1. Request Format: `multipart/form-data`

When sending files, you **must** use `multipart/form-data` instead of JSON. 
In Flutter (using Dio):

```dart
FormData formData = FormData.fromMap({
  "vehicle": 1,
  "emergency_type": "ACCIDENT",
  "location": "123 Main St",
  "description": "Fender bender",
  "attachment": await MultipartFile.fromFile("./path/to/image.jpg", filename: "incident.jpg"),
  "video_attachment": await MultipartFile.fromFile("./path/to/video.mp4", filename: "incident.mp4"),
});

response = await dio.post("/api/emergencies/", data: formData);
```

### 2. Available Fields for Media

#### Emergency Incident (`POST /api/emergencies/`)
- **`attachment`**: Image file (JPG/PNG).
- **`video_attachment`**: Video or other file.

#### Emergency Response (`POST /api/emergencies/responses/`)
- **`attachment`**: File (completion report, photo of repair, etc.).

### 3. Response Data

When retrieving incidents (`GET /api/emergencies/`), the API provides absolute URLs for media:

```json
{
  "id": 42,
  "attachment": "/media/emergency/incidents/incident.jpg",
  "attachment_url": "http://192.168.1.12:8000/media/emergency/incidents/incident.jpg",
  "video_attachment": "/media/emergency/videos/incident.mp4"
}
```

## Vehicle Gallery (Digital Assets)

The gallery supports images, videos, and sounds for each fleet vehicle.

**Endpoint**: `GET /api/vehicles/media/`
**Endpoint**: `POST /api/vehicles/media/`

### 1. Uploading to Gallery (multipart/form-data)

```dart
FormData formData = FormData.fromMap({
  "vehicle": 1, 
  "media_type": "IMAGE", // IMAGE, VIDEO, SOUND
  "title": "Front Right Fender",
  "description": "Visual check during routine inspection",
  "file": await MultipartFile.fromFile("./path/to/media.jpg", filename: "gall.jpg"),
});

response = await dio.post("/api/vehicles/media/", data: formData);
```

### 2. Retrieving Gallery Items
You can filter media by vehicle ID using query parameters:
`GET /api/vehicles/media/?vehicle=1`

### 3. Media Types Supported
- **IMAGE**: JPG, PNG
- **VIDEO**: MP4, MOV
- **SOUND**: MP3, WAV (Engine diagnostics, driver voice notes)

## Summary of Current Connection Data
| Requirement | Current Value |
|-------------|---------------|
| **Base URL** | `http://192.168.1.12:8000/api` |
| **Media URL** | `http://192.168.1.12:8000/media/` |
| **PC IP (WiFi)** | `192.168.1.12` |
| **Port** | `8000` |
| **Dev Settings** | `CarFleetManagement.settings.dev` |

Document updated February 2026.
