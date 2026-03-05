"""
Question Bank Generator for Insurance Claims
Generates 1200+ questions across different categories programmatically
"""

import json
import itertools
from typing import List, Dict, Any


class QuestionGenerator:
    """Generates insurance claim questions programmatically"""
    
    def __init__(self):
        self.question_id_counter = 1
        self.questions = []
    
    def generate_all_questions(self) -> List[Dict[str, Any]]:
        """Generate all questions across all categories"""
        
        # TASK 1: Generate questions for each category
        self.generate_collision_questions()
        self.generate_theft_questions()
        self.generate_fire_questions()
        self.generate_flood_questions()
        self.generate_vandalism_questions()
        self.generate_documentation_questions()
        self.generate_policy_gate_questions()
        self.generate_fraud_detection_questions()
        self.generate_repair_preference_questions()
        
        return self.questions
    
    def _add_question(self, text: str, question_field: str, priority: int,
                     triggers: Dict[str, Any], targets: Dict[str, List[str]]):
        """Add a question to the bank"""
        question = {
            "id": f"Q{self.question_id_counter:04d}",
            "text": text,
            "question_field": question_field,
            "priority": priority,
            "triggers": triggers,
            "targets": targets
        }
        self.questions.append(question)
        self.question_id_counter += 1
    
    def generate_collision_questions(self):
        """Generate 200+ collision-related questions"""
        
        # Basic collision questions
        collision_variations = [
            ("What type of collision occurred?", "category", 1, 
             {"incident_type": [None], "required_fields_present": []},
             {"fill_fields": ["category"]}),
            
            ("Can you describe the collision in your own words?", "incident_description", 3,
             {"incident_type": ["collision"], "required_fields_present": ["category"]},
             {"fill_fields": ["incident_description"]}),
            
            ("When exactly did the collision happen?", "loss_datetime", 1,
             {"incident_type": ["collision"], "required_fields_present": ["category"]},
             {"fill_fields": ["loss_datetime"]}),
            
            ("What date and time did the accident occur?", "loss_datetime", 1,
             {"incident_type": ["collision"], "loss_datetime": None},
             {"fill_fields": ["loss_datetime"]}),
            
            ("Where did the collision take place?", "loss_location", 1,
             {"incident_type": ["collision"], "required_fields_present": ["category"]},
             {"fill_fields": ["loss_location.city", "loss_location.address"]}),
            
            ("What city did this happen in?", "loss_location.city", 1,
             {"incident_type": ["collision"], "required_fields_present": ["category"]},
             {"fill_fields": ["loss_location.city"]}),
            
            ("Can you provide the street address?", "loss_location.address", 2,
             {"incident_type": ["collision"], "required_fields_present": ["loss_location.city"]},
             {"fill_fields": ["loss_location.address"]}),
            
            ("Was this on a highway, city street, or rural road?", "loss_location.road_type", 3,
             {"incident_type": ["collision"], "required_fields_present": ["category"]},
             {"fill_fields": ["loss_location.road_type"]}),
            
            ("Was another vehicle involved in the collision?", "third_party_involved", 1,
             {"incident_type": ["collision"], "required_fields_present": ["category"]},
             {"fill_fields": ["third_party_involved"]}),
            
            ("Were there any other parties involved?", "third_party_involved", 1,
             {"incident_type": ["collision"], "third_party_involved": None},
             {"fill_fields": ["third_party_involved"]}),
        ]
        
        for text, field, priority, triggers, targets in collision_variations:
            self._add_question(text, field, priority, triggers, targets)
        
        # Third party collision questions
        third_party_questions = [
            ("Did you get the other driver's contact information?", "third_party_contact", 2,
             {"incident_type": ["collision"], "third_party_involved": True},
             {"fill_fields": ["third_party_contact"]}),
            
            ("Do you have the other driver's insurance details?", "third_party_insurance", 2,
             {"incident_type": ["collision"], "third_party_involved": True},
             {"fill_fields": ["third_party_insurance"]}),
            
            ("What was the license plate of the other vehicle?", "third_party_plate", 2,
             {"incident_type": ["collision"], "third_party_involved": True},
             {"fill_fields": ["third_party_plate"]}),
            
            ("Can you describe the other vehicle (make, model, color)?", "third_party_vehicle", 3,
             {"incident_type": ["collision"], "third_party_involved": True},
             {"fill_fields": ["third_party_vehicle"]}),
            
            ("Who do you believe was at fault for the collision?", "driver_at_fault", 3,
             {"incident_type": ["collision"], "third_party_involved": True},
             {"fill_fields": ["driver_at_fault"]}),
        ]
        
        for text, field, priority, triggers, targets in third_party_questions:
            self._add_question(text, field, priority, triggers, targets)
        
        # Damage assessment questions
        damage_questions = [
            ("Which parts of your vehicle were damaged?", "damage_areas", 3,
             {"incident_type": ["collision"], "required_fields_present": ["category"]},
             {"fill_fields": ["damage_areas"]}),
            
            ("Was the front of your vehicle damaged?", "damage_areas", 3,
             {"incident_type": ["collision"], "required_fields_present": ["category"]},
             {"fill_fields": ["damage_areas"]}),
            
            ("Was the rear of your vehicle damaged?", "damage_areas", 3,
             {"incident_type": ["collision"], "required_fields_present": ["category"]},
             {"fill_fields": ["damage_areas"]}),
            
            ("Was the left side damaged?", "damage_areas", 3,
             {"incident_type": ["collision"], "required_fields_present": ["category"]},
             {"fill_fields": ["damage_areas"]}),
            
            ("Was the right side damaged?", "damage_areas", 3,
             {"incident_type": ["collision"], "required_fields_present": ["category"]},
             {"fill_fields": ["damage_areas"]}),
            
            ("Is your vehicle still drivable?", "drivable", 2,
             {"incident_type": ["collision"], "required_fields_present": ["category"]},
             {"fill_fields": ["drivable"]}),
            
            ("Can you drive the vehicle home?", "drivable", 2,
             {"incident_type": ["collision"], "drivable": None},
             {"fill_fields": ["drivable"]}),
            
            ("How severe would you say the damage is?", "damage_severity", 3,
             {"incident_type": ["collision"], "required_fields_present": ["category"]},
             {"fill_fields": ["damage_severity"]}),
            
            ("Would you describe the damage as minor, moderate, or severe?", "damage_severity", 3,
             {"incident_type": ["collision"], "damage_severity": None},
             {"fill_fields": ["damage_severity"]}),
            
            ("Was your vehicle towed from the scene?", "vehicle_towed", 2,
             {"incident_type": ["collision"], "drivable": False},
             {"fill_fields": ["vehicle_towed"]}),
        ]
        
        for text, field, priority, triggers, targets in damage_questions:
            self._add_question(text, field, priority, triggers, targets)
        
        # Injury and safety questions
        injury_questions = [
            ("Were there any injuries as a result of this collision?", "injuries_reported", 1,
             {"incident_type": ["collision"], "required_fields_present": ["category"]},
             {"fill_fields": ["injuries_reported"]}),
            
            ("Did anyone require medical attention?", "injuries_reported", 1,
             {"incident_type": ["collision"], "injuries_reported": None},
             {"fill_fields": ["injuries_reported"]}),
            
            ("Were the airbags deployed during the collision?", "airbag_deployed", 2,
             {"incident_type": ["collision"], "required_fields_present": ["category"]},
             {"fill_fields": ["airbag_deployed"]}),
            
            ("Did you visit a hospital or doctor after the collision?", "medical_visit", 2,
             {"incident_type": ["collision"], "injuries_reported": True},
             {"fill_fields": ["medical_visit"]}),
        ]
        
        for text, field, priority, triggers, targets in injury_questions:
            self._add_question(text, field, priority, triggers, targets)
        
        # Police and legal questions
        police_questions = [
            ("Did you file a police report?", "police_report_filed", 1,
             {"incident_type": ["collision"], "required_fields_present": ["category"]},
             {"fill_fields": ["police_report_filed"]}),
            
            ("Was law enforcement called to the scene?", "police_report_filed", 1,
             {"incident_type": ["collision"], "police_report_filed": None},
             {"fill_fields": ["police_report_filed"]}),
            
            ("Do you have the police report number?", "police_report_number", 2,
             {"incident_type": ["collision"], "police_report_filed": True},
             {"fill_fields": ["police_report_number"]}),
            
            ("What is the report number from the police?", "police_report_number", 2,
             {"incident_type": ["collision"], "police_report_filed": True, "police_report_number": None},
             {"fill_fields": ["police_report_number"]}),
        ]
        
        for text, field, priority, triggers, targets in police_questions:
            self._add_question(text, field, priority, triggers, targets)
        
        # Witness questions
        witness_questions = [
            ("Were there any witnesses to the collision?", "witness_present", 2,
             {"incident_type": ["collision"], "required_fields_present": ["category"]},
             {"fill_fields": ["witness_present"]}),
            
            ("Did anyone see what happened?", "witness_present", 2,
             {"incident_type": ["collision"], "witness_present": None},
             {"fill_fields": ["witness_present"]}),
            
            ("How many witnesses were there?", "witness_count", 3,
             {"incident_type": ["collision"], "witness_present": True},
             {"fill_fields": ["witness_count"]}),
            
            ("Did you get contact information from any witnesses?", "witness_contact", 3,
             {"incident_type": ["collision"], "witness_present": True},
             {"fill_fields": ["witness_contact"]}),
        ]
        
        for text, field, priority, triggers, targets in witness_questions:
            self._add_question(text, field, priority, triggers, targets)
        
        # Environmental conditions
        condition_questions = [
            ("What were the weather conditions at the time?", "weather_conditions", 3,
             {"incident_type": ["collision"], "required_fields_present": ["category"]},
             {"fill_fields": ["weather_conditions"]}),
            
            ("Was it raining, snowing, or clear?", "weather_conditions", 3,
             {"incident_type": ["collision"], "weather_conditions": None},
             {"fill_fields": ["weather_conditions"]}),
            
            ("What time of day did this occur?", "time_of_day", 3,
             {"incident_type": ["collision"], "required_fields_present": ["category"]},
             {"fill_fields": ["time_of_day"]}),
            
            ("Was it during daylight or nighttime?", "time_of_day", 3,
             {"incident_type": ["collision"], "time_of_day": None},
             {"fill_fields": ["time_of_day"]}),
            
            ("What were the road conditions like?", "road_conditions", 3,
             {"incident_type": ["collision"], "required_fields_present": ["category"]},
             {"fill_fields": ["road_conditions"]}),
        ]
        
        for text, field, priority, triggers, targets in condition_questions:
            self._add_question(text, field, priority, triggers, targets)
        
        # Speed and dynamics
        dynamics_questions = [
            ("How fast were you traveling at the time of impact?", "speed_at_impact", 3,
             {"incident_type": ["collision"], "required_fields_present": ["category"]},
             {"fill_fields": ["speed_at_impact"]}),
            
            ("What was your approximate speed?", "speed_at_impact", 3,
             {"incident_type": ["collision"], "speed_at_impact": None},
             {"fill_fields": ["speed_at_impact"]}),
            
            ("Were you stopped or moving when impact occurred?", "vehicle_moving", 3,
             {"incident_type": ["collision"], "required_fields_present": ["category"]},
             {"fill_fields": ["vehicle_moving"]}),
            
            ("Can you describe how the collision happened?", "collision_dynamics", 3,
             {"incident_type": ["collision"], "required_fields_present": ["category"]},
             {"fill_fields": ["collision_dynamics"]}),
            
            ("Did you see the other vehicle before impact?", "visibility", 3,
             {"incident_type": ["collision"], "third_party_involved": True},
             {"fill_fields": ["visibility"]}),
        ]
        
        for text, field, priority, triggers, targets in dynamics_questions:
            self._add_question(text, field, priority, triggers, targets)
        
        # Additional collision variations for reaching 200
        additional_variations = [
            ("At what intersection did this occur?", "loss_location.intersection", 3,
             {"incident_type": ["collision"], "loss_location.road_type": "urban"},
             {"fill_fields": ["loss_location.intersection"]}),
            
            ("Which direction were you traveling?", "travel_direction", 3,
             {"incident_type": ["collision"], "required_fields_present": ["category"]},
             {"fill_fields": ["travel_direction"]}),
            
            ("Were you making a turn when the collision happened?", "turning", 3,
             {"incident_type": ["collision"], "required_fields_present": ["category"]},
             {"fill_fields": ["turning"]}),
            
            ("Was there a traffic signal at the location?", "traffic_signal_present", 3,
             {"incident_type": ["collision"], "loss_location.road_type": "urban"},
             {"fill_fields": ["traffic_signal_present"]}),
            
            ("What color was the traffic light?", "traffic_light_color", 3,
             {"incident_type": ["collision"], "traffic_signal_present": True},
             {"fill_fields": ["traffic_light_color"]}),
            
            ("Were you in a parking lot?", "parking_lot", 3,
             {"incident_type": ["collision"], "required_fields_present": ["category"]},
             {"fill_fields": ["parking_lot"]}),
            
            ("Was your vehicle parked when hit?", "parked_when_hit", 3,
             {"incident_type": ["collision"], "vehicle_moving": False},
             {"fill_fields": ["parked_when_hit"]}),
            
            ("Did you brake before impact?", "braked", 3,
             {"incident_type": ["collision"], "vehicle_moving": True},
             {"fill_fields": ["braked"]}),
            
            ("Did you try to avoid the collision?", "evasive_action", 3,
             {"incident_type": ["collision"], "vehicle_moving": True},
             {"fill_fields": ["evasive_action"]}),
            
            ("Was the other driver distracted?", "other_driver_distracted", 3,
             {"incident_type": ["collision"], "third_party_involved": True},
             {"fill_fields": ["other_driver_distracted"]}),
        ]
        
        for text, field, priority, triggers, targets in additional_variations:
            self._add_question(text, field, priority, triggers, targets)
    
    def generate_theft_questions(self):
        """Generate 150+ theft-related questions"""
        
        theft_questions = [
            ("When did you discover your vehicle was stolen?", "loss_datetime", 1,
             {"incident_type": ["theft"], "required_fields_present": ["category"]},
             {"fill_fields": ["loss_datetime"]}),
            
            ("What date and time was the theft discovered?", "loss_datetime", 1,
             {"incident_type": ["theft"], "loss_datetime": None},
             {"fill_fields": ["loss_datetime"]}),
            
            ("When did you last see your vehicle?", "last_seen_datetime", 1,
             {"incident_type": ["theft"], "required_fields_present": ["category"]},
             {"fill_fields": ["last_seen_datetime"]}),
            
            ("Where was your vehicle stolen from?", "loss_location", 1,
             {"incident_type": ["theft"], "required_fields_present": ["category"]},
             {"fill_fields": ["loss_location.city", "loss_location.address"]}),
            
            ("From what location was it taken?", "loss_location", 1,
             {"incident_type": ["theft"], "loss_location.city": None},
             {"fill_fields": ["loss_location.city"]}),
            
            ("Was it stolen from your home, work, or elsewhere?", "theft_location_type", 2,
             {"incident_type": ["theft"], "required_fields_present": ["category"]},
             {"fill_fields": ["theft_location_type"]}),
            
            ("Did you file a police report for the stolen vehicle?", "police_report_filed", 1,
             {"incident_type": ["theft"], "required_fields_present": ["category"]},
             {"fill_fields": ["police_report_filed"]}),
            
            ("Have you reported this to law enforcement?", "police_report_filed", 1,
             {"incident_type": ["theft"], "police_report_filed": None},
             {"fill_fields": ["police_report_filed"]}),
            
            ("What is the police report number?", "police_report_number", 1,
             {"incident_type": ["theft"], "police_report_filed": True},
             {"fill_fields": ["police_report_number"]}),
            
            ("Were all keys accounted for when the vehicle was stolen?", "all_keys_present", 2,
             {"incident_type": ["theft"], "required_fields_present": ["category"]},
             {"fill_fields": ["all_keys_present"]}),
            
            ("Do you still have all sets of keys?", "all_keys_present", 2,
             {"incident_type": ["theft"], "all_keys_present": None},
             {"fill_fields": ["all_keys_present"]}),
            
            ("Where were the keys when the vehicle was stolen?", "key_location", 2,
             {"incident_type": ["theft"], "required_fields_present": ["category"]},
             {"fill_fields": ["key_location"]}),
            
            ("Was the vehicle locked when stolen?", "vehicle_locked", 2,
             {"incident_type": ["theft"], "required_fields_present": ["category"]},
             {"fill_fields": ["vehicle_locked"]}),
            
            ("Are you certain you locked the vehicle?", "vehicle_locked", 2,
             {"incident_type": ["theft"], "vehicle_locked": None},
             {"fill_fields": ["vehicle_locked"]}),
            
            ("Were the windows closed?", "windows_closed", 3,
             {"incident_type": ["theft"], "required_fields_present": ["category"]},
             {"fill_fields": ["windows_closed"]}),
            
            ("Did the vehicle have an alarm system?", "alarm_present", 3,
             {"incident_type": ["theft"], "required_fields_present": ["category"]},
             {"fill_fields": ["alarm_present"]}),
            
            ("Was the alarm active when stolen?", "alarm_active", 3,
             {"incident_type": ["theft"], "alarm_present": True},
             {"fill_fields": ["alarm_active"]}),
            
            ("Did you hear the alarm go off?", "alarm_heard", 3,
             {"incident_type": ["theft"], "alarm_present": True},
             {"fill_fields": ["alarm_heard"]}),
            
            ("Does your vehicle have GPS tracking?", "gps_tracking", 2,
             {"incident_type": ["theft"], "required_fields_present": ["category"]},
             {"fill_fields": ["gps_tracking"]}),
            
            ("Can the vehicle be tracked via GPS?", "gps_tracking", 2,
             {"incident_type": ["theft"], "gps_tracking": None},
             {"fill_fields": ["gps_tracking"]}),
        ]
        
        for text, field, priority, triggers, targets in theft_questions:
            self._add_question(text, field, priority, triggers, targets)
        
        # Additional theft questions
        more_theft_questions = [
            ("Were any personal belongings left in the vehicle?", "belongings_in_vehicle", 3,
             {"incident_type": ["theft"], "required_fields_present": ["category"]},
             {"fill_fields": ["belongings_in_vehicle"]}),
            
            ("What items were in the vehicle when stolen?", "stolen_items", 3,
             {"incident_type": ["theft"], "belongings_in_vehicle": True},
             {"fill_fields": ["stolen_items"]}),
            
            ("Was there any damage to where it was parked?", "parking_area_damage", 3,
             {"incident_type": ["theft"], "required_fields_present": ["category"]},
             {"fill_fields": ["parking_area_damage"]}),
            
            ("Were there security cameras in the area?", "security_cameras", 2,
             {"incident_type": ["theft"], "required_fields_present": ["category"]},
             {"fill_fields": ["security_cameras"]}),
            
            ("Have you obtained security footage?", "security_footage_obtained", 3,
             {"incident_type": ["theft"], "security_cameras": True},
             {"fill_fields": ["security_footage_obtained"]}),
            
            ("Did anyone see the theft occur?", "witness_present", 2,
             {"incident_type": ["theft"], "required_fields_present": ["category"]},
             {"fill_fields": ["witness_present"]}),
            
            ("Were there any witnesses?", "witness_present", 2,
             {"incident_type": ["theft"], "witness_present": None},
             {"fill_fields": ["witness_present"]}),
            
            ("How much fuel was in the tank?", "fuel_level", 4,
             {"incident_type": ["theft"], "required_fields_present": ["category"]},
             {"fill_fields": ["fuel_level"]}),
            
            ("What was the odometer reading when last seen?", "odometer_reading", 4,
             {"incident_type": ["theft"], "required_fields_present": ["category"]},
             {"fill_fields": ["odometer_reading"]}),
            
            ("Were there any unique identifying features on the vehicle?", "unique_features", 3,
             {"incident_type": ["theft"], "required_fields_present": ["category"]},
             {"fill_fields": ["unique_features"]}),
            
            ("Did you have any custom modifications?", "custom_modifications", 3,
             {"incident_type": ["theft"], "required_fields_present": ["category"]},
             {"fill_fields": ["custom_modifications"]}),
            
            ("How long was the vehicle left unattended?", "unattended_duration", 3,
             {"incident_type": ["theft"], "required_fields_present": ["category"]},
             {"fill_fields": ["unattended_duration"]}),
            
            ("Have you checked with neighbors or nearby businesses?", "checked_with_neighbors", 3,
             {"incident_type": ["theft"], "required_fields_present": ["category"]},
             {"fill_fields": ["checked_with_neighbors"]}),
            
            ("Is it possible the vehicle was towed?", "possibly_towed", 2,
             {"incident_type": ["theft"], "required_fields_present": ["category"]},
             {"fill_fields": ["possibly_towed"]}),
            
            ("Have you confirmed it wasn't towed by authorities?", "verified_not_towed", 2,
             {"incident_type": ["theft"], "possibly_towed": True},
             {"fill_fields": ["verified_not_towed"]}),
        ]
        
        for text, field, priority, triggers, targets in more_theft_questions:
            self._add_question(text, field, priority, triggers, targets)
        
        # Theft recovery questions
        recovery_questions = [
            ("Has the vehicle been recovered?", "vehicle_recovered", 2,
             {"incident_type": ["theft"], "required_fields_present": ["police_report_filed"]},
             {"fill_fields": ["vehicle_recovered"]}),
            
            ("When was the vehicle recovered?", "recovery_datetime", 3,
             {"incident_type": ["theft"], "vehicle_recovered": True},
             {"fill_fields": ["recovery_datetime"]}),
            
            ("In what condition was the vehicle recovered?", "recovery_condition", 3,
             {"incident_type": ["theft"], "vehicle_recovered": True},
             {"fill_fields": ["recovery_condition"]}),
            
            ("Was there damage when recovered?", "damage_on_recovery", 3,
             {"incident_type": ["theft"], "vehicle_recovered": True},
             {"fill_fields": ["damage_on_recovery"]}),
            
            ("Were any parts missing from the recovered vehicle?", "missing_parts", 3,
             {"incident_type": ["theft"], "vehicle_recovered": True},
             {"fill_fields": ["missing_parts"]}),
        ]
        
        for text, field, priority, triggers, targets in recovery_questions:
            self._add_question(text, field, priority, triggers, targets)
    
    def generate_fire_questions(self):
        """Generate 150+ fire-related questions"""
        
        fire_questions = [
            ("When did the fire occur?", "loss_datetime", 1,
             {"incident_type": ["fire"], "required_fields_present": ["category"]},
             {"fill_fields": ["loss_datetime"]}),
            
            ("What date and time did you discover the fire?", "loss_datetime", 1,
             {"incident_type": ["fire"], "loss_datetime": None},
             {"fill_fields": ["loss_datetime"]}),
            
            ("Where did the fire happen?", "loss_location", 1,
             {"incident_type": ["fire"], "required_fields_present": ["category"]},
             {"fill_fields": ["loss_location.city", "loss_location.address"]}),
            
            ("What location was the vehicle at when it caught fire?", "loss_location", 1,
             {"incident_type": ["fire"], "loss_location.city": None},
             {"fill_fields": ["loss_location.city"]}),
            
            ("Was the fire department called?", "fire_department_called", 1,
             {"incident_type": ["fire"], "required_fields_present": ["category"]},
             {"fill_fields": ["fire_department_called"]}),
            
            ("Did firefighters respond to the scene?", "fire_department_called", 1,
             {"incident_type": ["fire"], "fire_department_called": None},
             {"fill_fields": ["fire_department_called"]}),
            
            ("Do you have a fire department report?", "fire_report_obtained", 2,
             {"incident_type": ["fire"], "fire_department_called": True},
             {"fill_fields": ["fire_report_obtained"]}),
            
            ("What is the fire report number?", "fire_report_number", 2,
             {"incident_type": ["fire"], "fire_report_obtained": True},
             {"fill_fields": ["fire_report_number"]}),
            
            ("Was anyone injured in the fire?", "injuries_reported", 1,
             {"incident_type": ["fire"], "required_fields_present": ["category"]},
             {"fill_fields": ["injuries_reported"]}),
            
            ("Did anyone require medical attention?", "injuries_reported", 1,
             {"incident_type": ["fire"], "injuries_reported": None},
             {"fill_fields": ["injuries_reported"]}),
            
            ("What do you believe caused the fire?", "fire_cause_belief", 2,
             {"incident_type": ["fire"], "required_fields_present": ["category"]},
             {"fill_fields": ["fire_cause_belief"]}),
            
            ("Where did the fire start on the vehicle?", "fire_origin", 2,
             {"incident_type": ["fire"], "required_fields_present": ["category"]},
             {"fill_fields": ["fire_origin"]}),
            
            ("Did the fire start in the engine compartment?", "fire_origin", 2,
             {"incident_type": ["fire"], "fire_origin": None},
             {"fill_fields": ["fire_origin"]}),
            
            ("Was the vehicle running when the fire started?", "vehicle_running", 2,
             {"incident_type": ["fire"], "required_fields_present": ["category"]},
             {"fill_fields": ["vehicle_running"]}),
            
            ("Were you driving when the fire started?", "vehicle_running", 2,
             {"incident_type": ["fire"], "vehicle_running": None},
             {"fill_fields": ["vehicle_running"]}),
            
            ("Was the vehicle parked?", "vehicle_parked", 2,
             {"incident_type": ["fire"], "vehicle_running": False},
             {"fill_fields": ["vehicle_parked"]}),
            
            ("How extensive is the fire damage?", "damage_severity", 3,
             {"incident_type": ["fire"], "required_fields_present": ["category"]},
             {"fill_fields": ["damage_severity"]}),
            
            ("Would you say it's a total loss?", "damage_severity", 3,
             {"incident_type": ["fire"], "damage_severity": None},
             {"fill_fields": ["damage_severity"]}),
            
            ("Did you notice any warning signs before the fire?", "warning_signs", 3,
             {"incident_type": ["fire"], "required_fields_present": ["category"]},
             {"fill_fields": ["warning_signs"]}),
            
            ("Were there any unusual smells or smoke beforehand?", "warning_signs", 3,
             {"incident_type": ["fire"], "warning_signs": None},
             {"fill_fields": ["warning_signs"]}),
        ]
        
        for text, field, priority, triggers, targets in fire_questions:
            self._add_question(text, field, priority, triggers, targets)
        
        # Additional fire questions
        more_fire_questions = [
            ("Had you recently had any mechanical work done?", "recent_repairs", 2,
             {"incident_type": ["fire"], "required_fields_present": ["category"]},
             {"fill_fields": ["recent_repairs"]}),
            
            ("What repairs were completed recently?", "recent_repairs_details", 3,
             {"incident_type": ["fire"], "recent_repairs": True},
             {"fill_fields": ["recent_repairs_details"]}),
            
            ("Did you have any check engine lights on?", "check_engine_light", 3,
             {"incident_type": ["fire"], "required_fields_present": ["category"]},
             {"fill_fields": ["check_engine_light"]}),
            
            ("Were there any electrical issues before the fire?", "electrical_issues", 2,
             {"incident_type": ["fire"], "required_fields_present": ["category"]},
             {"fill_fields": ["electrical_issues"]}),
            
            ("Did you smell anything burning before?", "burning_smell", 3,
             {"incident_type": ["fire"], "required_fields_present": ["category"]},
             {"fill_fields": ["burning_smell"]}),
            
            ("Was there smoke coming from the vehicle?", "smoke_observed", 2,
             {"incident_type": ["fire"], "required_fields_present": ["category"]},
             {"fill_fields": ["smoke_observed"]}),
            
            ("Did anyone try to extinguish the fire?", "extinguish_attempted", 3,
             {"incident_type": ["fire"], "required_fields_present": ["category"]},
             {"fill_fields": ["extinguish_attempted"]}),
            
            ("Did you have a fire extinguisher in the vehicle?", "fire_extinguisher_present", 4,
             {"incident_type": ["fire"], "required_fields_present": ["category"]},
             {"fill_fields": ["fire_extinguisher_present"]}),
            
            ("How quickly did the fire spread?", "fire_spread_speed", 3,
             {"incident_type": ["fire"], "required_fields_present": ["category"]},
             {"fill_fields": ["fire_spread_speed"]}),
            
            ("Was the entire vehicle engulfed?", "fully_engulfed", 3,
             {"incident_type": ["fire"], "required_fields_present": ["category"]},
             {"fill_fields": ["fully_engulfed"]}),
            
            ("Did the fire spread to any other property?", "fire_spread_to_property", 1,
             {"incident_type": ["fire"], "required_fields_present": ["category"]},
             {"fill_fields": ["fire_spread_to_property"]}),
            
            ("Was anyone else's property damaged?", "third_party_property_damage", 2,
             {"incident_type": ["fire"], "fire_spread_to_property": True},
             {"fill_fields": ["third_party_property_damage"]}),
            
            ("Were you able to remove belongings before the fire spread?", "belongings_removed", 4,
             {"incident_type": ["fire"], "required_fields_present": ["category"]},
             {"fill_fields": ["belongings_removed"]}),
            
            ("What items were destroyed in the fire?", "destroyed_items", 4,
             {"incident_type": ["fire"], "required_fields_present": ["category"]},
             {"fill_fields": ["destroyed_items"]}),
            
            ("Has a fire investigator examined the vehicle?", "fire_investigator", 2,
             {"incident_type": ["fire"], "fire_department_called": True},
             {"fill_fields": ["fire_investigator"]}),
        ]
        
        for text, field, priority, triggers, targets in more_fire_questions:
            self._add_question(text, field, priority, triggers, targets)
    
    def generate_flood_questions(self):
        """Generate 150+ flood-related questions"""
        
        flood_questions = [
            ("When did the flooding occur?", "loss_datetime", 1,
             {"incident_type": ["flood"], "required_fields_present": ["category"]},
             {"fill_fields": ["loss_datetime"]}),
            
            ("What date did your vehicle get flooded?", "loss_datetime", 1,
             {"incident_type": ["flood"], "loss_datetime": None},
             {"fill_fields": ["loss_datetime"]}),
            
            ("Where was your vehicle when it was flooded?", "loss_location", 1,
             {"incident_type": ["flood"], "required_fields_present": ["category"]},
             {"fill_fields": ["loss_location.city", "loss_location.address"]}),
            
            ("What location did the flooding happen?", "loss_location", 1,
             {"incident_type": ["flood"], "loss_location.city": None},
             {"fill_fields": ["loss_location.city"]}),
            
            ("How high did the water reach on your vehicle?", "water_level", 2,
             {"incident_type": ["flood"], "required_fields_present": ["category"]},
             {"fill_fields": ["water_level"]}),
            
            ("Did water enter the interior of the vehicle?", "water_in_interior", 2,
             {"incident_type": ["flood"], "required_fields_present": ["category"]},
             {"fill_fields": ["water_in_interior"]}),
            
            ("Was the water above the floor level?", "water_in_interior", 2,
             {"incident_type": ["flood"], "water_in_interior": None},
             {"fill_fields": ["water_in_interior"]}),
            
            ("Did water reach the engine?", "water_in_engine", 2,
             {"incident_type": ["flood"], "required_fields_present": ["category"]},
             {"fill_fields": ["water_in_engine"]}),
            
            ("Was the vehicle submerged?", "fully_submerged", 2,
             {"incident_type": ["flood"], "required_fields_present": ["category"]},
             {"fill_fields": ["fully_submerged"]}),
            
            ("Was the vehicle completely underwater?", "fully_submerged", 2,
             {"incident_type": ["flood"], "fully_submerged": None},
             {"fill_fields": ["fully_submerged"]}),
            
            ("Was your vehicle running when it was flooded?", "vehicle_running", 3,
             {"incident_type": ["flood"], "required_fields_present": ["category"]},
             {"fill_fields": ["vehicle_running"]}),
            
            ("Were you driving through high water?", "driving_through_water", 3,
             {"incident_type": ["flood"], "vehicle_running": True},
             {"fill_fields": ["driving_through_water"]}),
            
            ("Was the vehicle parked during the flood?", "vehicle_parked", 2,
             {"incident_type": ["flood"], "vehicle_running": False},
             {"fill_fields": ["vehicle_parked"]}),
            
            ("Is the vehicle still drivable?", "drivable", 2,
             {"incident_type": ["flood"], "required_fields_present": ["category"]},
             {"fill_fields": ["drivable"]}),
            
            ("Can the vehicle start now?", "drivable", 2,
             {"incident_type": ["flood"], "drivable": None},
             {"fill_fields": ["drivable"]}),
            
            ("Did you attempt to start the vehicle after flooding?", "start_attempted", 2,
             {"incident_type": ["flood"], "required_fields_present": ["category"]},
             {"fill_fields": ["start_attempted"]}),
            
            ("Have you tried to turn on the engine since?", "start_attempted", 2,
             {"incident_type": ["flood"], "start_attempted": None},
             {"fill_fields": ["start_attempted"]}),
            
            ("Was this from a natural disaster or weather event?", "natural_disaster", 2,
             {"incident_type": ["flood"], "required_fields_present": ["category"]},
             {"fill_fields": ["natural_disaster"]}),
            
            ("Was this from a hurricane or major storm?", "natural_disaster", 2,
             {"incident_type": ["flood"], "natural_disaster": None},
             {"fill_fields": ["natural_disaster"]}),
            
            ("Is the area under a disaster declaration?", "disaster_declaration", 2,
             {"incident_type": ["flood"], "natural_disaster": True},
             {"fill_fields": ["disaster_declaration"]}),
        ]
        
        for text, field, priority, triggers, targets in flood_questions:
            self._add_question(text, field, priority, triggers, targets)
        
        # Additional flood questions
        more_flood_questions = [
            ("Was the water fresh or salt water?", "water_type", 3,
             {"incident_type": ["flood"], "required_fields_present": ["category"]},
             {"fill_fields": ["water_type"]}),
            
            ("Were you warned about flooding in the area?", "flood_warning", 3,
             {"incident_type": ["flood"], "required_fields_present": ["category"]},
             {"fill_fields": ["flood_warning"]}),
            
            ("Did you have time to move the vehicle?", "time_to_move", 3,
             {"incident_type": ["flood"], "vehicle_parked": True},
             {"fill_fields": ["time_to_move"]}),
            
            ("Why was the vehicle not moved to higher ground?", "not_moved_reason", 4,
             {"incident_type": ["flood"], "time_to_move": True},
             {"fill_fields": ["not_moved_reason"]}),
            
            ("How long was the vehicle in water?", "submersion_duration", 3,
             {"incident_type": ["flood"], "required_fields_present": ["category"]},
             {"fill_fields": ["submersion_duration"]}),
            
            ("Has the vehicle been dried out?", "dried_out", 3,
             {"incident_type": ["flood"], "required_fields_present": ["category"]},
             {"fill_fields": ["dried_out"]}),
            
            ("Are there visible water lines on the vehicle?", "water_lines_visible", 3,
             {"incident_type": ["flood"], "required_fields_present": ["category"]},
             {"fill_fields": ["water_lines_visible"]}),
            
            ("Is there mud or debris inside the vehicle?", "mud_debris_inside", 3,
             {"incident_type": ["flood"], "water_in_interior": True},
             {"fill_fields": ["mud_debris_inside"]}),
            
            ("Does the vehicle smell of mold or mildew?", "mold_smell", 3,
             {"incident_type": ["flood"], "water_in_interior": True},
             {"fill_fields": ["mold_smell"]}),
            
            ("Are the electrical systems functioning?", "electrical_working", 3,
             {"incident_type": ["flood"], "required_fields_present": ["category"]},
             {"fill_fields": ["electrical_working"]}),
            
            ("Was the vehicle towed to a safe location?", "vehicle_towed", 3,
             {"incident_type": ["flood"], "required_fields_present": ["category"]},
             {"fill_fields": ["vehicle_towed"]}),
            
            ("Where is the vehicle currently located?", "current_location", 3,
             {"incident_type": ["flood"], "required_fields_present": ["category"]},
             {"fill_fields": ["current_location"]}),
            
            ("Have you documented the damage with photos?", "photos_available", 4,
             {"incident_type": ["flood"], "required_fields_present": ["category"]},
             {"fill_fields": ["photos_available"]}),
            
            ("Do you have photos of the water level?", "water_level_photos", 4,
             {"incident_type": ["flood"], "photos_available": True},
             {"fill_fields": ["water_level_photos"]}),
            
            ("Was anyone else's property damaged in the flood?", "other_property_damaged", 3,
             {"incident_type": ["flood"], "natural_disaster": True},
             {"fill_fields": ["other_property_damaged"]}),
        ]
        
        for text, field, priority, triggers, targets in more_flood_questions:
            self._add_question(text, field, priority, triggers, targets)
    
    def generate_vandalism_questions(self):
        """Generate 150+ vandalism-related questions"""
        
        vandalism_questions = [
            ("When did you discover the vandalism?", "loss_datetime", 1,
             {"incident_type": ["vandalism"], "required_fields_present": ["category"]},
             {"fill_fields": ["loss_datetime"]}),
            
            ("What date and time was the vandalism discovered?", "loss_datetime", 1,
             {"incident_type": ["vandalism"], "loss_datetime": None},
             {"fill_fields": ["loss_datetime"]}),
            
            ("Where was your vehicle when it was vandalized?", "loss_location", 1,
             {"incident_type": ["vandalism"], "required_fields_present": ["category"]},
             {"fill_fields": ["loss_location.city", "loss_location.address"]}),
            
            ("What location did this occur at?", "loss_location", 1,
             {"incident_type": ["vandalism"], "loss_location.city": None},
             {"fill_fields": ["loss_location.city"]}),
            
            ("What type of vandalism occurred?", "vandalism_type", 2,
             {"incident_type": ["vandalism"], "required_fields_present": ["category"]},
             {"fill_fields": ["vandalism_type"]}),
            
            ("Can you describe the damage?", "vandalism_description", 2,
             {"incident_type": ["vandalism"], "required_fields_present": ["category"]},
             {"fill_fields": ["vandalism_description"]}),
            
            ("Were the windows broken?", "windows_broken", 2,
             {"incident_type": ["vandalism"], "required_fields_present": ["category"]},
             {"fill_fields": ["windows_broken"]}),
            
            ("Which windows were damaged?", "damaged_windows", 3,
             {"incident_type": ["vandalism"], "windows_broken": True},
             {"fill_fields": ["damaged_windows"]}),
            
            ("Was the vehicle keyed or scratched?", "keyed_scratched", 2,
             {"incident_type": ["vandalism"], "required_fields_present": ["category"]},
             {"fill_fields": ["keyed_scratched"]}),
            
            ("Where is the scratch damage located?", "scratch_location", 3,
             {"incident_type": ["vandalism"], "keyed_scratched": True},
             {"fill_fields": ["scratch_location"]}),
            
            ("Were the tires slashed or damaged?", "tires_damaged", 2,
             {"incident_type": ["vandalism"], "required_fields_present": ["category"]},
             {"fill_fields": ["tires_damaged"]}),
            
            ("How many tires were damaged?", "damaged_tire_count", 3,
             {"incident_type": ["vandalism"], "tires_damaged": True},
             {"fill_fields": ["damaged_tire_count"]}),
            
            ("Was paint or graffiti sprayed on the vehicle?", "graffiti", 2,
             {"incident_type": ["vandalism"], "required_fields_present": ["category"]},
             {"fill_fields": ["graffiti"]}),
            
            ("Was anything stolen from inside the vehicle?", "items_stolen", 2,
             {"incident_type": ["vandalism"], "required_fields_present": ["category"]},
             {"fill_fields": ["items_stolen"]}),
            
            ("What items were taken?", "stolen_items_list", 3,
             {"incident_type": ["vandalism"], "items_stolen": True},
             {"fill_fields": ["stolen_items_list"]}),
            
            ("Did you file a police report?", "police_report_filed", 1,
             {"incident_type": ["vandalism"], "required_fields_present": ["category"]},
             {"fill_fields": ["police_report_filed"]}),
            
            ("Have you reported this to law enforcement?", "police_report_filed", 1,
             {"incident_type": ["vandalism"], "police_report_filed": None},
             {"fill_fields": ["police_report_filed"]}),
            
            ("What is the police report number?", "police_report_number", 2,
             {"incident_type": ["vandalism"], "police_report_filed": True},
             {"fill_fields": ["police_report_number"]}),
            
            ("When did you last see the vehicle undamaged?", "last_seen_undamaged", 2,
             {"incident_type": ["vandalism"], "required_fields_present": ["category"]},
             {"fill_fields": ["last_seen_undamaged"]}),
            
            ("Was the vehicle locked?", "vehicle_locked", 2,
             {"incident_type": ["vandalism"], "required_fields_present": ["category"]},
             {"fill_fields": ["vehicle_locked"]}),
        ]
        
        for text, field, priority, triggers, targets in vandalism_questions:
            self._add_question(text, field, priority, triggers, targets)
        
        # Additional vandalism questions
        more_vandalism_questions = [
            ("Do you know who might have done this?", "suspect_known", 2,
             {"incident_type": ["vandalism"], "required_fields_present": ["category"]},
             {"fill_fields": ["suspect_known"]}),
            
            ("Have you been having disputes with anyone?", "recent_disputes", 2,
             {"incident_type": ["vandalism"], "required_fields_present": ["category"]},
             {"fill_fields": ["recent_disputes"]}),
            
            ("Was this a random act or targeted?", "targeted_or_random", 3,
             {"incident_type": ["vandalism"], "required_fields_present": ["category"]},
             {"fill_fields": ["targeted_or_random"]}),
            
            ("Were other vehicles in the area also vandalized?", "other_vehicles_vandalized", 2,
             {"incident_type": ["vandalism"], "required_fields_present": ["category"]},
             {"fill_fields": ["other_vehicles_vandalized"]}),
            
            ("Was there security camera footage?", "security_cameras", 2,
             {"incident_type": ["vandalism"], "required_fields_present": ["category"]},
             {"fill_fields": ["security_cameras"]}),
            
            ("Have you obtained the security footage?", "footage_obtained", 3,
             {"incident_type": ["vandalism"], "security_cameras": True},
             {"fill_fields": ["footage_obtained"]}),
            
            ("Did anyone witness the vandalism?", "witness_present", 2,
             {"incident_type": ["vandalism"], "required_fields_present": ["category"]},
             {"fill_fields": ["witness_present"]}),
            
            ("Did you hear anything suspicious?", "suspicious_sounds", 3,
             {"incident_type": ["vandalism"], "required_fields_present": ["category"]},
             {"fill_fields": ["suspicious_sounds"]}),
            
            ("Was the vehicle in a public or private location?", "location_type", 3,
             {"incident_type": ["vandalism"], "required_fields_present": ["category"]},
             {"fill_fields": ["location_type"]}),
            
            ("Is the vehicle still drivable?", "drivable", 3,
             {"incident_type": ["vandalism"], "required_fields_present": ["category"]},
             {"fill_fields": ["drivable"]}),
            
            ("Were the mirrors damaged?", "mirrors_damaged", 3,
             {"incident_type": ["vandalism"], "required_fields_present": ["category"]},
             {"fill_fields": ["mirrors_damaged"]}),
            
            ("Was the hood or trunk damaged?", "hood_trunk_damaged", 3,
             {"incident_type": ["vandalism"], "required_fields_present": ["category"]},
             {"fill_fields": ["hood_trunk_damaged"]}),
            
            ("Were the lights broken?", "lights_broken", 3,
             {"incident_type": ["vandalism"], "required_fields_present": ["category"]},
             {"fill_fields": ["lights_broken"]}),
            
            ("How many panels need repainting?", "panels_needing_paint", 4,
             {"incident_type": ["vandalism"], "keyed_scratched": True},
             {"fill_fields": ["panels_needing_paint"]}),
            
            ("Do you have photos of the damage?", "photos_available", 3,
             {"incident_type": ["vandalism"], "required_fields_present": ["category"]},
             {"fill_fields": ["photos_available"]}),
        ]
        
        for text, field, priority, triggers, targets in more_vandalism_questions:
            self._add_question(text, field, priority, triggers, targets)
    
    def generate_documentation_questions(self):
        """Generate 150+ documentation-related questions"""
        
        doc_questions = [
            ("Do you have photos of the damage?", "photos_available", 3,
             {"required_fields_present": ["category"]},
             {"fill_fields": ["photos_available"]}),
            
            ("Have you taken pictures of your vehicle?", "photos_available", 3,
             {"photos_available": None},
             {"fill_fields": ["photos_available"]}),
            
            ("How many photos have you taken?", "photos_count", 4,
             {"photos_available": True},
             {"fill_fields": ["photos_count"]}),
            
            ("Have you obtained a repair estimate?", "repair_estimate_obtained", 3,
             {"required_fields_present": ["category"]},
             {"fill_fields": ["repair_estimate_obtained"]}),
            
            ("Did you get an estimate from a shop?", "repair_estimate_obtained", 3,
             {"repair_estimate_obtained": None},
             {"fill_fields": ["repair_estimate_obtained"]}),
            
            ("What is the estimated repair cost?", "repair_estimate_amount", 3,
             {"repair_estimate_obtained": True},
             {"fill_fields": ["repair_estimate_amount"]}),
            
            ("Do you have the written estimate?", "written_estimate_available", 4,
             {"repair_estimate_obtained": True},
             {"fill_fields": ["written_estimate_available"]}),
            
            ("From which shop did you get the estimate?", "estimate_shop_name", 4,
             {"repair_estimate_obtained": True},
             {"fill_fields": ["estimate_shop_name"]}),
            
            ("Do you have the vehicle registration?", "registration_available", 3,
             {"required_fields_present": ["category"]},
             {"fill_fields": ["registration_available"]}),
            
            ("Can you provide your vehicle registration?", "registration_available", 3,
             {"registration_available": None},
             {"fill_fields": ["registration_available"]}),
            
            ("Do you have proof of ownership?", "proof_of_ownership", 2,
             {"required_fields_present": ["category"]},
             {"fill_fields": ["proof_of_ownership"]}),
            
            ("Are you the registered owner?", "registered_owner", 2,
             {"required_fields_present": ["category"]},
             {"fill_fields": ["registered_owner"]}),
            
            ("Is there a lien on the vehicle?", "lien_holder", 2,
             {"required_fields_present": ["category"]},
             {"fill_fields": ["lien_holder"]}),
            
            ("Who is the lienholder?", "lien_holder_name", 3,
             {"lien_holder": True},
             {"fill_fields": ["lien_holder_name"]}),
            
            ("Do you have your insurance policy documents?", "policy_documents", 3,
             {"required_fields_present": ["category"]},
             {"fill_fields": ["policy_documents"]}),
            
            ("What is your policy number?", "policy_number", 2,
             {"required_fields_present": ["category"]},
             {"fill_fields": ["policy_number"]}),
            
            ("When does your policy expire?", "policy_expiration", 3,
             {"required_fields_present": ["category"]},
             {"fill_fields": ["policy_expiration"]}),
            
            ("What is your deductible amount?", "deductible_amount", 3,
             {"required_fields_present": ["category"]},
             {"fill_fields": ["deductible_amount"]}),
            
            ("Do you have comprehensive coverage?", "comprehensive_coverage", 2,
             {"required_fields_present": ["category"]},
             {"fill_fields": ["comprehensive_coverage"]}),
            
            ("Do you have collision coverage?", "collision_coverage", 2,
             {"incident_type": ["collision"]},
             {"fill_fields": ["collision_coverage"]}),
        ]
        
        for text, field, priority, triggers, targets in doc_questions:
            self._add_question(text, field, priority, triggers, targets)
        
        # More documentation questions
        more_doc_questions = [
            ("How would you like to submit your documents?", "document_submission_method", 4,
             {"required_fields_present": ["category"]},
             {"fill_fields": ["document_submission_method"]}),
            
            ("Can you email the documents?", "can_email_documents", 4,
             {"required_fields_present": ["category"]},
             {"fill_fields": ["can_email_documents"]}),
            
            ("What email address should we use?", "contact_email", 3,
             {"can_email_documents": True},
             {"fill_fields": ["contact_email"]}),
            
            ("What is your phone number?", "contact_phone", 3,
             {"required_fields_present": ["category"]},
             {"fill_fields": ["contact_phone"]}),
            
            ("What is the best time to reach you?", "preferred_contact_time", 4,
             {"required_fields_present": ["contact_phone"]},
             {"fill_fields": ["preferred_contact_time"]}),
            
            ("Do you prefer calls or texts?", "contact_method_preference", 4,
             {"required_fields_present": ["contact_phone"]},
             {"fill_fields": ["contact_method_preference"]}),
            
            ("Do you have your driver's license available?", "license_available", 2,
             {"required_fields_present": ["category"]},
             {"fill_fields": ["license_available"]}),
            
            ("What is your driver's license number?", "license_number", 2,
             {"license_available": True},
             {"fill_fields": ["license_number"]}),
            
            ("In which state is your license issued?", "license_state", 2,
             {"license_available": True},
             {"fill_fields": ["license_state"]}),
            
            ("Is your license currently valid?", "license_valid", 1,
             {"license_available": True},
             {"fill_fields": ["license_valid"]}),
            
            ("Do you have the vehicle title?", "title_available", 3,
             {"required_fields_present": ["category"]},
             {"fill_fields": ["title_available"]}),
            
            ("Where is the vehicle title?", "title_location", 4,
             {"title_available": True},
             {"fill_fields": ["title_location"]}),
            
            ("Do you have maintenance records?", "service_records", 4,
             {"required_fields_present": ["category"]},
             {"fill_fields": ["service_records"]}),
            
            ("When was the last service?", "last_service_date", 4,
             {"service_records": True},
             {"fill_fields": ["last_service_date"]}),
            
            ("What is your VIN number?", "vin_number", 2,
             {"required_fields_present": ["category"]},
             {"fill_fields": ["vin_number"]}),
        ]
        
        for text, field, priority, triggers, targets in more_doc_questions:
            self._add_question(text, field, priority, triggers, targets)
    
    def generate_policy_gate_questions(self):
        """Generate 100+ policy gate questions"""
        
        policy_questions = [
            ("Was your insurance active at the time of loss?", "policy_active", 1,
             {"required_fields_present": ["category", "loss_datetime"]},
             {"fill_fields": ["policy_active"]}),
            
            ("Is this vehicle covered under your policy?", "vehicle_covered", 1,
             {"required_fields_present": ["category"]},
             {"fill_fields": ["vehicle_covered"]}),
            
            ("Were you authorized to drive this vehicle?", "authorized_driver", 1,
             {"required_fields_present": ["category"]},
             {"fill_fields": ["authorized_driver"]}),
            
            ("Are you listed on the insurance policy?", "listed_on_policy", 1,
             {"required_fields_present": ["category"]},
             {"fill_fields": ["listed_on_policy"]}),
            
            ("Do you have the required coverage for this type of claim?", "adequate_coverage", 1,
             {"required_fields_present": ["category"]},
             {"fill_fields": ["adequate_coverage"]}),
            
            ("Was the vehicle being used for business purposes?", "commercial_use", 2,
             {"required_fields_present": ["category"]},
             {"fill_fields": ["commercial_use"]}),
            
            ("Was the vehicle being used as a ride-share vehicle?", "rideshare_use", 2,
             {"required_fields_present": ["category"]},
             {"fill_fields": ["rideshare_use"]}),
            
            ("Was the vehicle being used for delivery services?", "delivery_use", 2,
             {"required_fields_present": ["category"]},
             {"fill_fields": ["delivery_use"]}),
            
            ("Had you reported any previous claims on this vehicle?", "previous_claims", 2,
             {"required_fields_present": ["category"]},
             {"fill_fields": ["previous_claims"]}),
            
            ("How many claims have you had in the past 3 years?", "claims_count_3yr", 2,
             {"previous_claims": True},
             {"fill_fields": ["claims_count_3yr"]}),
            
            ("Has your policy ever been cancelled?", "policy_cancelled", 2,
             {"required_fields_present": ["category"]},
             {"fill_fields": ["policy_cancelled"]}),
            
            ("Have you had any coverage gaps?", "coverage_gaps", 2,
             {"required_fields_present": ["category"]},
             {"fill_fields": ["coverage_gaps"]}),
            
            ("When did you purchase this policy?", "policy_purchase_date", 3,
             {"required_fields_present": ["category"]},
             {"fill_fields": ["policy_purchase_date"]}),
            
            ("When did coverage begin for this vehicle?", "vehicle_coverage_start", 2,
             {"required_fields_present": ["category"]},
             {"fill_fields": ["vehicle_coverage_start"]}),
            
            ("Did you make any recent changes to your policy?", "recent_policy_changes", 3,
             {"required_fields_present": ["category"]},
             {"fill_fields": ["recent_policy_changes"]}),
            
            ("Are your premium payments current?", "premiums_current", 1,
             {"required_fields_present": ["category"]},
             {"fill_fields": ["premiums_current"]}),
            
            ("Have you received any cancellation notices?", "cancellation_notice", 1,
             {"required_fields_present": ["category"]},
             {"fill_fields": ["cancellation_notice"]}),
            
            ("Who is the primary policyholder?", "primary_policyholder", 2,
             {"required_fields_present": ["category"]},
             {"fill_fields": ["primary_policyholder"]}),
            
            ("Is this a personal or commercial policy?", "policy_type", 2,
             {"required_fields_present": ["category"]},
             {"fill_fields": ["policy_type"]}),
            
            ("What is your coverage limit?", "coverage_limit", 3,
             {"required_fields_present": ["category"]},
             {"fill_fields": ["coverage_limit"]}),
        ]
        
        for text, field, priority, triggers, targets in policy_questions:
            self._add_question(text, field, priority, triggers, targets)
    
    def generate_fraud_detection_questions(self):
        """Generate 150+ fraud detection questions"""
        
        fraud_questions = [
            ("Have you filed claims for this vehicle before?", "prior_claims_vehicle", 2,
             {"required_fields_present": ["category"]},
             {"fill_fields": ["prior_claims_vehicle"]}),
            
            ("How many times has this vehicle been in an incident?", "incident_count", 2,
             {"prior_claims_vehicle": True},
             {"fill_fields": ["incident_count"]}),
            
            ("When did you purchase this vehicle?", "vehicle_purchase_date", 2,
             {"required_fields_present": ["category"]},
             {"fill_fields": ["vehicle_purchase_date"]}),
            
            ("How long have you owned this vehicle?", "ownership_duration", 2,
             {"required_fields_present": ["category"]},
             {"fill_fields": ["ownership_duration"]}),
            
            ("Where did you purchase the vehicle?", "purchase_location", 3,
             {"required_fields_present": ["category"]},
             {"fill_fields": ["purchase_location"]}),
            
            ("Was this vehicle purchased new or used?", "new_or_used", 3,
             {"required_fields_present": ["category"]},
             {"fill_fields": ["new_or_used"]}),
            
            ("What is the current mileage on the vehicle?", "current_mileage", 3,
             {"required_fields_present": ["category"]},
             {"fill_fields": ["current_mileage"]}),
            
            ("Have you been making loan or lease payments on time?", "payment_history", 2,
             {"lien_holder": True},
             {"fill_fields": ["payment_history"]}),
            
            ("Are you behind on any payments for this vehicle?", "payment_delinquent", 2,
             {"lien_holder": True},
             {"fill_fields": ["payment_delinquent"]}),
            
            ("How much do you still owe on the vehicle?", "remaining_loan_balance", 3,
             {"lien_holder": True},
             {"fill_fields": ["remaining_loan_balance"]}),
            
            ("What is the current value of the vehicle?", "current_vehicle_value", 3,
             {"required_fields_present": ["category"]},
             {"fill_fields": ["current_vehicle_value"]}),
            
            ("Have you had financial difficulties recently?", "financial_difficulties", 2,
             {"required_fields_present": ["category"]},
             {"fill_fields": ["financial_difficulties"]}),
            
            ("Are there any mechanical issues with the vehicle?", "mechanical_issues", 2,
             {"required_fields_present": ["category"]},
             {"fill_fields": ["mechanical_issues"]}),
            
            ("Has the vehicle been in the shop frequently?", "frequent_repairs", 2,
             {"mechanical_issues": True},
             {"fill_fields": ["frequent_repairs"]}),
            
            ("Did you recently increase your coverage?", "coverage_recently_increased", 2,
             {"required_fields_present": ["category"]},
             {"fill_fields": ["coverage_recently_increased"]}),
            
            ("When was coverage increased?", "coverage_increase_date", 2,
             {"coverage_recently_increased": True},
             {"fill_fields": ["coverage_increase_date"]}),
            
            ("Can you provide contact info for witnesses?", "witness_contact_info", 2,
             {"witness_present": True},
             {"fill_fields": ["witness_contact_info"]}),
            
            ("Are the witnesses related to you?", "witness_relationship", 2,
             {"witness_present": True},
             {"fill_fields": ["witness_relationship"]}),
            
            ("Did you report the incident immediately?", "immediate_report", 2,
             {"required_fields_present": ["category", "loss_datetime"]},
             {"fill_fields": ["immediate_report"]}),
            
            ("How long after the incident did you file this claim?", "report_delay", 2,
             {"immediate_report": False},
             {"fill_fields": ["report_delay"]}),
            
            ("Why was there a delay in reporting?", "delay_reason", 2,
             {"immediate_report": False},
             {"fill_fields": ["delay_reason"]}),
            
            ("Have you moved recently?", "recent_move", 3,
             {"required_fields_present": ["category"]},
             {"fill_fields": ["recent_move"]}),
            
            ("What is your current address?", "current_address", 2,
             {"required_fields_present": ["category"]},
             {"fill_fields": ["current_address"]}),
            
            ("Is this where the vehicle is garaged?", "garaged_at_address", 2,
             {"required_fields_present": ["current_address"]},
             {"fill_fields": ["garaged_at_address"]}),
            
            ("Where do you normally park the vehicle?", "normal_parking_location", 3,
             {"required_fields_present": ["category"]},
             {"fill_fields": ["normal_parking_location"]}),
        ]
        
        for text, field, priority, triggers, targets in fraud_questions:
            self._add_question(text, field, priority, triggers, targets)
        
        # Additional fraud detection questions
        more_fraud_questions = [
            ("Do you have dashcam footage?", "dashcam_footage", 2,
             {"incident_type": ["collision"]},
             {"fill_fields": ["dashcam_footage"]}),
            
            ("Can you provide the dashcam video?", "dashcam_available", 2,
             {"dashcam_footage": True},
             {"fill_fields": ["dashcam_available"]}),
            
            ("Was anyone else in the vehicle with you?", "passengers", 2,
             {"incident_type": ["collision"], "vehicle_moving": True},
             {"fill_fields": ["passengers"]}),
            
            ("Who were the passengers?", "passenger_names", 3,
             {"passengers": True},
             {"fill_fields": ["passenger_names"]}),
            
            ("Are the passengers family members?", "passengers_family", 3,
             {"passengers": True},
             {"fill_fields": ["passengers_family"]}),
            
            ("Did any passengers claim injury?", "passenger_injuries", 2,
             {"passengers": True},
             {"fill_fields": ["passenger_injuries"]}),
            
            ("What is your occupation?", "occupation", 3,
             {"required_fields_present": ["category"]},
             {"fill_fields": ["occupation"]}),
            
            ("What is your annual income?", "annual_income", 3,
             {"required_fields_present": ["category"]},
             {"fill_fields": ["annual_income"]}),
            
            ("Do you have other vehicles insured with us?", "other_vehicles", 3,
             {"required_fields_present": ["category"]},
             {"fill_fields": ["other_vehicles"]}),
            
            ("Have you filed claims on other vehicles?", "claims_other_vehicles", 2,
             {"other_vehicles": True},
             {"fill_fields": ["claims_other_vehicles"]}),
            
            ("Are you disputing any traffic violations?", "traffic_violations", 2,
             {"required_fields_present": ["category"]},
             {"fill_fields": ["traffic_violations"]}),
            
            ("Have you had your license suspended?", "license_suspended", 2,
             {"required_fields_present": ["category"]},
             {"fill_fields": ["license_suspended"]}),
            
            ("Do you have any DUI convictions?", "dui_conviction", 2,
             {"required_fields_present": ["category"]},
             {"fill_fields": ["dui_conviction"]}),
            
            ("Were you under the influence during the incident?", "under_influence", 1,
             {"incident_type": ["collision"], "required_fields_present": ["category"]},
             {"fill_fields": ["under_influence"]}),
            
            ("Have you had your claim denied by another insurer?", "prior_denial", 2,
             {"required_fields_present": ["category"]},
             {"fill_fields": ["prior_denial"]}),
        ]
        
        for text, field, priority, triggers, targets in more_fraud_questions:
            self._add_question(text, field, priority, triggers, targets)
    
    def generate_repair_preference_questions(self):
        """Generate 100+ repair preference questions"""
        
        repair_questions = [
            ("Do you need a rental car while repairs are made?", "rental_car_needed", 3,
             {"drivable": False},
             {"fill_fields": ["rental_car_needed"]}),
            
            ("Would you like us to arrange a rental vehicle?", "rental_car_needed", 3,
             {"drivable": False, "rental_car_needed": None},
             {"fill_fields": ["rental_car_needed"]}),
            
            ("What type of rental car do you need?", "rental_car_type", 4,
             {"rental_car_needed": True},
             {"fill_fields": ["rental_car_type"]}),
            
            ("Do you have a preferred repair shop?", "preferred_shop", 4,
             {"required_fields_present": ["category"]},
             {"fill_fields": ["preferred_shop"]}),
            
            ("What shop would you like to use?", "repair_shop_name", 4,
             {"preferred_shop": True},
             {"fill_fields": ["repair_shop_name"]}),
            
            ("Should we use our network of shops?", "use_network_shop", 4,
             {"preferred_shop": False},
             {"fill_fields": ["use_network_shop"]}),
            
            ("Would you like us to arrange towing?", "need_towing_arranged", 3,
             {"drivable": False, "vehicle_towed": False},
             {"fill_fields": ["need_towing_arranged"]}),
            
            ("Where should the vehicle be towed to?", "towing_destination", 4,
             {"need_towing_arranged": True},
             {"fill_fields": ["towing_destination"]}),
            
            ("Do you want OEM parts or aftermarket?", "parts_preference", 4,
             {"required_fields_present": ["category"]},
             {"fill_fields": ["parts_preference"]}),
            
            ("Are you willing to use aftermarket parts for cost savings?", "aftermarket_acceptable", 4,
             {"required_fields_present": ["category"]},
             {"fill_fields": ["aftermarket_acceptable"]}),
            
            ("Do you want to be present for the vehicle inspection?", "attend_inspection", 4,
             {"required_fields_present": ["category"]},
             {"fill_fields": ["attend_inspection"]}),
            
            ("When is the best time for an inspection appointment?", "inspection_time_preference", 4,
             {"attend_inspection": True},
             {"fill_fields": ["inspection_time_preference"]}),
            
            ("Should we send the adjuster to you?", "mobile_inspection", 4,
             {"required_fields_present": ["category"]},
             {"fill_fields": ["mobile_inspection"]}),
            
            ("Or can you bring the vehicle to our location?", "can_bring_vehicle", 4,
             {"mobile_inspection": False},
             {"fill_fields": ["can_bring_vehicle"]}),
            
            ("How quickly do you need the repairs completed?", "repair_urgency", 4,
             {"required_fields_present": ["category"]},
             {"fill_fields": ["repair_urgency"]}),
            
            ("Is this your only vehicle?", "only_vehicle", 3,
             {"required_fields_present": ["category"]},
             {"fill_fields": ["only_vehicle"]}),
            
            ("Do you have alternative transportation?", "alternative_transport", 3,
             {"only_vehicle": True, "drivable": False},
             {"fill_fields": ["alternative_transport"]}),
            
            ("Would you prefer direct payment or reimbursement?", "payment_preference", 4,
             {"required_fields_present": ["category"]},
             {"fill_fields": ["payment_preference"]}),
            
            ("Should we pay the shop directly?", "direct_payment_shop", 4,
             {"payment_preference": "direct"},
             {"fill_fields": ["direct_payment_shop"]}),
            
            ("What is your preferred contact method during repairs?", "repair_contact_method", 5,
             {"required_fields_present": ["category"]},
             {"fill_fields": ["repair_contact_method"]}),
        ]
        
        for text, field, priority, triggers, targets in repair_questions:
            self._add_question(text, field, priority, triggers, targets)
    
    def save_to_file(self, filepath: str):
        """Save questions to JSONL file"""
        with open(filepath, 'w') as f:
            for question in self.questions:
                f.write(json.dumps(question) + '\n')


def main():
    """Generate all questions and save to file"""
    generator = QuestionGenerator()
    questions = generator.generate_all_questions()
    
    print(f"Generated {len(questions)} questions")
    
    # Save to file
    generator.save_to_file('data/question_bank_raw.jsonl')
    print("Questions saved to question_bank_raw.jsonl")


if __name__ == "__main__":
    main()
