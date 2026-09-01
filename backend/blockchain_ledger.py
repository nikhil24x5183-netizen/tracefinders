import hashlib
import json
import time
from typing import List, Dict, Any

class EvidenceBlock:
    def __init__(self, index: int, timestamp: str, case_id: str, action_type: str, actor: str, data_payload: Dict[str, Any], previous_hash: str):
        self.index = index
        self.timestamp = timestamp
        self.case_id = case_id
        self.action_type = action_type
        self.actor = actor
        self.data_payload = data_payload
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "case_id": self.case_id,
            "action_type": self.action_type,
            "actor": self.actor,
            "data_payload": self.data_payload,
            "previous_hash": self.previous_hash
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode('utf-8')).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "case_id": self.case_id,
            "action_type": self.action_type,
            "actor": self.actor,
            "data_payload": self.data_payload,
            "previous_hash": self.previous_hash,
            "hash": self.hash
        }

class BlockchainEvidenceLedger:
    def __init__(self):
        self.chain: List[EvidenceBlock] = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis = EvidenceBlock(
            index=0,
            timestamp="2026-08-15 00:00:00",
            case_id="SYSTEM",
            action_type="GENESIS_BLOCK_INITIALIZED",
            actor="TRACE-X Cryptographic Kernel",
            data_payload={"system": "TRACE-X Evidence Ledger Engine", "hash_algo": "SHA-256"},
            previous_hash="0" * 64
        )
        self.chain.append(genesis)

    def add_evidence_block(self, case_id: str, action_type: str, actor: str, data_payload: Dict[str, Any]) -> EvidenceBlock:
        prev_block = self.chain[-1]
        new_block = EvidenceBlock(
            index=len(self.chain),
            timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
            case_id=case_id,
            action_type=action_type,
            actor=actor,
            data_payload=data_payload,
            previous_hash=prev_block.hash
        )
        self.chain.append(new_block)
        return new_block

    def verify_integrity(self) -> Dict[str, Any]:
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.hash != current.calculate_hash():
                return {
                    "is_valid": False,
                    "tampered_block_index": current.index,
                    "reason": f"Block #{current.index} data hash mismatch! Recorded: {current.hash[:16]}... Calculated: {current.calculate_hash()[:16]}..."
                }

            if current.previous_hash != previous.hash:
                return {
                    "is_valid": False,
                    "tampered_block_index": current.index,
                    "reason": f"Block #{current.index} previous_hash pointer link broken!"
                }

        return {
            "is_valid": True,
            "total_blocks": len(self.chain),
            "latest_block_hash": self.chain[-1].hash,
            "status": "ALL_BLOCKS_VERIFIED_SECURE"
        }

    def simulate_tamper(self, block_index: int, field_to_tamper: str, tampered_val: str) -> Dict[str, Any]:
        if block_index < 0 or block_index >= len(self.chain):
            return {"success": False, "error": "Invalid block index."}

        target = self.chain[block_index]
        target.data_payload[field_to_tamper] = tampered_val
        return {
            "success": True,
            "tampered_block_index": block_index,
            "tampered_field": field_to_tamper,
            "tampered_value": tampered_val,
            "message": "Block payload intentionally tampered without updating block hash to test verification auditor."
        }

evidence_ledger = BlockchainEvidenceLedger()
