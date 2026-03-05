#!/usr/bin/env python3
"""
Manual Input Demo Loop for Insurance Claim Question-Answering System

This script demonstrates the multi-turn interview process where:
1. User manually enters claim state fields
2. System returns next question from the question bank
3. User manually updates state with new info
4. Repeat until termination condition is met

Generates turn logs in sample_runs/ folder.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Add parent directory to imports
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from app.retriever import QuestionRetriever
from app.state_fusion import extract_and_merge
from app.termination import should_terminate


def initialize_claim_state():
    """Initialize an empty claim state"""
    return {
        "category": None,
        "loss_datetime": None,
        "loss_location": {
            "city": None,
            "state": None,
            "address": None,
            "road_type": None
        },
        "vehicle": {
            "make": None,
            "model": None,
            "year": None
        },
        "drivable": None,
        "third_party_involved": None,
        "third_party_vehicle_id": None,
        "injuries_reported": None,
        "police_report_filed": None,
        "damage_areas": [],
        "already_extracted_categories": [],
        "answered_question_ids": []
    }


def save_turn_log(turn_number, state, question, user_input, output_dir="sample_runs"):
    """Save a turn log to JSON file"""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    log_data = {
        "turn_number": turn_number,
        "timestamp": datetime.now().isoformat(),
        "claim_state_before": state.copy(),
        "question_presented": question,
        "user_input": user_input
    }
    
    filename = f"{output_dir}/Turn_{turn_number:02d}.json"
    with open(filename, 'w') as f:
        json.dump(log_data, f, indent=2)
    
    print(f"✅ Saved turn log: {filename}")


def display_state(state):
    """Display current claim state in a readable format"""
    print("\n" + "="*80)
    print("📋 CURRENT CLAIM STATE")
    print("="*80)
    
    print(f"Category: {state.get('category', 'Not specified')}")
    print(f"Date/Time: {state.get('loss_datetime', 'Not specified')}")
    
    location = state.get('loss_location', {})
    print(f"Location: {location.get('city', 'N/A')}, {location.get('road_type', 'N/A')}")
    
    print(f"Third Party Involved: {state.get('third_party_involved', 'Not specified')}")
    print(f"Drivable: {state.get('drivable', 'Not specified')}")
    print(f"Injuries: {state.get('injuries_reported', 'Not specified')}")
    print(f"Police Report: {state.get('police_report_filed', 'Not specified')}")
    print(f"Damage Areas: {', '.join(state.get('damage_areas', [])) or 'None'}")
    
    print(f"\nExtracted Categories: {', '.join(state.get('already_extracted_categories', [])) or 'None'}")
    print(f"Questions Answered: {len(state.get('answered_question_ids', []))}")
    print("="*80 + "\n")


def display_question(question, turn_number):
    """Display the next question with metadata"""
    if not question:
        print("\n❌ No question returned from retriever")
        return
    
    print("\n" + "="*80)
    print(f"❓ TURN {turn_number} - NEXT QUESTION")
    print("="*80)
    
    print(f"\n🆔 Question ID: {question.get('id')}")
    print(f"📝 Field: {question.get('question_field')}")
    print(f"⭐ Priority: {question.get('priority')}")
    
    if 'score_breakdown' in question:
        print(f"📊 Scores: {json.dumps(question['score_breakdown'], indent=2)}")
    
    print(f"\n💬 Question: {question.get('text')}")
    
    print("\n" + "="*80 + "\n")


def main():
    """Main demo loop"""
    print("\n" + "🚗" * 40)
    print("INSURANCE CLAIM INTAKE - MANUAL DEMO LOOP")
    print("🚗" * 40 + "\n")
    
    # Initialize
    question_bank_path = "data/question_bank_validated.jsonl"
    if not os.path.exists(question_bank_path):
        print(f"❌ Error: Question bank not found at {question_bank_path}")
        return
    
    retriever = QuestionRetriever(question_bank_path)
    claim_state = initialize_claim_state()
    turn_number = 0
    
    print("📋 Instructions:")
    print("  - You'll be prompted to enter incident descriptions")
    print("  - The system will extract information and ask follow-up questions")
    print("  - Type 'exit' or 'quit' to end the session")
    print("  - Logs will be saved to sample_runs/ folder")
    print()
    
    # Initial input
    print("="*80)
    print("INITIAL INPUT")
    print("="*80)
    initial_input = input("\n📝 Describe the incident: ").strip()
    
    if initial_input.lower() in ['exit', 'quit', '']:
        print("\n👋 Exiting...")
        return
    
    # Extract from initial input
    print("\n🔍 Extracting information...")
    extracted_fields = extract_and_merge(initial_input, claim_state)
    
    # Add extracted fields to already_extracted_categories
    for field in extracted_fields:
        if field not in claim_state['already_extracted_categories']:
            claim_state['already_extracted_categories'].append(field)
    
    print(f"\n✅ Extracted {len(extracted_fields)} fields:")
    for field in extracted_fields:
        print(f"   • {field}")
    
    # Main interview loop
    while True:
        # Display current state
        display_state(claim_state)
        
        # Get next question
        next_question = retriever.get_next_question(claim_state)
        
        # Check termination with available questions
        available_questions = [next_question] if next_question else []
        should_stop, reason, status_info = should_terminate(claim_state, available_questions)
        if should_stop:
            print("\n" + "="*80)
            print("✅ INTERVIEW COMPLETE")
            print("="*80)
            print(f"\nReason: {reason}")
            print(f"Total Turns: {turn_number}")
            print(f"Questions Answered: {len(claim_state.get('answered_question_ids', []))}")
            
            # Save final summary
            final_summary = {
                "completion_reason": reason,
                "total_turns": turn_number,
                "total_questions": len(claim_state.get('answered_question_ids', [])),
                "final_claim_state": claim_state
            }
            with open("sample_runs/final_summary.json", 'w') as f:
                json.dump(final_summary, f, indent=2)
            print("\n✅ Final summary saved to: sample_runs/final_summary.json")
            break
        
        if not next_question:
            print("\n⚠️ No more questions available. Interview complete.")
            break
        
        # Display question
        turn_number += 1
        display_question(next_question, turn_number)
        
        # Get user answer
        user_answer = input("💬 Your answer (or 'exit' to quit): ").strip()
        
        if user_answer.lower() in ['exit', 'quit']:
            print("\n👋 Session terminated by user")
            break
        
        if not user_answer:
            print("⚠️ No answer provided, skipping...")
            continue
        
        # Save turn log BEFORE extraction
        save_turn_log(turn_number, claim_state, next_question, user_answer)
        
        # Extract and update state with question context
        print("\n🔍 Extracting information from your answer...")
        extracted_fields = extract_and_merge(user_answer, claim_state, next_question)
        
        # Mark question as answered
        if next_question.get('id') not in claim_state['answered_question_ids']:
            claim_state['answered_question_ids'].append(next_question['id'])
        
        # Add target fields to already_extracted_categories
        question_field = next_question.get('question_field')
        if question_field and question_field not in claim_state['already_extracted_categories']:
            claim_state['already_extracted_categories'].append(question_field)
        
        # Show what was extracted
        if extracted_fields:
            print(f"\n✅ Extracted {len(extracted_fields)} new fields:")
            for field in extracted_fields:
                print(f"   • {field}")
        else:
            print("\n⚠️ No new information extracted")
        
        print("\n" + "-"*80)
        input("\nPress Enter to continue...")
        print("\n\n")
    
    print("\n" + "🚗" * 40)
    print("SESSION COMPLETE")
    print("🚗" * 40 + "\n")


if __name__ == "__main__":
    main()
