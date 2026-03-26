![CVE](https://img.shields.io/badge/CVE-2026--29905-red)
# CVE-2026-29905 — Kirby CMS Persistent DoS via Malformed Image Upload

## Overview

A authenticated user with **Editor** permissions can upload a malformed file with an image extension to cause a persistent Denial of Service in Kirby CMS.

**CVE ID:** CVE-2026-29905
**Affected Version:** Kirby CMS ≤ 5.1.4
**Fixed In:** Kirby CMS 5.2.0-rc.1
**Severity:** Medium
**CWE:** CWE-252 (Unchecked Return Value), CWE-20 (Improper Input Validation)

---

## Description

Kirby processes uploaded image files using PHP's `getimagesize()` function without validating its return value. When a malformed file is uploaded with a valid image extension (e.g. `.jpg`), `getimagesize()` returns `false` instead of an array. The application then triggers a fatal `TypeError` during thumbnail generation or metadata processing.

The crash persists across page reloads until the file is manually removed from the filesystem.

---

## Impact

- Any Editor-role user (non-admin) can trigger the DoS condition.
- Affected pages return HTTP 500 until the file is removed manually.

---

## Fix

Patched in [Kirby CMS 5.2.0-rc.1](https://github.com/getkirby/kirby/releases/tag/5.2.0-rc.1).

---

## Discoverer

**Stalin S** ([@Stalin-143](https://github.com/Stalin-143))
