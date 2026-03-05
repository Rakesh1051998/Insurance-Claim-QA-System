"""
Validator Pipeline for Question Bank
- Schema validation
- Logical validation
- Duplicate removal using semantic similarity
- Coverage checks
"""

import json
import jsonschema
from typing import List, Dict, Any, Tuple
from collections import defaultdict
import numpy as np


class QuestionValidator:
    """Validates question bank for quality and consistency"""
    
    def __init__(self):
        self.valid_questions = []
        self.rejected_questions = []
        self.rejection_reasons = defaultdict(int)
        
        # Question schema
        self.question_schema = {
            "type": "object",
            "required": ["id", "text", "question_field", "priority", "triggers", "targets"],
            "properties": {
                "id": {"type": "string"},
                "text": {"type": "string", "minLength": 5},
                "question_field": {"type": "string", "minLength": 1},
                "priority": {"type": "integer", "minimum": 1, "maximum": 5},
                "triggers": {"type": "object"},
                "targets": {
                    "type": "object",
                    "required": ["fill_fields"],
                    "properties": {
                        "fill_fields": {
                            "type": "array",
                            "minItems": 1
                        }
                    }
                }
            }
        }
    
    def validate_all(self, questions: List[Dict[str, Any]]) -> Tuple[List[Dict], List[Dict]]:
        """Run full validation pipeline"""
        print("Starting validation pipeline...")
        
        # Step 1: Schema validation
        schema_valid = self._schema_validation(questions)
        print(f"  Schema validation: {len(schema_valid)}/{len(questions)} passed")
        
        # Step 2: Logical validation
        logically_valid = self._logical_validation(schema_valid)
        print(f"  Logical validation: {len(logically_valid)}/{len(schema_valid)} passed")
        
        # Step 3: Duplicate removal
        unique_questions = self._remove_duplicates(logically_valid)
        print(f"  Duplicate removal: {len(unique_questions)}/{len(logically_valid)} unique")
        
        # Step 4: Coverage check
        coverage_report = self._coverage_check(unique_questions)
        print(f"  Coverage check: {coverage_report}")
        
        self.valid_questions = unique_questions
        return self.valid_questions, self.rejected_questions
    
    def _schema_validation(self, questions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Validate questions against schema"""
        valid = []
        
        for q in questions:
            try:
                # Validate against schema
                jsonschema.validate(instance=q, schema=self.question_schema)
                
                # Additional checks
                if not q["text"].strip():
                    self._reject(q, "Empty question text")
                    continue
                
                if not q["targets"].get("fill_fields"):
                    self._reject(q, "No target fields specified")
                    continue
                
                if not isinstance(q["triggers"], dict):
                    self._reject(q, "Invalid triggers format")
                    continue
                
                valid.append(q)
                
            except jsonschema.exceptions.ValidationError as e:
                self._reject(q, f"Schema validation failed: {e.message}")
            except Exception as e:
                self._reject(q, f"Unexpected error: {str(e)}")
        
        return valid
    
    def _logical_validation(self, questions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Validate logical consistency of questions"""
        valid = []
        
        for q in questions:
            # Check 1: Target shouldn't be in triggers
            target_fields = set(q["targets"]["fill_fields"])
            trigger_keys = set(q["triggers"].keys())
            
            # Simple check - if target field name appears in trigger keys
            if target_fields.intersection(trigger_keys):
                self._reject(q, "Target field appears in triggers")
                continue
            
            # Check 2: Must have at least one trigger or required_fields_present
            if not q["triggers"] or (len(q["triggers"]) == 0):
                self._reject(q, "No triggers defined")
                continue
            
            # Check 3: Priority must be reasonable
            if q["priority"] < 1 or q["priority"] > 5:
                self._reject(q, f"Invalid priority: {q['priority']}")
                continue
            
            # Check 4: Question text shouldn't be too short
            if len(q["text"]) < 10:
                self._reject(q, "Question text too short")
                continue
            
            # Check 5: Targets must not be empty
            if not q["targets"]["fill_fields"]:
                self._reject(q, "Empty fill_fields in targets")
                continue
            
            valid.append(q)
        
        return valid
    
    def _remove_duplicates(self, questions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate questions using semantic similarity"""
        
        # Simple approach: use text similarity
        # For production, use sentence-transformers
        
        unique = []
        seen_texts = set()
        
        for q in questions:
            # Normalize text for comparison
            normalized = q["text"].lower().strip()
            
            # Simple duplicate check based on exact text match
            if normalized in seen_texts:
                self._reject(q, "Duplicate question text")
                continue
            
            # Check for very similar questions (simple heuristic)
            is_duplicate = False
            for existing in unique:
                existing_text = existing["text"].lower().strip()
                
                # Calculate simple similarity
                similarity = self._simple_similarity(normalized, existing_text)
                
                if similarity > 0.92:
                    self._reject(q, f"Too similar to {existing['id']}")
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                unique.append(q)
                seen_texts.add(normalized)
        
        return unique
    
    def _simple_similarity(self, text1: str, text2: str) -> float:
        """Calculate simple text similarity (word overlap)"""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def _coverage_check(self, questions: List[Dict[str, Any]]) -> Dict[str, int]:
        """Check coverage across categories"""
        coverage = defaultdict(int)
        
        for q in questions:
            # Count by priority
            coverage[f"priority_{q['priority']}"] += 1
            
            # Count by incident type in triggers
            if "incident_type" in q["triggers"]:
                incident_types = q["triggers"]["incident_type"]
                if isinstance(incident_types, list):
                    for itype in incident_types:
                        if itype:
                            coverage[f"type_{itype}"] += 1
            
            # Count fraud questions
            if "fraud" in q["question_field"].lower() or "fraud" in q["text"].lower():
                coverage["fraud_questions"] += 1
        
        return dict(coverage)
    
    def _reject(self, question: Dict[str, Any], reason: str):
        """Record rejected question"""
        rejection = {
            "question": question,
            "reason": reason
        }
        self.rejected_questions.append(rejection)
        self.rejection_reasons[reason] += 1
    
    def save_results(self, valid_path: str, rejected_path: str):
        """Save validation results"""
        # Save valid questions
        with open(valid_path, 'w') as f:
            for q in self.valid_questions:
                f.write(json.dumps(q) + '\n')
        
        # Save rejected questions
        with open(rejected_path, 'w') as f:
            for r in self.rejected_questions:
                f.write(json.dumps(r) + '\n')
        
        print(f"\nValidation complete:")
        print(f"  Valid: {len(self.valid_questions)}")
        print(f"  Rejected: {len(self.rejected_questions)}")
        print(f"\nRejection reasons:")
        for reason, count in sorted(self.rejection_reasons.items(), key=lambda x: x[1], reverse=True):
            print(f"  {reason}: {count}")


def load_questions(filepath: str) -> List[Dict[str, Any]]:
    """Load questions from JSONL file"""
    questions = []
    with open(filepath, 'r') as f:
        for line in f:
            if line.strip():
                questions.append(json.loads(line))
    return questions


def main():
    """Run validation pipeline"""
    print("Loading questions...")
    questions = load_questions('data/question_bank_raw.jsonl')
    print(f"Loaded {len(questions)} questions")
    
    validator = QuestionValidator()
    valid, rejected = validator.validate_all(questions)
    
    validator.save_results(
        'data/question_bank_validated.jsonl',
        'data/rejected_questions.jsonl'
    )


if __name__ == "__main__":
    main()
