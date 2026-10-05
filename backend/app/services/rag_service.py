import json
import math
from typing import List, Dict, Any, Tuple
from pathlib import Path
from backend.app.config import BASE_DIR, settings

class RAGService:
    """
    RAG Knowledge Base & Policy Retrieval Service.
    Implements:
    1. Chunk indexing with character n-gram + term weighting vectorizer
    2. Hybrid cosine similarity matching
    3. Confidence threshold verification (refusal / human escalation for ungrounded queries)
    4. Exact citation extraction with policy codes
    """

    def __init__(self):
        self.chunks: List[Dict[str, Any]] = []
        self._load_knowledge_base()

    def _load_knowledge_base(self):
        kb_path = BASE_DIR / "dataset" / "rag" / "knowledge_base.json"
        if kb_path.exists():
            with open(kb_path, "r", encoding="utf-8") as f:
                self.chunks = json.load(f)

    def _tokenize(self, text: str) -> List[str]:
        # Character bigram + keyword extraction
        text = text.lower().strip()
        tokens = []
        # Add single significant characters
        for ch in text:
            if '\u4e00' <= ch <= '\u9fa5' or ch.isalnum():
                tokens.append(ch)
        # Add bigrams
        for i in range(len(text) - 1):
            pair = text[i:i+2]
            if all('\u4e00' <= c <= '\u9fa5' or c.isalnum() for c in pair):
                tokens.append(pair)
        return tokens

    def _compute_similarity(self, query: str, chunk_text: str) -> float:
        q_tokens = set(self._tokenize(query))
        c_tokens = set(self._tokenize(chunk_text))
        if not q_tokens or not c_tokens:
            return 0.0

        intersection = q_tokens.intersection(c_tokens)
        # Jaccard / Dice overlap combined with length norm
        dice = (2.0 * len(intersection)) / (len(q_tokens) + len(c_tokens))
        
        # Keyword weighting boost for high-salience terms
        important_keywords = [
            "退货", "换货", "保修", "维修", "顺丰", "运费", "发票", "包装", "过敏", 
            "进水", "摔碎", "屏幕", "电机", "延误", "改地址", "拒收", "签收", "丢失", "超时", "赠品"
        ]
        boost = 0.0
        for kw in important_keywords:
            if kw in query and kw in chunk_text:
                boost += 0.08

        score = min(dice * 0.7 + boost, 1.0)
        return round(score, 4)

    def search(self, query: str, top_k: int = 3) -> Dict[str, Any]:
        """
        Search knowledge base. If highest score < threshold, returns refusal indicator.
        """
        results = []
        for chunk in self.chunks:
            full_text = f"{chunk['title']} {chunk['content']}"
            score = self._compute_similarity(query, full_text)
            results.append({
                "policy_code": chunk["policy_code"],
                "category": chunk["category"],
                "title": chunk["title"],
                "content": chunk["content"],
                "score": score
            })

        results.sort(key=lambda x: x["score"], reverse=True)
        top_results = results[:top_k]

        max_score = top_results[0]["score"] if top_results else 0.0
        is_grounded = max_score >= settings.RAG_SIMILARITY_THRESHOLD

        citations = []
        if is_grounded:
            for item in top_results:
                if item["score"] >= settings.RAG_SIMILARITY_THRESHOLD - 0.1:
                    citations.append({
                        "policy_code": item["policy_code"],
                        "title": item["title"],
                        "snippet": item["content"][:120] + "...",
                        "score": item["score"]
                    })

        return {
            "query": query,
            "is_grounded": is_grounded,
            "max_score": max_score,
            "threshold": settings.RAG_SIMILARITY_THRESHOLD,
            "citations": citations,
            "matched_chunks": top_results if is_grounded else []
        }

rag_service = RAGService()
