"""
Termination Policy - Determines when to stop asking questions
"""

from typing import Dict, Any, Tuple, List


class TerminationPolicy:
    """Decides when the interview should terminate"""
    
    def __init__(self):
        # Mandatory fields that must be collected
        self.mandatory_fields = [
            "category",
            "loss_datetime",
            "loss_location"
        ]
        
        # Maximum number of questions to ask
        self.max_questions = 15
        
        # Priority thresholds
        self.must_ask_priorities = [1, 2]  # Must ask all priority 1 and 2 questions
    
    def should_terminate(self, claim_state: Dict[str, Any], 
                        available_questions: list,
                        history: list = None) -> Tuple[bool, str]:
        """
        Determine if interview should terminate
        
        Returns: (should_stop, reason)
        """
        
        # Reason 1: All mandatory fields collected
        if self._all_mandatory_fields_present(claim_state):
            
            # Check if any high priority questions remain
            high_priority_remain = any(q.get("priority", 5) in self.must_ask_priorities 
                                      for q in available_questions)
            
            if not high_priority_remain:
                return True, "All mandatory fields collected and no high-priority questions remain"
        
        # Reason 2: Maximum question limit reached
        answered_count = len(claim_state.get("answered_question_ids", []))
        if answered_count >= self.max_questions:
            return True, f"Maximum question limit reached ({self.max_questions} questions)"
        
        # Reason 3: No more applicable questions
        if not available_questions or len(available_questions) == 0:
            return True, "No more applicable questions based on current state"
        
        # Reason 4: Only low-priority questions remain (and we have basic info)
        if self._has_sufficient_info(claim_state) and self._only_low_priority_remain(available_questions):
            return True, "Sufficient information collected, only low-priority questions remain"
        
        # Continue asking questions
        return False, "Continue gathering information"
    
    def _all_mandatory_fields_present(self, claim_state: Dict[str, Any]) -> bool:
        """Check if all mandatory fields are present and not None"""
        for field in self.mandatory_fields:
            value = claim_state.get(field)
            if value is None or value == "unknown":
                return False
            
            # For nested fields like loss_location
            if field == "loss_location" and isinstance(value, dict):
                if not value.get("city"):
                    return False
        
        return True
    
    def _has_sufficient_info(self, claim_state: Dict[str, Any]) -> bool:
        """Check if we have sufficient basic information"""
        # At minimum, we need category, datetime, and location
        basic_fields = ["category", "loss_datetime"]
        
        for field in basic_fields:
            if not claim_state.get(field):
                return False
        
        # Check location has at least city
        location = claim_state.get("loss_location", {})
        if not location.get("city"):
            return False
        
        return True
    
    def _only_low_priority_remain(self, available_questions: list) -> bool:
        """Check if only low-priority questions (4-5) remain"""
        if not available_questions:
            return True
        
        for q in available_questions:
            priority = q.get("priority", 5)
            if priority <= 3:  # If any priority 1, 2, or 3 remains
                return False
        
        return True
    
    def get_completion_status(self, claim_state: Dict[str, Any]) -> Dict[str, Any]:
        """Get detailed completion status"""
        status = {
            "mandatory_fields": {},
            "answered_questions": len(claim_state.get("answered_question_ids", [])),
            "max_questions": self.max_questions,
            "completion_percentage": 0
        }
        
        # Check each mandatory field
        completed = 0
        for field in self.mandatory_fields:
            is_present = claim_state.get(field) is not None
            status["mandatory_fields"][field] = is_present
            if is_present:
                completed += 1
        
        status["completion_percentage"] = (completed / len(self.mandatory_fields)) * 100
        
        return status


# Standalone function wrapper for easy imports
_policy_instance = None

def should_terminate(claim_state: Dict[str, Any], available_questions: List[Dict[str, Any]]) -> Tuple[bool, str, Dict[str, Any]]:
    """
    Standalone function wrapper for termination policy
    Returns: (should_stop, reason, status_info)
    """
    global _policy_instance
    if _policy_instance is None:
        _policy_instance = TerminationPolicy()
    
    should_stop, reason = _policy_instance.should_terminate(claim_state, available_questions)
    status_info = _policy_instance.get_completion_status(claim_state)
    
    return should_stop, reason, status_info


def main():
    """Test termination policy"""
    policy = TerminationPolicy()
    
    # Test 1: Incomplete state
    test_state_1 = {
        "category": "collision",
        "answered_question_ids": ["Q0001", "Q0002"]
    }
    
    available_q = [{"priority": 1}, {"priority": 2}, {"priority": 3}]
    
    print("=== Test 1: Incomplete State ===")
    should_stop, reason = policy.should_terminate(test_state_1, available_q)
    print(f"Should Stop: {should_stop}")
    print(f"Reason: {reason}")
    print(f"Status: {policy.get_completion_status(test_state_1)}")
    
    # Test 2: Complete state with high priority questions
    test_state_2 = {
        "category": "collision",
        "loss_datetime": "March 2, 2026",
        "loss_location": {"city": "Pune", "road_type": "urban"},
        "answered_question_ids": ["Q0001", "Q0002", "Q0003", "Q0004"]
    }
    
    print("\n=== Test 2: Complete State with High Priority ===")
    should_stop, reason = policy.should_terminate(test_state_2, available_q)
    print(f"Should Stop: {should_stop}")
    print(f"Reason: {reason}")
    
    # Test 3: Complete state with only low priority questions
    low_priority_q = [{"priority": 4}, {"priority": 5}]
    
    print("\n=== Test 3: Complete State with Low Priority Only ===")
    should_stop, reason = policy.should_terminate(test_state_2, low_priority_q)
    print(f"Should Stop: {should_stop}")
    print(f"Reason: {reason}")
    
    # Test 4: Max questions reached
    test_state_3 = {
        "category": "collision",
        "loss_datetime": "March 2, 2026",
        "loss_location": {"city": "Pune"},
        "answered_question_ids": [f"Q{i:04d}" for i in range(16)]
    }
    
    print("\n=== Test 4: Max Questions Reached ===")
    should_stop, reason = policy.should_terminate(test_state_3, available_q)
    print(f"Should Stop: {should_stop}")
    print(f"Reason: {reason}")


if __name__ == "__main__":
    main()
