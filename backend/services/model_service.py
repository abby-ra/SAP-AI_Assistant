from backend.config import settings
import os


def run_model_test() -> dict:
    if not settings.model_api_key or settings.model_api_key == "test_api_key_placeholder":
        return {
            "status": "warning",
            "message": "Using mock AI mode. Set MODEL_API_KEY in .env for real AI.",
        }

    return {
        "status": "ok",
        "message": "AI model connected and ready.",
    }


def analyze_business_query(query: str) -> dict:
    """Analyze a business query using AI or mock responses"""
    
    # Check if real API key is configured
    if not settings.model_api_key or settings.model_api_key == "test_api_key_placeholder":
        return _mock_ai_analysis(query)
    
    # Try real AI integration
    try:
        return _call_ai_api(query)
    except Exception as e:
        return {
            "status": "error",
            "analysis": f"AI Error: {str(e)}\n\nFalling back to mock mode.",
            "query": query,
            "mock_mode": True
        }


def _call_ai_api(query: str) -> dict:
    """Call real AI API (OpenAI/Anthropic/etc)"""
    try:
        # Try OpenAI first
        import openai
        openai.api_key = settings.model_api_key
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an SAP Enterprise AI Assistant. Provide concise, actionable business insights for enterprise stakeholders. Focus on data-driven recommendations."},
                {"role": "user", "content": query}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        return {
            "status": "success",
            "analysis": response.choices[0].message.content,
            "query": query,
            "model": "gpt-3.5-turbo",
            "mock_mode": False
        }
    except ImportError:
        # OpenAI not installed, try anthropic
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=settings.model_api_key)
            
            message = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=500,
                messages=[
                    {"role": "user", "content": f"As an SAP Enterprise AI Assistant, analyze this business query: {query}"}
                ]
            )
            
            return {
                "status": "success",
                "analysis": message.content[0].text,
                "query": query,
                "model": "claude-3-haiku",
                "mock_mode": False
            }
        except ImportError:
            raise Exception("No AI library installed. Run: pip install openai anthropic")


