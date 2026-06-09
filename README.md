# Live Deal Feed

A automated pipeline and modern static dashboard designed to fetch and showcase active restaurant/meal deals from a Google Firestore backend (specifically configured for Los Angeles). It features a clean, responsive user interface and automatic deployment to GitHub Pages.

## Features

- **Firestore Query Integration**: Connects to the Firebase API with target device/package metadata to fetch active offers.
- **Modern Responsive Dashboard**: Displays deals with dynamic badges (tailored for Lakers, Dodgers, Kings, and manual deals), expiration timers, and external promo links.
- **Headless / CI Support**: The generation script detects when it's running in a continuous integration environment (like GitHub Actions) and skips opening the browser.
- **Automated Deployments**: A GitHub Actions workflow automatically rebuilds and deploys the dashboard to GitHub Pages on schedule and on code pushes.

---

## Getting Started

### Prerequisites

Ensure you have **Python 3.8+** installed on your system.

### Installation

Clone the repository and install the required Python dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

### 1. Generating & Previewing Locally (Standard Mode)

To generate the dashboard and immediately open it in your default web browser for preview:

```bash
python meal_html.py
```
*Output file: `deals_dashboard.html`*

### 2. Generating a Custom File (e.g. for GitHub Pages)

To generate the dashboard under a specific file name (e.g., `index.html`) without opening the browser (using the `CI` environment variable):

```bash
# On Linux/macOS
CI=true python meal_html.py index.html

# On Windows (PowerShell)
$env:CI="true"; python meal_html.py index.html
```

---

## GitHub Actions & GitHub Pages Deployment

The project is fully integrated with GitHub Actions to keep the live deal feed up to date:

- **Schedule**: The workflow runs automatically **daily at 1:00 AM Pacific Time** (8:00 AM UTC) to pull new live deals.
- **On Push**: Every push to the `master` branch triggers a build to publish updates immediately.
- **Manual Trigger**: The workflow can be run manually from the Actions tab on GitHub (`workflow_dispatch`).
- **Deployment**: The workflow outputs `index.html` and deploys it directly to GitHub Pages.