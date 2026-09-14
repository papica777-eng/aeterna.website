import shutil
from pathlib import Path

files_to_sync = [
    "CLINICAL_DOCTOR_PORTAL.html",
    "tcga_cohort_samples.json",
    "tcga_logic.js",
    "EPIGENETIC_BIFURCATION_CURIE_MEMORANDUM.md",
    "CURIE_TRANSMITTAL_LETTER_BARILLOT.md",
    "CLINICAL_ETHICS_PROTOCOL_MU_SOFIA.md",
    "ETHICS_APPLICATION_FORM_MU_SOFIA.md",
    "GDPR_ART9_ETHICS_DECLARATION.md",
    "run_hospital_edge_service.bat",
    "install_hospital_windows_service.ps1",
    "run_hospital_pqc_gateway.bat",
    "aeterna_hospital_ota_updater.py",
    "install_hospital_ota_updater.ps1",
    "NZIS_FHIR_INTEGRATION_SPEC.md",
    "nzis_fhir_adapter.py",
    "nzis_oncology_fhir_sample.json",
    "clinical_manifest.json",
    "AETERNA_VHT_HOSPITAL_DEPLOYMENT_MANUAL.md",
    "HOSPITAL_IT_DIRECTOR_TRANSMITTAL_LETTER_MU_SOFIA.md"
]

src_dir = Path(r"z:\aeterna.website")
docs_dir = Path(r"z:\aeterna.website\docs")
desktop_file = Path(r"C:\Users\papic\Desktop\AETERNA_VHT_CLINICAL_DOCTOR_PORTAL.html")
omni_dir = Path(r"c:\Users\papic\AETERNA-PLATFORM\OMNI-VIVISECTOR\soul\BRUTAL_MODULES\aeterna_selye_engine")

print("=== SYNCING MASTER CLINICAL SUITE ACROSS ALL DIRECTORIES ===")
for fname in files_to_sync:
    src_file = src_dir / fname
    if not src_file.exists():
        continue
    
    # 1. Sync to docs
    try:
        shutil.copy2(src_file, docs_dir / fname)
        print(f"✓ docs/{fname}")
    except Exception as e:
        print(f"❌ docs/{fname}: {e}")
        
    # 2. Sync to OMNI-VIVISECTOR
    try:
        shutil.copy2(src_file, omni_dir / fname)
        print(f"✓ omni/{fname}")
    except Exception as e:
        print(f"❌ omni/{fname}: {e}")

# Copy portal to Desktop
try:
    shutil.copy2(src_dir / "CLINICAL_DOCTOR_PORTAL.html", desktop_file)
    print(f"✓ Desktop/AETERNA_VHT_CLINICAL_DOCTOR_PORTAL.html")
except Exception as e:
    print(f"❌ Desktop copy failed: {e}")

# Copy generated PDFs to Desktop and docs
desktop_dir = Path(r"C:\Users\papic\Desktop")
for pdf_name in ["AETERNA_VHT_HOSPITAL_DEPLOYMENT_MANUAL.pdf", "HOSPITAL_IT_DIRECTOR_TRANSMITTAL_LETTER_MU_SOFIA.pdf"]:
    pdf_src = src_dir / "generated" / pdf_name
    if pdf_src.exists():
        try:
            shutil.copy2(pdf_src, desktop_dir / pdf_name)
            print(f"✓ Desktop/{pdf_name}")
        except Exception as e:
            print(f"❌ Desktop copy {pdf_name} failed: {e}")
        try:
            shutil.copy2(pdf_src, docs_dir / pdf_name)
            print(f"✓ docs/{pdf_name}")
        except Exception as e:
            print(f"❌ docs copy {pdf_name} failed: {e}")

print("=== ALL ARTIFACTS FULLY SYNCHRONIZED ===")
