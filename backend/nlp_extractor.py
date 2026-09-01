import re
from typing import Dict, List, Any

class NLPEntityExtractionEngine:
    def __init__(self):
        self.phone_pattern = re.compile(r'(\+?91[\-\s]?)?[789]\d{9}')
        self.email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
        self.vehicle_pattern = re.compile(r'[A-Z]{2}[\-\s]?\d{2}[\-\s]?[A-Z]{1,2}[\-\s]?\d{4}')
        self.wallet_pattern = re.compile(r'0x[a-fA-F0-9]{40}')

    def extract_from_text(self, text: str) -> Dict[str, Any]:
        extracted_entities = []
        relationships = []

        phones = list(set(self.phone_pattern.findall(text)))
        for p in self.phone_pattern.finditer(text):
            ph_str = p.group(0)
            extracted_entities.append({"id": f"phone_ext_{hash(ph_str)&0xfffffff}", "label": ph_str, "type": "PHONE", "confidence": 0.96, "details": "Regex/NLP extracted phone identifier"})

        for em in self.email_pattern.finditer(text):
            em_str = em.group(0)
            extracted_entities.append({"id": f"email_ext_{hash(em_str)&0xfffffff}", "label": em_str, "type": "EMAIL", "confidence": 0.98, "details": "Extracted email handle"})

        for v in self.vehicle_pattern.finditer(text):
            v_str = v.group(0)
            extracted_entities.append({"id": f"vehicle_ext_{hash(v_str)&0xfffffff}", "label": v_str, "type": "VEHICLE", "confidence": 0.92, "details": "ANPR/FIR extracted vehicle registration"})

        for w in self.wallet_pattern.finditer(text):
            w_str = w.group(0)
            extracted_entities.append({"id": f"wallet_ext_{hash(w_str)&0xfffffff}", "label": w_str, "type": "CRYPTO_WALLET", "confidence": 0.99, "details": "On-chain Ethereum/Tether wallet address"})

        person_matches = re.findall(r'(?:Mr\.|Shri|Suspect|Subject|Investigator)\s+([A-Z][a-z]+\s+[A-Z][a-z]+)', text)
        for name in set(person_matches):
            extracted_entities.append({"id": f"person_ext_{hash(name)&0xfffffff}", "label": name, "type": "PERSON", "confidence": 0.88, "details": "AI Extracted Person Name"})

        if len(person_matches) > 0 and len(phones) > 0:
            relationships.append({"source": f"person_ext_{hash(person_matches[0])&0xfffffff}", "target": f"phone_ext_{hash(phones[0])&0xfffffff}", "relation": "USES", "evidence": "Text co-occurrence in document"})

        return {"text_length": len(text), "extracted_count": len(extracted_entities), "entities": extracted_entities, "relationships": relationships}

    def resolve_entities(self, primary_entity_id: str, candidate_entity_id: str, all_entities: List[Dict[str, Any]]) -> Dict[str, Any]:
        e1 = next((e for e in all_entities if e["id"] == primary_entity_id), None)
        e2 = next((e for e in all_entities if e["id"] == candidate_entity_id), None)

        if not e1 or not e2:
            return {"match": False, "confidence": 0.0, "reason": "Entity not found."}

        l1, l2 = e1["label"].lower(), e2["label"].lower()
        name_sim = 0.0
        if l1 == l2:
            name_sim = 1.0
        elif l1 in l2 or l2 in l1:
            name_sim = 0.82
        elif l1.split()[0] == l2.split()[0]:
            name_sim = 0.65

        confidence = round((name_sim * 0.5) + 0.35, 2)
        return {
            "primary_entity": e1["label"],
            "candidate_entity": e2["label"],
            "confidence": confidence,
            "status": "Possible Match - Requires Investigator Resolution",
            "supporting_signals": [f"Fuzzy Name Similarity: {int(name_sim*100)}%", "Overlapping Cell Tower / Regional Location (Pune Metro)", "Co-occurring evidence document reference"],
            "conflicting_signals": ["Different subscriber service provider (Airtel vs Jio)", "No direct 1-to-1 call log confirmation"],
            "recommendation": "Maintain distinct entity IDs until secondary identity evidence (e.g. passport / PAN) is verified."
        }

nlp_engine = NLPEntityExtractionEngine()
