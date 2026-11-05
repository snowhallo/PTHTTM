import logging
from typing import Dict, Any, List, Optional

from knowledge_graph.graph_engine import graph_engine
from knowledge_graph.neo4j_manager import neo4j_manager
from chatbot.entity_extractor import entity_extractor
from chatbot.llm_client import llm_client
from chatbot.local_synthesizer import local_synthesizer

logger = logging.getLogger("MedicalGraphRAG")

class MedicalGraphRAG:
    """
    Graph Retrieval-Augmented Generation (GraphRAG) Orchestrator for Diabetes Healthcare.
    Coordinates entity extraction, knowledge graph retrieval, Generative LLM reasoning, 
    and local clinical synthesis.
    """
    def __init__(self):
        self.entity_extractor = entity_extractor
        self.llm_client = llm_client
        self.local_synthesizer = local_synthesizer

    @property
    def gemini_api_key(self) -> str:
        return self.llm_client.gemini_api_key

    @property
    def openai_api_key(self) -> str:
        return self.llm_client.openai_api_key

    def set_api_keys(self, gemini_key: str = "", openai_key: str = ""):
        """Dynamically updates and persists API keys for LLM reasoning."""
        self.llm_client.set_api_keys(gemini_key=gemini_key, openai_key=openai_key)

    def extract_keywords_and_intent(self, text: str) -> Dict[str, Any]:
        """Extracts medical entities, numbers, and user intents from user prompt."""
        return self.entity_extractor.extract_keywords_and_intent(text)

    def retrieve_graph_context(self, node_ids: List[str]) -> Dict[str, Any]:
        """Retrieves subgraph information, medicines, indications, prices, and relations."""
        context_items = []
        medicines = []
        symptoms = []
        complications = []
        lifestyle = []
        
        for nid in node_ids:
            details = graph_engine.get_node_details_and_neighbors(nid)
            if not details:
                continue
                
            node = details["node"]
            n_type = node.get("type")
            
            if n_type == "Medicine":
                medicines.append(node)
            elif n_type == "Symptom":
                symptoms.append(node)
            elif n_type == "Complication":
                complications.append(node)
            elif n_type == "DietLifestyle":
                lifestyle.append(node)
                
            summary_str = f"• [{n_type}] **{node.get('label')}**: {node.get('summary', '')}"
            if "active_ingredient" in node:
                summary_str += f" (Hoạt chất: {node.get('active_ingredient')})"
            if "price_ref" in node:
                summary_str += f" - Giá Nhà thuốc Long Châu: {node.get('price_ref')}"
            if "dosage" in node:
                summary_str += f" | Cách dùng: {node.get('dosage')}"
            context_items.append(summary_str)
            
            # Relations
            for rel in details.get("outgoing", [])[:4]:
                context_items.append(f"   ↳ {rel['relation']} ➔ {rel['target_label']} ({rel['title']})")
                
        return {
            "formatted_context": "\n".join(context_items),
            "medicines": medicines,
            "symptoms": symptoms,
            "complications": complications,
            "lifestyle": lifestyle,
            "raw_nodes": node_ids
        }

    def generate_response(self, user_query: str, ml_prediction: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Generates accurate, medically grounded GraphRAG response targeted to the question."""
        extracted = self.extract_keywords_and_intent(user_query)
        node_ids = extracted["matched_node_ids"]
        intents = extracted["intents"]
        
        graph_context = self.retrieve_graph_context(node_ids)
        
        # 1. Try Generative LLM if Gemini / OpenAI API Key is available
        llm_answer = None
        if self.gemini_api_key:
            llm_answer = self.llm_client.call_gemini(user_query, graph_context, ml_prediction)
        elif self.openai_api_key:
            llm_answer = self.llm_client.call_openai(user_query, graph_context, ml_prediction)
            
        # 2. If LLM produced answer, use it; otherwise use Local Targeted Synthesizer
        if llm_answer:
            answer = llm_answer
            mode = "Generative LLM (Gemini/OpenAI) + GraphRAG"
        else:
            answer = self.local_synthesizer.synthesize_response(user_query, graph_context, ml_prediction, extracted)
            mode = "Local Knowledge Graph Engine"
        
        return {
            "answer": answer,
            "extracted_entities": [graph_engine.graph.nodes[n].get("label", n) for n in node_ids if n in graph_engine.graph],
            "related_nodes": node_ids,
            "knowledge_source": "Nhà thuốc Long Châu Medical Knowledge Graph",
            "intents": intents,
            "engine_mode": mode
        }

# Singleton instance
medical_bot = MedicalGraphRAG()
