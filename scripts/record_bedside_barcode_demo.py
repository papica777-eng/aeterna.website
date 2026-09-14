#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==============================================================================
=== BEDSIDE 5-RIGHTS BARCODE INTERACTION & SCREENSHOT AUDITOR              ===
=== Validates Hardware Laser Scanner Emulation in Clinical Portal Tab 3    ===
==============================================================================
"""

import os
from playwright.sync_api import sync_playwright

ARTIFACT_DIR = r"C:\Users\papic\.gemini\antigravity-ide\brain\67cdfc38-c943-440e-b971-43dc677d7a82"
HTML_PATH = os.path.abspath(r"z:\aeterna.website\CLINICAL_DOCTOR_PORTAL.html")

def run_barcode_demo():
    print("=== STARTING BEDSIDE 5-RIGHTS BARCODE SCANNER AUDIT ===")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()

        page.goto(f"file:///{HTML_PATH}")
        page.wait_for_timeout(1000)

        # Navigate to Tab 3 (Nurse / Bedside Safety Terminal)
        page.click("#btnNavNurse")
        page.wait_for_timeout(500)
        print("✓ Switched to Tab 3 via #btnNavNurse")

        # Capture Initial Tab 3 State (Idle)
        init_shot = os.path.join(ARTIFACT_DIR, "bedside_scan_step0_idle.png")
        page.screenshot(path=init_shot)
        print(f"✓ Saved idle state: {init_shot}")

        # Scenario 1: Valid Scan (Match)
        current_pid = page.evaluate("getCalculatedPrescription().patientId")
        page.evaluate(f"setBedsideWristband('{current_pid}')")
        page.evaluate("loadCurrentBagIntoBedside()")
        page.click("#bedsideVerifyBtn")
        page.wait_for_timeout(800)

        status_badge = page.inner_text("#bedsideStatusBadge")
        print(f"  • Match Status Badge: {status_badge}")
        match_shot = os.path.join(ARTIFACT_DIR, "bedside_scan_step1_verified_safe.png")
        page.screenshot(path=match_shot)
        print(f"✓ Saved verified state: {match_shot}")

        # Scenario 2: Patient Mismatch (Lockout & Alarm)
        page.fill("#bedsideWristbandInput", "PT-WRONG-PATIENT-999")
        page.click("#bedsideVerifyBtn")
        page.wait_for_timeout(800)

        mismatch_badge = page.inner_text("#bedsideStatusBadge")
        print(f"  • Mismatch Status Badge: {mismatch_badge}")
        mismatch_shot = os.path.join(ARTIFACT_DIR, "bedside_scan_step2_mismatch_lockout.png")
        page.screenshot(path=mismatch_shot)
        print(f"✓ Saved mismatch lockout state: {mismatch_shot}")

        # Restore valid match
        page.evaluate(f"setBedsideWristband('{current_pid}')")
        page.click("#bedsideVerifyBtn")
        page.wait_for_timeout(500)

        browser.close()
    print("=== BEDSIDE BARCODE DEMO COMPLETE: 3 HIGH-RES ARTIFACTS CAPTURED ===")

if __name__ == "__main__":
    run_barcode_demo()
