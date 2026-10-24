"""
CLI Command to inspect and audit question bank health across all topics.
Usage:
    python -m app.cli.validate_bank
    python backend/app/cli/validate_bank.py
"""

import sys
import json
from app.core.database import SessionLocal, init_db
from app.services.question_bank_validator import QuestionBankValidator


def print_table_report():
    init_db()
    with SessionLocal() as db:
        report = QuestionBankValidator.validate_all(db)

    summary = report["summary"]
    topics = report["topics"]

    print("\n" + "=" * 105)
    print("                      MASTERYLOOP QUESTION BANK VALIDATION REPORT")
    print("=" * 105)
    header = f"{'Domain':<26} | {'Topic':<32} | {'Total':<5} | {'Valid':<5} | {'Adaptive':<8} | {'Dupes':<5} | {'Status':<10}"
    print(header)
    print("-" * 105)

    for t in topics:
        dom = (t["domain_name"] or "")[:25]
        top = (t["topic_name"] or "")[:31]
        tot = str(t["total_questions"])
        val = str(t["valid_usable_questions"])
        adap = str(t["adaptive_available_questions"])
        dups = str(t["duplicate_count"])
        status = t["status"]
        status_display = status
        if status == "OPTIMAL":
            status_display = "[OK] OPTIMAL"
        elif status == "SUFFICIENT":
            status_display = "[*] SUFFICIENT"
        else:
            status_display = "[!] SHORTAGE"

        row = f"{dom:<26} | {top:<32} | {tot:<5} | {val:<5} | {adap:<8} | {dups:<5} | {status_display:<10}"
        print(row)

    print("=" * 105)
    print("SUMMARY:")
    print(f"  * Total Questions in DB:          {summary['total_items_in_database']}")
    print(f"  * Total Usable Questions:         {summary['total_valid_usable_items']}")
    print(f"  * Total Adaptive-Ready Questions: {summary['total_adaptive_available_items']}")
    print(f"  * Total Topics:                   {summary['total_topics']}")
    print(f"  * Topics Reaching Target (15+):   {summary['topics_meeting_target_15']}/{summary['total_topics']}")
    print(f"  * Topics Reaching Minimum (10+):  {summary['topics_meeting_minimum_10']}/{summary['total_topics']}")
    print(f"  * Topics with Shortage (<10):     {summary['topics_with_shortage']}/{summary['total_topics']}")
    print("=" * 105)

    if summary["topics_with_shortage"] > 0:
        print("\nTOPIC SHORTAGES IDENTIFIED:")
        for t in topics:
            if t["status"] == "SHORTAGE":
                print(f"  - [{t['domain_name']}] {t['topic_name']}: {t['valid_usable_questions']} valid questions (needs at least {summary['configured_min_questions']})")
        print()

    return report


if __name__ == "__main__":
    rep = print_table_report()
    if "--json" in sys.argv:
        print(json.dumps(rep, indent=2))
