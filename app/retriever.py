"""
Retrieval Engine for Dynamic Question Selection
Uses hard filtering + ranking to select next best question
"""

import json
from typing import List, Dict, Any, Optional
from collections import defaultdict


class QuestionRetriever:
    """Retrieves and ranks questions based on claim state"""
    
    def __init__(self, question_bank_path: str):
        self.questions = self._load_questions(question_bank_path)
        print(f"Loaded {len(self.questions)} questions into retriever")
        
        # Weights for scoring
        self.priority_weight = 1.0
        self.relevance_weight = 0.8
        self.gap_fill_weight = 0.9
        self.fraud_weight = 0.7
    
    def _load_questions(self, filepath: str) -> List[Dict[str, Any]]:
        """Load validated question bank"""
        questions = []
        try:
            with open(filepath, 'r') as f:
                for line in f:
                    if line.strip():
                        questions.append(json.loads(line))
        except FileNotFoundError:
            print(f"Warning: Question bank not found at {filepath}")
        return questions
    
    def get_next_question(self, claim_state: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Get the next best question based on current claim state"""
        
        # Stage 1: Hard filter
        candidates = self._hard_filter(claim_state)
        
        if not candidates:
            return None
        
        # Stage 2: Rank candidates
        ranked = self._rank_questions(candidates, claim_state)
        
        if not ranked:
            return None
        
        # Return top ranked question
        return ranked[0]
    
    def _hard_filter(self, claim_state: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Apply hard filters to question bank"""
        candidates = []
        
        answered_ids = set(claim_state.get("answered_question_ids", []))
        
        for question in self.questions:
            # Filter 1: Already asked
            if question["id"] in answered_ids:
                continue
            
            # Filter 2: Triggers match claim state
            if not self._triggers_match(question["triggers"], claim_state):
                continue
            
            # Filter 3: Target fields not already filled
            if self._targets_already_filled(question["targets"], claim_state):
                continue
            
            candidates.append(question)
        
        return candidates
    
    def _triggers_match(self, triggers: Dict[str, Any], claim_state: Dict[str, Any]) -> bool:
        """Check if question triggers match current claim state"""
        
        # If no triggers, question is always applicable
        if not triggers:
            return True
        
        for trigger_key, trigger_value in triggers.items():
            
            # Special handling for incident_type
            if trigger_key == "incident_type":
                category = claim_state.get("category")
                
                # If trigger is list with None, means category not set yet
                if isinstance(trigger_value, list) and None in trigger_value:
                    if category is None or category == "unknown":
                        return True
                    continue
                
                # Check if category matches any in list
                if isinstance(trigger_value, list):
                    if category not in trigger_value:
                        return False
                elif trigger_value != category:
                    return False
            
            # Special handling for required_fields_present
            elif trigger_key == "required_fields_present":
                if isinstance(trigger_value, list):
                    for required_field in trigger_value:
                        if not self._field_is_present(required_field, claim_state):
                            return False
            
            # Handle boolean triggers
            elif trigger_key in claim_state:
                state_value = claim_state[trigger_key]
                
                # If trigger expects None, only match if state is None
                if trigger_value is None:
                    if state_value is not None:
                        return False
                # Otherwise check equality
                elif state_value != trigger_value:
                    return False
        
        return True
    
    def _field_is_present(self, field_path: str, claim_state: Dict[str, Any]) -> bool:
        """Check if a field (possibly nested) is present and non-null"""
        parts = field_path.split(".")
        current = claim_state
        
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return False
        
        # Field is present if not None
        return current is not None
    
    def _targets_already_filled(self, targets: Dict[str, Any], claim_state: Dict[str, Any]) -> bool:
        """Check if all target fields are already filled"""
        fill_fields = targets.get("fill_fields", [])
        
        if not fill_fields:
            return False
        
        # If ANY target field is not filled, we should ask this question
        for field in fill_fields:
            if not self._field_is_present(field, claim_state):
                return False
        
        # All target fields are filled
        return True
    
    def _rank_questions(self, candidates: List[Dict[str, Any]], 
                       claim_state: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Rank candidate questions by score"""
        
        scored = []
        
        for question in candidates:
            score, breakdown = self._calculate_score(question, claim_state)
            
            scored.append({
                **question,
                "score": score,
                "score_breakdown": breakdown
            })
        
        # Sort by score (descending)
        scored.sort(key=lambda x: x["score"], reverse=True)
        
        return scored
    
    def _calculate_score(self, question: Dict[str, Any], 
                        claim_state: Dict[str, Any]) -> tuple:
        """Calculate relevance score for a question"""
        
        # Priority score (higher priority = higher score)
        priority = question["priority"]
        priority_score = (6 - priority) / 5.0 * self.priority_weight
        
        # Gap fill score (does this fill missing fields?)
        gap_score = self._gap_fill_score(question, claim_state) * self.gap_fill_weight
        
        # Category relevance
        relevance_score = self._relevance_score(question, claim_state) * self.relevance_weight
        
        # Fraud detection bonus
        fraud_score = self._fraud_score(question) * self.fraud_weight
        
        total_score = priority_score + gap_score + relevance_score + fraud_score
        
        breakdown = {
            "priority": round(priority_score, 3),
            "gap_fill": round(gap_score, 3),
            "relevance": round(relevance_score, 3),
            "fraud": round(fraud_score, 3)
        }
        
        return total_score, breakdown
    
    def _gap_fill_score(self, question: Dict[str, Any], claim_state: Dict[str, Any]) -> float:
        """Score based on filling missing fields"""
        fill_fields = question["targets"].get("fill_fields", [])
        
        if not fill_fields:
            return 0.0
        
        missing_count = 0
        for field in fill_fields:
            if not self._field_is_present(field, claim_state):
                missing_count += 1
        
        # Higher score if fills more missing fields
        return missing_count / len(fill_fields)
    
    def _relevance_score(self, question: Dict[str, Any], claim_state: Dict[str, Any]) -> float:
        """Score based on category/context relevance"""
        triggers = question.get("triggers", {})
        
        # Check if category matches
        if "incident_type" in triggers:
            incident_types = triggers["incident_type"]
            category = claim_state.get("category")
            
            if isinstance(incident_types, list):
                if category in incident_types:
                    return 1.0
                elif None not in incident_types:
                    return 0.5
            elif incident_types == category:
                return 1.0
        
        return 0.7  # Default relevance
    
    def _fraud_score(self, question: Dict[str, Any]) -> float:
        """Bonus for fraud detection questions"""
        text = question["text"].lower()
        field = question["question_field"].lower()
        
        fraud_keywords = ["fraud", "suspicious", "verify", "confirm", "prior", "previous"]
        
        for keyword in fraud_keywords:
            if keyword in text or keyword in field:
                return 0.5
        
        return 0.0
    
    def get_statistics(self, claim_state: Dict[str, Any]) -> Dict[str, Any]:
        """Get statistics about available questions"""
        candidates = self._hard_filter(claim_state)
        
        stats = {
            "total_questions": len(self.questions),
            "available_questions": len(candidates),
            "answered_questions": len(claim_state.get("answered_question_ids", [])),
            "priority_breakdown": defaultdict(int)
        }
        
        for q in candidates:
            stats["priority_breakdown"][q["priority"]] += 1
        
        stats["priority_breakdown"] = dict(stats["priority_breakdown"])
        
        return stats


def main():
    """Test retrieval engine"""
    retriever = QuestionRetriever('data/question_bank_validated.jsonl')
    
    # Test with empty claim state
    claim_state = {
        "category": None,
        "answered_question_ids": [],
        "already_extracted_categories": []
    }
    
    print("\n=== Test 1: Empty Claim State ===")
    next_q = retriever.get_next_question(claim_state)
    if next_q:
        print(f"Question: {next_q['text']}")
        print(f"Priority: {next_q['priority']}")
        print(f"Score: {next_q.get('score', 'N/A')}")
        print(f"Score Breakdown: {next_q.get('score_breakdown', {})}")
    
    # Test with collision category
    claim_state["category"] = "collision"
    claim_state["answered_question_ids"] = [next_q["id"]] if next_q else []
    
    print("\n=== Test 2: Collision Category Set ===")
    next_q = retriever.get_next_question(claim_state)
    if next_q:
        print(f"Question: {next_q['text']}")
        print(f"Priority: {next_q['priority']}")
        print(f"Score: {next_q.get('score', 'N/A')}")
    
    # Statistics
    print("\n=== Statistics ===")
    stats = retriever.get_statistics(claim_state)
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
