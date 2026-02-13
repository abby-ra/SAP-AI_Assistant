"""
ML-based Analysis Service for SAP AI Assistant
Uses scikit-learn for intelligent query categorization and insight generation
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import Dict, List, Tuple


class MLAnalysisService:
    """Machine Learning service for business query analysis"""
    
    def __init__(self):
        # Training data: categories and example queries
        self.categories = {
            'stock_inventory': {
                'keywords': ['stock', 'inventory', 'reduced', 'supplies', 'warehouse', 'reorder', 'sku'],
                'examples': [
                    'Is stock getting reduced?',
                    'What is our inventory level?',
                    'Do we need to reorder supplies?',
                    'Show me warehouse stock levels'
                ]
            },
            'sales_revenue': {
                'keywords': ['sales', 'revenue', 'profit', 'quarter', 'q4', 'growth', 'earnings'],
                'examples': [
                    'What are Q4 sales trends?',
                    'Show me revenue growth',
                    'How is our profit margin?',
                    'Sales performance this quarter'
                ]
            },
            'kpi_metrics': {
                'keywords': ['kpi', 'metrics', 'performance', 'indicators', 'dashboard', 'score'],
                'examples': [
                    'Show me key performance indicators',
                    'What are our KPIs?',
                    'Performance metrics dashboard',
                    'How are we performing?'
                ]
            },
            'customer_analysis': {
                'keywords': ['customer', 'client', 'retention', 'churn', 'satisfaction', 'nps'],
                'examples': [
                    'What is our customer retention rate?',
                    'Show me customer churn analysis',
                    'Customer satisfaction scores',
                    'NPS trends'
                ]
            },
            'cost_budget': {
                'keywords': ['cost', 'budget', 'expense', 'spending', 'opex', 'savings'],
                'examples': [
                    'Where can we reduce costs?',
                    'Show me budget utilization',
                    'What are our expenses?',
                    'Cost optimization opportunities'
                ]
            },
            'risk_compliance': {
                'keywords': ['risk', 'compliance', 'security', 'audit', 'gdpr', 'regulation'],
                'examples': [
                    'What are our compliance risks?',
                    'Security audit status',
                    'GDPR compliance check',
                    'Risk assessment report'
                ]
            }
        }
        
        # Build training corpus
        self.training_queries = []
        self.training_labels = []
        for category, data in self.categories.items():
            for example in data['examples']:
                self.training_queries.append(example)
                self.training_labels.append(category)
        
        # Initialize TF-IDF vectorizer
        self.vectorizer = TfidfVectorizer(
            max_features=100,
            ngram_range=(1, 2),
            stop_words='english'
        )
        
        # Fit on training data
        self.training_vectors = self.vectorizer.fit_transform(self.training_queries)
    
    def categorize_query(self, query: str) -> Tuple[str, float]:
        """
        Categorize a business query using ML
        Returns: (category, confidence_score)
        """
        # Vectorize the query
        query_vector = self.vectorizer.transform([query])
        
        # Calculate similarity with all training examples
        similarities = cosine_similarity(query_vector, self.training_vectors)[0]
        
        # Find best match
        best_match_idx = np.argmax(similarities)
        confidence = similarities[best_match_idx]
        category = self.training_labels[best_match_idx]
        
        return category, float(confidence)
    
    def calculate_business_impact(self, query: str, category: str) -> Dict[str, any]:
        """
        Calculate business impact metrics using ML-based scoring
        """
        query_lower = query.lower()
        
        # Impact scoring based on urgency keywords
        urgency_keywords = ['urgent', 'critical', 'immediate', 'asap', 'emergency', 'now']
        urgency_score = sum(1 for kw in urgency_keywords if kw in query_lower) * 0.2
        
        # Financial impact based on category
        financial_impact = {
            'stock_inventory': 0.8,  # High impact - affects revenue
            'sales_revenue': 0.9,    # Very high impact
            'cost_budget': 0.85,     # High impact - affects bottom line
            'customer_analysis': 0.7, # Medium-high impact
            'kpi_metrics': 0.6,      # Medium impact
            'risk_compliance': 0.75  # High impact - regulatory
        }
        
        base_impact = financial_impact.get(category, 0.5)
        total_impact = min(1.0, base_impact + urgency_score)
        
        # Generate priority level
        if total_impact >= 0.8:
            priority = "High"
        elif total_impact >= 0.6:
            priority = "Medium"
        else:
            priority = "Low"
        
        return {
            'impact_score': round(total_impact, 2),
            'priority': priority,
            'category': category,
            'confidence': round(urgency_score + 0.5, 2)
        }
    
    def generate_ml_insights(self, query: str) -> Dict[str, any]:
        """
        Generate ML-enhanced insights for a business query
        """
        # Categorize the query
        category, confidence = self.categorize_query(query)
        
        # Calculate business impact
        impact_metrics = self.calculate_business_impact(query, category)
        
        # Generate recommendations based on category
        recommendations = self._get_category_recommendations(category)
        
        return {
            'category': category,
            'confidence': round(confidence, 2),
            'impact_metrics': impact_metrics,
            'recommendations': recommendations,
            'ml_model': 'scikit-learn-tfidf-v1'
        }
    
    def _get_category_recommendations(self, category: str) -> List[str]:
        """Get ML-driven recommendations based on category"""
        recommendations_map = {
            'stock_inventory': [
                'Review inventory turnover ratios',
                'Implement automated reorder points',
                'Analyze supplier lead times',
                'Consider just-in-time inventory strategies'
            ],
            'sales_revenue': [
                'Focus on high-margin products',
                'Implement upselling strategies',
                'Analyze customer acquisition costs',
                'Review pricing optimization opportunities'
            ],
            'kpi_metrics': [
                'Set SMART goals for underperforming metrics',
                'Implement real-time monitoring dashboards',
                'Benchmark against industry standards',
                'Establish regular review cadence'
            ],
            'customer_analysis': [
                'Implement customer success programs',
                'Conduct NPS surveys regularly',
                'Analyze customer journey touchpoints',
                'Develop retention strategies for at-risk segments'
            ],
            'cost_budget': [
                'Conduct zero-based budgeting review',
                'Identify redundant software licenses',
                'Negotiate vendor contracts',
                'Implement cost allocation tracking'
            ],
            'risk_compliance': [
                'Schedule regular compliance audits',
                'Update security policies and procedures',
                'Conduct employee training programs',
                'Implement continuous monitoring systems'
            ]
        }
        
        return recommendations_map.get(category, [
            'Gather relevant data and metrics',
            'Consult with stakeholders',
            'Develop action plan with milestones',
            'Monitor progress regularly'
        ])


# Global instance
_ml_service = None

def get_ml_service() -> MLAnalysisService:
    """Get or create ML service singleton"""
    global _ml_service
    if _ml_service is None:
        _ml_service = MLAnalysisService()
    return _ml_service
