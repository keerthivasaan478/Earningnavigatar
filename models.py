from datetime import datetime
from app import db

class Company(db.Model):
    """Model for storing company information"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    ticker = db.Column(db.String(20), nullable=False, unique=True)
    sector = db.Column(db.String(100))
    industry = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    earnings_calls = db.relationship('EarningsCall', backref='company', lazy='dynamic')
    
    def __repr__(self):
        return f'<Company {self.ticker}: {self.name}>'

class EarningsCall(db.Model):
    """Model for storing earnings call data"""
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    fiscal_year = db.Column(db.Integer, nullable=False)
    fiscal_quarter = db.Column(db.Integer, nullable=False)
    call_date = db.Column(db.DateTime, nullable=False)
    transcript_text = db.Column(db.Text)
    audio_url = db.Column(db.String(512))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    analysis = db.relationship('EarningsAnalysis', backref='earnings_call', uselist=False)
    
    def __repr__(self):
        return f'<EarningsCall {self.company.ticker} Q{self.fiscal_quarter} FY{self.fiscal_year}>'

class EarningsAnalysis(db.Model):
    """Model for storing the AI analysis of earnings calls"""
    id = db.Column(db.Integer, primary_key=True)
    earnings_call_id = db.Column(db.Integer, db.ForeignKey('earnings_call.id'), nullable=False)
    sentiment_score = db.Column(db.Float)  # Overall sentiment (-1 to 1)
    guidance_sentiment = db.Column(db.Float)  # Sentiment related to guidance (-1 to 1)
    management_confidence = db.Column(db.Float)  # Confidence score (0 to 1)
    summary = db.Column(db.Text)  # AI-generated summary
    key_metrics = db.Column(db.JSON)  # Extracted financial metrics
    key_topics = db.Column(db.JSON)  # Key topics discussed
    competitor_mentions = db.Column(db.JSON)  # Mentioned competitors
    guidance_changes = db.Column(db.JSON)  # Changes in guidance
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<EarningsAnalysis for {self.earnings_call.company.ticker} Q{self.earnings_call.fiscal_quarter} FY{self.earnings_call.fiscal_year}>'

class Query(db.Model):
    """Model for storing user queries and AI responses"""
    id = db.Column(db.Integer, primary_key=True)
    earnings_call_id = db.Column(db.Integer, db.ForeignKey('earnings_call.id'), nullable=False)
    user_query = db.Column(db.Text, nullable=False)
    ai_response = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to earnings call
    earnings_call = db.relationship('EarningsCall')
    
    def __repr__(self):
        return f'<Query {self.user_query[:20]}...>'