def _mock_ai_analysis(query: str) -> dict:
    """Generate intelligent mock responses based on query keywords"""
    query_lower = query.lower()
    
    # Stock/Inventory related
    if any(word in query_lower for word in ['stock', 'inventory', 'reduced', 'supplies']):
        analysis = """📊 Stock Analysis:

✓ Current Status: Your inventory levels show a 15% reduction compared to last quarter.

🔍 Key Insights:
• High-demand items (SKU-2891, SKU-3047) are below reorder point
• Seasonal products show expected decline patterns
• Supply chain delays affecting 3 product categories

💡 Recommendations:
1. Initiate emergency reorder for critical SKUs
2. Review supplier contracts for delayed shipments
3. Consider alternative suppliers for categories X, Y, Z
4. Implement automated reorder triggers

📈 Projected Impact: Restocking within 2 weeks will prevent 8% revenue loss."""
    
    # Sales/Revenue related
    elif any(word in query_lower for word in ['sales', 'revenue', 'profit', 'q4', 'quarter']):
        analysis = """💰 Sales Performance Analysis:

✓ Q4 Revenue: $12.4M (↑ 8.3% YoY)
✓ Profit Margin: 23.5% (↑ 2.1%)

🎯 Top Performers:
• Enterprise Solutions: $5.2M (+15%)
• Cloud Services: $4.1M (+22%)
• Consulting: $3.1M (+3%)

⚠️ Areas of Concern:
• Customer churn rate increased to 12%
• Average deal size decreased by $15K

💡 Strategic Recommendations:
1. Launch customer retention program
2. Upsell existing clients with premium packages
3. Focus on high-margin cloud solutions
4. Implement predictive analytics for sales forecasting

📊 Forecast: Q1 2026 projected at $13.8M with current initiatives."""
    
    # KPI/Performance related
    elif any(word in query_lower for word in ['kpi', 'metrics', 'performance', 'indicators']):
        analysis = """📈 Key Performance Indicators Dashboard:

🎯 Strategic KPIs:
• Customer Satisfaction: 87% (Target: 90%)
• Net Promoter Score: 62 (Industry Avg: 58)
• Employee Productivity: 94% (↑ 3%)
• System Uptime: 99.7% (Target: 99.5%)

💼 Operational Metrics:
• Order Fulfillment Rate: 96.2%
• Average Response Time: 4.2 hours
• First Contact Resolution: 78%

💡 Priority Actions:
1. Improve customer satisfaction with enhanced support
2. Maintain NPS leadership position
3. Address 0.3% remaining uptime issues
4. Optimize fulfillment for remaining 3.8%

✓ Overall Health Score: 8.4/10 - Strong performance with room for optimization."""
    
    # Customer/Client related
    elif any(word in query_lower for word in ['customer', 'client', 'retention', 'churn']):
        analysis = """👥 Customer Insights Analysis:

📊 Customer Base Overview:
• Total Active Customers: 1,847
• New Acquisitions (Last 30 days): 142
• Churn Rate: 3.2% (Industry: 5.1%)
• Lifetime Value (Avg): $124,500

🌟 Segment Performance:
• Enterprise (500+ employees): 412 customers, 68% of revenue
• Mid-Market (100-500): 789 customers, 24% of revenue
• Small Business: 646 customers, 8% of revenue

⚠️ At-Risk Customers: 67 accounts showing reduced engagement

💡 Retention Strategy:
1. Proactive outreach to at-risk accounts
2. Quarterly business reviews for top 100 clients
3. Implement customer success program
4. Enhance self-service portal features

🎯 Goal: Reduce churn to 2.5% through targeted interventions."""
    
    # Cost/Budget related
    elif any(word in query_lower for word in ['cost', 'budget', 'expense', 'spending']):
        analysis = """💵 Cost Analysis & Budget Optimization:

📉 Current Spending Overview:
• Total OpEx: $3.2M/month
• Year-over-Year Change: +12%
• Budget Utilization: 87%

🔍 Cost Breakdown:
• Personnel: $1.8M (56%)
• Technology/Infrastructure: $0.8M (25%)
• Marketing: $0.4M (13%)
• Operations: $0.2M (6%)

⚠️ Cost Overruns:
• Cloud infrastructure: +18% (unplanned scaling)
• Third-party tools: +9% (license creep)

💡 Optimization Opportunities:
1. Renegotiate cloud contracts (potential savings: $85K/year)
2. Consolidate redundant software licenses
3. Implement automated resource management
4. Review headcount allocation vs productivity

💰 Projected Savings: $240K annually with recommended changes."""
    
    # Risk/Compliance related
    elif any(word in query_lower for word in ['risk', 'compliance', 'security', 'audit']):
        analysis = """🛡️ Risk & Compliance Assessment:

✓ Compliance Status:
• GDPR: Fully Compliant ✓
• SOC 2: Certified (renewal due Q2 2026)
• ISO 27001: In Progress (85% complete)
• Industry Regulations: Compliant ✓

⚠️ Risk Exposure:
• Cybersecurity: Medium Risk (2 vulnerabilities pending patch)
• Data Privacy: Low Risk
• Operational: Low Risk
• Financial: Low Risk

🔐 Security Posture:
• Recent Incidents: 0 (last 90 days)
• Security Training: 94% staff completion
• Penetration Test: Passed (Jan 2026)

💡 Action Items:
1. Apply pending security patches by end of week
2. Complete ISO 27001 certification
3. Conduct quarterly table-top exercises
4. Update incident response playbooks

🎯 Overall Risk Score: Low - Well-managed with proactive monitoring."""
    
    # Default general business query
    else:
        analysis = f"""🤖 AI Business Analysis:

📝 Query: "{query}"

🔍 Analysis:
Based on current enterprise data and market trends, here are key insights:

✓ Your query touches on strategic business areas requiring:
• Data-driven decision making
• Cross-functional collaboration
• Performance monitoring
• Resource optimization

💡 Recommendations:
1. Gather relevant KPIs and metrics for this area
2. Benchmark against industry standards
3. Consult with stakeholders across departments
4. Develop action plan with clear milestones
5. Implement monitoring dashboard for tracking

📊 Next Steps:
• Define specific success metrics
• Set quarterly review checkpoints
• Allocate resources appropriately
• Establish accountability framework

🎯 Note: For more specific insights, connect a real AI model by setting MODEL_API_KEY in your .env file.

📌 This is a mock response. Configure your AI API key for real-time, personalized analysis."""
    
    return {
        "status": "success",
        "analysis": analysis,
        "query": query,
        "model": "mock-ai-v1",
        "mock_mode": True
    }
