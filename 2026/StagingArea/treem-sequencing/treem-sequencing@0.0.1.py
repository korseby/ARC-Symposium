# /// script
# requires-python = ">=3.11"
# dependencies = ["arcexpect", "arctrl"]
# ///

"""
---
Name: example-validator
MajorVersion: 1
MinorVersion: 0
PatchVersion: 0
Summary: Checks the basic structure of an ARC.
Description: |
  A minimal native-Python ARC validation package.
---
"""

import argparse
from pathlib import Path
from arcexpect import Execute, Expect, Setup, test_case, test_list

parser = argparse.ArgumentParser()
parser.add_argument("--input", "-i", required=True, type=Path)
parser.add_argument("--output", "-o", required=True, type=Path)
args = parser.parse_args()

def investigation_exists() -> None:
    Expect.is_true(
        (args.input / "isa.investigation.xlsx").is_file(),
        "isa.investigation.xlsx not found"
    )

def arc_has_valid_contacts() -> None:
    contacts = arc.Contacts
    Expect.is_true(len(contacts) > 0, "No contacts found.")
    for c in contacts:
        Expect.is_true(c.FirstName != "", f"No first name found for contact: {c}")
        Expect.is_true(c.LastName  != "", f"No last name found for contact: {c}")
        Expect.is_true(c.Affiliation != "", f"No affiliation found for contact: {c}")
        Expect.is_true(c.EMail != "", f"No email found for contact: {c}")
        Expect.is_true(c.ORCID != "", f"No ORCID found for contact: {c}")

package = Setup.validation_package_from_script(
    __file__,
    critical=[
        test_list("ARC structure", [
            test_case("investigation exists", investigation_exists),
            test_case("Title", arc_has_title),
            test_case("Description", arc_has_description),
            test_case("Contacts", arc_has_valid_contacts),
            test_case("License", arc_has_license),
        ])
    ],
)

Execute.validation_pipeline(package, str(args.output))