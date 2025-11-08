"""
RAG (Retrieval-Augmented Generation) Pipeline
Handles context retrieval and enhanced AI responses
"""

import logging
from typing import List, Dict, Any
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RAGPipeline:
    """Retrieval-Augmented Generation for student performance analysis"""
    
    def __init__(self):
        self.knowledge_base = []
        self.student_data = {}
        
    def index_student_data(self, students_data: List[Dict]):
        """Index student data for retrieval"""
        self.student_data = {str(s.get('student_id', i)): s for i, s in enumerate(students_data)}
        logger.info(f"Indexed {len(self.student_data)} student records")
    
    def add_to_knowledge_base(self, documents: List[str]):
        """Add educational documents to knowledge base"""
        self.knowledge_base.extend(documents)
        logger.info(f"Added {len(documents)} documents to knowledge base")
    
    def retrieve_student_context(self, student_id: str) -> Dict[str, Any]:
        """Retrieve relevant context for a student"""
        student = self.student_data.get(str(student_id))
        
        if not student:
            return {}
        
        context = {
            'student_id': student_id,
            'academic_info': {},
            'risk_factors': [],
            'strengths': []
        }
        
        # Extract academic information
        for key, value in student.items():
            if 'mark' in key.lower() or 'score' in key.lower() or 'grade' in key.lower():
                context['academic_info'][key] = value
        
        # Identify risk factors and strengths
        if 'at_risk' in student and student['at_risk'] == 'Yes':
            context['risk_factors'].append('Classified as at-risk student')
        
        if 'risk_probability' in student:
            risk_pct = student['risk_probability']
            if risk_pct > 70:
                context['risk_factors'].append(f'High risk probability: {risk_pct:.1f}%')
            elif risk_pct < 30:
                context['strengths'].append(f'Low risk probability: {risk_pct:.1f}%')
        
        return context
    
    def retrieve_similar_cases(self, student_context: Dict, top_k: int = 3) -> List[Dict]:
        """Retrieve similar student cases for comparison"""
        # Simple similarity based on risk probability
        similar_cases = []
        
        if 'risk_probability' not in student_context:
            return similar_cases
        
        target_risk = student_context['risk_probability']
        
        for sid, student in self.student_data.items():
            if sid != str(student_context.get('student_id')):
                if 'risk_probability' in student:
                    risk_diff = abs(student['risk_probability'] - target_risk)
                    similar_cases.append({
                        'student_id': sid,
                        'risk_probability': student['risk_probability'],
                        'similarity_score': 100 - risk_diff,
                        'data': student
                    })
        
        # Sort by similarity and return top_k
        similar_cases.sort(key=lambda x: x['similarity_score'], reverse=True)
        return similar_cases[:top_k]
    
    def retrieve_intervention_strategies(self, risk_factors: List[str]) -> List[str]:
        """Retrieve relevant intervention strategies based on risk factors"""
        strategies = []
        
        # General strategies
        general_strategies = [
            "Regular one-on-one meetings with student",
            "Personalized learning plan",
            "Progress monitoring and feedback",
            "Parent-teacher collaboration"
        ]
        
        # Specific strategies based on risk factors
        for factor in risk_factors:
            if 'attendance' in factor.lower():
                strategies.extend([
                    "Investigate attendance barriers",
                    "Implement attendance tracking system",
                    "Reward good attendance"
                ])
            
            if 'marks' in factor.lower() or 'performance' in factor.lower():
                strategies.extend([
                    "Provide additional tutoring",
                    "Break down complex topics",
                    "Use alternative teaching methods",
                    "Extra practice materials"
                ])
            
            if 'assignment' in factor.lower():
                strategies.extend([
                    "Assignment tracking and reminders",
                    "Break assignments into smaller tasks",
                    "Provide assignment help sessions"
                ])
        
        # Remove duplicates and add general strategies
        strategies = list(set(strategies))
        strategies.extend(general_strategies)
        
        return strategies[:10]  # Return top 10 strategies
    
    def build_context_for_llm(self, query: str, student_id: str = None) -> str:
        """Build comprehensive context for LLM query"""
        context_parts = []
        
        # Add query
        context_parts.append(f"User Query: {query}")
        
        # Add student-specific context if provided
        if student_id:
            student_context = self.retrieve_student_context(student_id)
            if student_context:
                context_parts.append(f"\nStudent Context:")
                context_parts.append(json.dumps(student_context, indent=2))
                
                # Add similar cases
                similar = self.retrieve_similar_cases(student_context)
                if similar:
                    context_parts.append(f"\nSimilar Student Cases:")
                    for case in similar:
                        context_parts.append(f"- Student {case['student_id']}: {case['risk_probability']:.1f}% risk")
        
        # Add general educational knowledge
        context_parts.append("\nEducational Best Practices:")
        context_parts.append("- Early intervention is key to student success")
        context_parts.append("- Personalized learning approaches improve outcomes")
        context_parts.append("- Parent involvement significantly impacts student performance")
        context_parts.append("- Regular feedback and monitoring prevent issues from escalating")
        
        return "\n".join(context_parts)


def create_educational_knowledge_base() -> List[str]:
    """Create a knowledge base of educational best practices"""
    return [
        "Early Intervention: Identifying and addressing learning difficulties early prevents long-term academic struggles.",
        "Personalized Learning: Adapting teaching methods to individual student needs improves engagement and outcomes.",
        "Growth Mindset: Encouraging students to view challenges as opportunities for growth builds resilience.",
        "Regular Assessment: Frequent formative assessments help track progress and adjust instruction accordingly.",
        "Parent Engagement: Active parent involvement in education correlates with higher student achievement.",
        "Peer Support: Peer tutoring and collaborative learning benefit both tutors and learners.",
        "Study Skills: Teaching effective study strategies and time management improves academic performance.",
        "Attendance Matters: Regular attendance is one of the strongest predictors of academic success.",
        "Feedback Quality: Specific, timely, and constructive feedback accelerates learning.",
        "Emotional Support: Addressing emotional and social needs is essential for academic success."
    ]
