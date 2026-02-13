"""
LLM-based Analysis Service for SAP AI Assistant
Uses Hugging Face transformers (DistilGPT-2) for dynamic text generation
"""
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch
from typing import Dict
import warnings

warnings.filterwarnings('ignore')


class LLMAnalysisService:
    """LLM service for generating business analysis using DistilGPT-2"""
    
    def __init__(self):
        self.model_name = "distilgpt2"
        self.generator = None
        self.tokenizer = None
        self.model = None
        self._initialized = False
    
    def _initialize_model(self):
        """Lazy load the model on first use"""
        if self._initialized:
            return
        
        try:
            print(f"Loading LLM model: {self.model_name}...")
            
            # Load tokenizer and model
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
            
            # Create text generation pipeline
            self.generator = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                device=-1,  # CPU
                max_new_tokens=200,
                temperature=0.7,
                top_p=0.9,
                do_sample=True
            )
            
            self._initialized = True
            print("LLM model loaded successfully!")
            
        except Exception as e:
            print(f"Error loading LLM model: {e}")
            self._initialized = False
            raise e
    
    def generate_analysis(self, query: str, category: str, ml_insights: Dict) -> str:
        """
        Generate dynamic business analysis using LLM
        
        Args:
            query: User's business query
            category: ML-categorized category
            ml_insights: ML insights including impact metrics
        
        Returns:
            Generated analysis text
        """
        # Initialize model if needed
        if not self._initialized:
            self._initialize_model()
        
        if not self._initialized:
            return None  # Fallback to template-based
        
        # Build prompt
        prompt = self._build_prompt(query, category, ml_insights)
        
        try:
            # Generate text
            result = self.generator(
                prompt,
                max_new_tokens=150,
                num_return_sequences=1,
                pad_token_id=self.tokenizer.eos_token_id
            )
            
            # Extract generated text (remove prompt)
            generated_text = result[0]['generated_text']
            analysis = generated_text[len(prompt):].strip()
            
            # Clean up the output
            analysis = self._clean_output(analysis)
            
            return analysis
            
        except Exception as e:
            print(f"Error generating LLM analysis: {e}")
            return None
    
    def _build_prompt(self, query: str, category: str, ml_insights: Dict) -> str:
        """Build a structured prompt for the LLM"""
        
        impact = ml_insights.get('impact_metrics', {})
        priority = impact.get('priority', 'Medium')
        impact_score = impact.get('impact_score', 0.5)
        
        category_context = {
            'stock_inventory': 'inventory management and supply chain',
            'sales_revenue': 'sales performance and revenue growth',
            'kpi_metrics': 'key performance indicators and business metrics',
            'customer_analysis': 'customer insights and retention',
            'cost_budget': 'cost optimization and budget management',
            'risk_compliance': 'risk assessment and compliance'
        }
        
        context = category_context.get(category, 'business operations')
        
        prompt = f"""Business Analysis Report

Query: {query}
Category: {category.replace('_', ' ').title()}
Priority: {priority}
Impact Score: {impact_score}/1.0

Analysis:
Based on current data and trends in {context}, here are the key findings:

1. Current Situation:"""
        
        return prompt
    
    def _clean_output(self, text: str) -> str:
        """Clean and format the generated output"""
        # Remove incomplete sentences at the end
        sentences = text.split('.')
        
        # Keep only complete sentences (at least 10 chars)
        complete_sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
        
        # Rejoin with proper punctuation
        if complete_sentences:
            cleaned = '. '.join(complete_sentences[:5])  # Max 5 sentences
            if not cleaned.endswith('.'):
                cleaned += '.'
            return cleaned
        
        return text[:300]  # Fallback: truncate to 300 chars


# Global instance
_llm_service = None

def get_llm_service() -> LLMAnalysisService:
    """Get or create LLM service singleton"""
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMAnalysisService()
    return _llm_service
