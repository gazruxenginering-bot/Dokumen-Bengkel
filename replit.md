# Google Drive File Browser

## Overview

A Flask-based web application that indexes and provides a browsable interface for Google Drive folders containing PDF files and documents. The application uses a Google Service Account for authentication, maintains a local SQLite database for file indexing, and includes a server-side proxy for streaming files to avoid CORS issues. The system is designed for deployment on platforms like Railway or Render with minimal configuration.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Architecture

**Web Framework**: Flask 3.1.0 with Gunicorn WSGI server (4 workers) for production deployment

**Database Strategy**: SQLite-based file index with dual-mode support:
- Default: Local `database.db` file for development and ephemeral deployments
- Production: Optional PostgreSQL via `DATABASE_URL` environment variable (partial support - SQLAlchemy migration recommended for full Postgres compatibility)
- Current implementation uses raw SQLite3 connections rather than ORM

**Authentication Model**: Google Service Account credentials
- Supports environment variable injection (`SERVICE_ACCOUNT_JSON`) for platforms that don't allow file uploads
- Credentials written to filesystem at startup when provided via environment
- Uses `google-auth` library with read-only Drive API scopes

**File Indexing**: Synchronization script (`drive_sync.py`) that:
- Recursively crawls configured Google Drive root folders
- Stores file metadata (name, MIME type, size, modified time, parent relationships) in SQLite
- Maintains folder hierarchy with `parent_id` relationships
- Tags files with `root_folder_name` for categorization

**File Proxy Architecture**: Server-side streaming proxy to bypass CORS restrictions
- `/download/<file_id>` endpoint streams files from Google Drive
- Uses service account credentials for authorized access
- Implements `stream_with_context` for efficient large file handling

### Frontend Architecture

**Template Engine**: Jinja2 templates with responsive design
- Base template with theme switching (light/dark mode)
- Grid and list view toggles for file browsing
- PDF.js integration for client-side PDF rendering (v3.10.251 from CDN)
- Fallback to Google Drive native preview when PDF.js fails

**View Structure**:
- Homepage: Category/root folder listing with statistics
- Folder view: Hierarchical file/folder browsing with breadcrumbs
- Search: Full-text search across indexed files
- PDF viewer: Dual-mode (PDF.js canvas rendering + Drive iframe fallback)

**UI/UX Patterns**:
- CSS custom properties for theming
- Font Awesome icons for visual consistency
- Responsive grid layouts
- Client-side sorting and view mode switching

### Data Storage

**Primary Database**: SQLite (`database.db`)
- Schema: `files` table with columns for Drive metadata
- No ORM layer (raw SQL with `sqlite3` module)
- Ephemeral on Railway/Render unless mounted to persistent volume

**Alternative ORM Model**: Incomplete Flask-SQLAlchemy setup in `models.py`
- Defines `File` model but not actively used
- Suggests planned migration to SQLAlchemy for better Postgres support

**Configuration Management**: Centralized in `config.py`
- Database path resolution with `DATABASE_URL` fallback logic
- Root folder IDs for Drive synchronization
- Service account file paths

### External Dependencies

**Google Drive API Integration**:
- `google-api-python-client` v2.150.0 for Drive v3 API
- `google-auth` v2.43.0 for service account authentication
- Scopes: `https://www.googleapis.com/auth/drive.readonly`
- API operations: file listing, metadata retrieval, file download

**Service Account Requirements**:
- Must have read access to all indexed Drive folders
- Credentials provided via `credentials.json` file or `SERVICE_ACCOUNT_JSON` environment variable
- Project: `studio-9399526178-46fef` (Firebase Admin SDK service account)

**Deployment Platforms**:
- **Railway**: Primary deployment target with `railway.json` configuration
  - Nixpacks build system
  - Health check endpoint: `/healthz`
  - Auto-scaling with restart policies
- **Render**: Alternative deployment with `render.yaml` support (mentioned but config not provided)

**Third-Party Services**:
- Google Drive API (googleapis.com)
- CDN resources: Font Awesome 6.4.0, PDF.js 3.10.251

**Production Server**: Gunicorn v23.0.0
- Configuration: 4 worker processes, binds to `0.0.0.0:$PORT`
- Gevent worker class for async I/O (gevent v24.11.1 included in dependencies)

**Key Python Dependencies**:
- Flask 3.1.0 (web framework)
- requests (HTTP client for Drive file streaming)
- google-api-python-client (Drive API)
- gunicorn (WSGI server)
- Additional scientific/data libraries (unused: matplotlib, numpy, pandas suggest possible future features or legacy dependencies)

**Configuration Hierarchy**:
1. Environment variables (`SERVICE_ACCOUNT_JSON`, `DATABASE_URL`, `FLASK_DEBUG`, `PORT`)
2. `config.py` for application constants
3. Hardcoded root folder IDs in multiple locations (config.py, app.py, drive_sync.py - potential maintenance issue)