"""
State Fusion Module - Extracts information from user text responses
Updates claim state based on extracted entities and facts
"""

import re
import json
from typing import Dict, Any, List, Tuple
from datetime import datetime
import dateparser


class StateFusion:
    """Extracts and merges information from user responses into claim state"""
    
    def __init__(self):
        # Incident type keywords
        self.incident_keywords = {
            "collision": ["accident", "crash", "hit", "collision", "collided", "rear-ended", "side-swiped", "bumped"],
            "theft": ["stolen", "theft", "missing", "taken", "stole", "robbed"],
            "fire": ["fire", "burned", "burning", "flames", "smoke", "caught fire", "engulfed"],
            "flood": ["flood", "flooded", "water", "submerged", "underwater", "waterlogged"],
            "vandalism": ["vandalized", "keyed", "scratched", "graffiti", "smashed", "broken into", "damaged"]
        }
        
        # Damage areas
        self.damage_keywords = {
            "front": ["front", "hood", "bonnet", "bumper front"],
            "rear": ["rear", "back", "trunk", "boot", "rear bumper"],
            "left_side": ["left", "driver side", "left door"],
            "right_side": ["right", "passenger side", "right door"],
            "roof": ["roof", "top"],
            "windshield": ["windshield", "windscreen", "glass"],
            "interior": ["interior", "inside", "seats", "dashboard"]
        }
        
        # Road types
        self.road_type_keywords = {
            "highway": ["highway", "expressway", "freeway", "motorway"],
            "urban": ["city", "urban", "street", "avenue", "road", "intersection"],
            "rural": ["rural", "village", "countryside", "farm road"]
        }
        
    def extract_and_merge(self, user_input: str, current_state: Dict[str, Any], 
                         current_question: Dict[str, Any] = None) -> Tuple[Dict[str, Any], List[str]]:
        """
        Extract information from user input and merge into current state
        Returns: (updated_state, extracted_categories)
        """
        user_input_lower = user_input.lower()
        updated_state = current_state.copy()
        extracted_categories = []
        
        # Extract incident type/category
        if not updated_state.get("category") or updated_state.get("category") == "unknown":
            category = self._extract_incident_type(user_input_lower)
            if category:
                updated_state["category"] = category
                extracted_categories.append("category")
        
        # Extract date/time
        datetime_extracted = self._extract_datetime(user_input)
        if datetime_extracted:
            updated_state["loss_datetime"] = datetime_extracted
            extracted_categories.append("loss_datetime")
        
        # Extract location
        location_info = self._extract_location(user_input)
        if location_info:
            if "loss_location" not in updated_state:
                updated_state["loss_location"] = {}
            updated_state["loss_location"].update(location_info)
            extracted_categories.append("loss_location")
        
        # Extract third party involvement
        third_party = self._extract_third_party(user_input_lower)
        if third_party is not None:
            updated_state["third_party_involved"] = third_party
            if third_party:
                extracted_categories.append("third_party_involved")
        
        # Extract drivability
        drivable = self._extract_drivable(user_input_lower)
        if drivable is not None:
            updated_state["drivable"] = drivable
            extracted_categories.append("drivable")
        
        # Extract damage areas
        damage_areas = self._extract_damage_areas(user_input_lower)
        if damage_areas:
            if "damage_areas" not in updated_state:
                updated_state["damage_areas"] = []
            updated_state["damage_areas"].extend(damage_areas)
            updated_state["damage_areas"] = list(set(updated_state["damage_areas"]))  # Remove duplicates
            extracted_categories.append("damage_areas")
        
        # Extract police report status
        police_report = self._extract_police_report(user_input_lower)
        if police_report is not None:
            updated_state["police_report_filed"] = police_report
            extracted_categories.append("police_report_filed")
        
        # Extract injuries
        injuries = self._extract_injuries(user_input_lower)
        if injuries is not None:
            updated_state["injuries_reported"] = injuries
            extracted_categories.append("injuries_reported")
        
        # Extract vehicle registration (if asking about third party)
        vehicle_id = self._extract_vehicle_registration(user_input)
        if vehicle_id:
            updated_state["third_party_vehicle_id"] = vehicle_id
            extracted_categories.append("third_party_details_registration")
        
        # If answering a specific question, extract the target field
        if current_question:
            question_field = current_question.get("question_field", "")
            extracted = self._extract_specific_field(user_input, question_field, user_input_lower)
            if extracted is not None:
                # Map question_field to state field
                field_name = self._map_question_field_to_state(question_field)
                updated_state[field_name] = extracted
                extracted_categories.append(question_field)
        
        # Update already_extracted_categories
        if "already_extracted_categories" not in updated_state:
            updated_state["already_extracted_categories"] = []
        
        for cat in extracted_categories:
            if cat not in updated_state["already_extracted_categories"]:
                updated_state["already_extracted_categories"].append(cat)
        
        return updated_state, extracted_categories
    
    def _extract_incident_type(self, text: str) -> str:
        """Extract incident type from text"""
        for incident_type, keywords in self.incident_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    return incident_type
        return None
    
    def _extract_datetime(self, text: str) -> str:
        """Extract date/time from text"""
        # Use dateparser to extract dates
        try:
            parsed_date = dateparser.parse(text, settings={'PREFER_DATES_FROM': 'past'})
            if parsed_date:
                return parsed_date.strftime("%B %d, %Y")
        except:
            pass
        
        # Simple pattern matching
        date_patterns = [
            r'(today|yesterday|last\s+\w+)',
            r'(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})',
            r'(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\w*\s+\d{1,2}',
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(0)
        
        return None
    
    def _extract_location(self, text: str) -> Dict[str, str]:
        """Extract location information"""
        location = {}
        
        # Extract city names (simple capitalized words that could be cities)
        # Common Indian cities
        cities = ["mumbai", "delhi", "bangalore", "pune", "hyderabad", "chennai", 
                 "kolkata", "ahmedabad", "surat", "jaipur", "lucknow", "kanpur"]
        
        text_lower = text.lower()
        for city in cities:
            if city in text_lower:
                location["city"] = city.capitalize()
                break
        
        # Extract road type
        for road_type, keywords in self.road_type_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    location["road_type"] = road_type
                    break
        
        return location
    
    def _extract_third_party(self, text: str) -> bool:
        """Extract third party involvement"""
        third_party_positive = ["other vehicle", "another car", "bike", "motorcycle", "truck", 
                               "bus", "hit by", "other driver", "their vehicle"]
        third_party_negative = ["single vehicle", "only my car", "no other vehicle", 
                               "wall", "pole", "tree", "by myself", "no one else"]
        
        for keyword in third_party_positive:
            if keyword in text:
                return True
        
        for keyword in third_party_negative:
            if keyword in text:
                return False
        
        return None
    
    def _extract_drivable(self, text: str) -> bool:
        """Extract vehicle drivability"""
        drivable_positive = ["drivable", "can drive", "drove home", "drove it", "still runs"]
        drivable_negative = ["not drivable", "can't drive", "towed", "won't start", 
                           "cannot drive", "immobile", "undrivable"]
        
        for keyword in drivable_positive:
            if keyword in text:
                return True
        
        for keyword in drivable_negative:
            if keyword in text:
                return False
        
        return None
    
    def _extract_damage_areas(self, text: str) -> List[str]:
        """Extract damaged areas"""
        areas = []
        for area, keywords in self.damage_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    areas.append(area)
                    break
        return areas
    
    def _extract_police_report(self, text: str) -> bool:
        """Extract police report filing status"""
        police_positive = ["filed report", "police report", "called police", "fir", 
                          "reported to police", "police came"]
        police_negative = ["no police", "didn't call police", "no report", "handled privately",
                          "without police", "without reporting"]
        
        for keyword in police_positive:
            if keyword in text:
                return True
        
        for keyword in police_negative:
            if keyword in text:
                return False
        
        return None
    
    def _extract_injuries(self, text: str) -> bool:
        """Extract injury information"""
        injury_keywords = ["injured", "hurt", "hospital", "ambulance", "medical", "bleeding"]
        no_injury_keywords = ["no injuries", "uninjured", "no one hurt", "everyone ok"]
        
        for keyword in injury_keywords:
            if keyword in text:
                return True
        
        for keyword in no_injury_keywords:
            if keyword in text:
                return False
        
        return None
    
    def _extract_vehicle_registration(self, text: str) -> str:
        """Extract vehicle registration number"""
        # Indian vehicle registration pattern: AA00AA0000
        pattern = r'\b[A-Z]{2}[ -]?\d{1,2}[ -]?[A-Z]{1,2}[ -]?\d{1,4}\b'
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(0).upper()
        return None
    
    def _extract_specific_field(self, text: str, question_field: str, text_lower: str) -> Any:
        """Extract specific field based on question type"""
        
        # Boolean questions - yes/no detection
        yes_patterns = ["yes", "yeah", "yup", "correct", "right", "true", "affirmative", "indeed"]
        no_patterns = ["no", "nope", "nah", "negative", "incorrect", "false", "not"]
        
        for pattern in yes_patterns:
            if pattern in text_lower.split():
                return True
        
        for pattern in no_patterns:
            if pattern in text_lower.split():
                return False
        
        # For text fields, return the input
        if len(text.strip()) > 3:
            return text.strip()
        
        return None
    
    def _map_question_field_to_state(self, question_field: str) -> str:
        """Map question_field to actual state field name"""
        # Simple mapping - in production, this would be more sophisticated
        mapping = {
            "third_party_details_registration": "third_party_vehicle_id",
            "legal_reporting_status": "police_report_filed",
            "damage_area_multi_select": "damage_areas",
            "fire_department_called": "fire_department_called",
            "water_level": "water_level",
            "vandalism_type": "vandalism_type"
        }
        return mapping.get(question_field, question_field)


# Standalone function wrapper for easy imports
_fusion_instance = None

def extract_and_merge(user_input: str, current_state: Dict[str, Any], 
                     current_question: Dict[str, Any] = None) -> List[str]:
    """
    Standalone function wrapper for state fusion
    Updates current_state in place and returns list of extracted categories
    """
    global _fusion_instance
    if _fusion_instance is None:
        _fusion_instance = StateFusion()
    
    updated_state, extracted = _fusion_instance.extract_and_merge(
        user_input, current_state, current_question
    )
    
    # Update the current_state dict in place with the extracted values
    current_state.update(updated_state)
    
    return extracted


def main():
    """Test state fusion"""
    fusion = StateFusion()
    
    # Test 1: Extract from initial claim
    test_input = "My car had an accident and got hit from the side from a bike"
    initial_state = {
        "category": None,
        "answered_question_ids": [],
        "already_extracted_categories": []
    }
    
    print("=== Test 1: Initial Claim ===")
    print(f"Input: {test_input}")
    updated_state, extracted = fusion.extract_and_merge(test_input, initial_state)
    print(f"Updated State: {json.dumps(updated_state, indent=2)}")
    print(f"Extracted: {extracted}")
    
    # Test 2: Extract registration and date
    test_input2 = "Yeah it was MH12AB1234, the accident happened today on Mar 2, 2026"
    print("\n=== Test 2: Registration and Date ===")
    print(f"Input: {test_input2}")
    updated_state2, extracted2 = fusion.extract_and_merge(test_input2, updated_state)
    print(f"Updated State: {json.dumps(updated_state2, indent=2)}")
    print(f"Extracted: {extracted2}")
    
    # Test 3: No police report
    test_input3 = "minor collision, exchanged details. We did not call police"
    print("\n=== Test 3: Police Report ===")
    print(f"Input: {test_input3}")
    updated_state3, extracted3 = fusion.extract_and_merge(test_input3, updated_state2)
    print(f"Updated State: {json.dumps(updated_state3, indent=2)}")
    print(f"Extracted: {extracted3}")


if __name__ == "__main__":
    main()
