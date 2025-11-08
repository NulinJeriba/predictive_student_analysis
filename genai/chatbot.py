import os
from typing import List, Dict, Optional
from rag_pipeline import RAGPipeline, create_educational_knowledge_base

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class StudentPerformanceChatbot:
    def __init__(self, api_key: Optional[str] = None, model: str = 'gpt-3.5-turbo'):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.model = model
        self.rag_pipeline = RAGPipeline()
        self.conversation_history = []
        knowledge_base = create_educational_knowledge_base()
        self.rag_pipeline.add_to_knowledge_base(knowledge_base)
        if self.api_key and OPENAI_AVAILABLE:
            openai.api_key = self.api_key
            self.use_openai = True
        else:
            self.use_openai = False

    def index_student_data(self, students_data: List[Dict]):
        self.rag_pipeline.index_student_data(students_data)

    def chat(self, user_message: str, student_id: Optional[str] = None) -> str:
        context = self.rag_pipeline.build_context_for_llm(user_message, student_id)
        if self.use_openai:
            response = self._generate_openai_response(user_message, context)
        else:
            response = self._generate_fallback_response(user_message, student_id)
        self.conversation_history.append({
            'user': user_message,
            'assistant': response,
            'student_id': student_id
        })
        return response

    def _generate_openai_response(self, user_message: str, context: str) -> str:
        try:
            system_prompt = """You are an expert educational advisor and data analyst specializing in student performance. 
Your role is to:
1. Analyze student performance data and provide insights
2. Explain why students might be at risk
3. Suggest evidence-based intervention strategies
4. Answer questions about educational best practices
5. Provide actionable, practical advice for teachers and administrators

Be empathetic, professional, and focus on solutions that help students succeed."""

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"{context}\n\nQuestion: {user_message}"}
            ]

            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )

            return response.choices[0].message.content.strip()
        except Exception:
            return self._generate_fallback_response(user_message, None)

    def _generate_fallback_response(self, user_message: str, student_id: Optional[str]) -> str:
        message_lower = user_message.lower()
        if student_id:
            student_context = self.rag_pipeline.retrieve_student_context(student_id)
            if 'why' in message_lower and 'risk' in message_lower:
                return self._explain_risk(student_context)
            if 'how' in message_lower and ('improve' in message_lower or 'help' in message_lower):
                return self._suggest_improvements(student_context)
            if 'what' in message_lower and 'intervention' in message_lower:
                return self._suggest_interventions(student_context)

        if 'at risk' in message_lower or 'failing' in message_lower:
            return """At-risk students are those predicted to have academic difficulties based on factors like:
- Low attendance rates
- Declining grades or marks
- Incomplete assignments
- Poor class participation

Early identification allows for timely intervention and support."""

        if 'intervention' in message_lower or 'help' in message_lower:
            return """Effective interventions for at-risk students include:
1. Personalized learning plans tailored to individual needs
2. Regular one-on-one meetings to track progress
3. Peer tutoring and mentorship programs
4. Parent-teacher collaboration and communication
5. Additional academic support and tutoring
6. Study skills and time management training
7. Addressing attendance and engagement issues
8. Setting clear, achievable goals with regular check-ins"""

        if 'attendance' in message_lower:
            return """Attendance is critical for academic success. To improve attendance:
- Identify and address barriers (transportation, health, family issues)
- Implement positive reinforcement for good attendance
- Communicate regularly with parents
- Make learning engaging and relevant
- Provide support for students facing challenges"""

        if 'model' in message_lower or 'prediction' in message_lower:
            return """The prediction system uses machine learning models (Random Forest and SVM) trained on historical student data.
The models analyze factors like marks, attendance, assignments, and participation to predict which students may need support.
The system provides probability scores and explanations to help educators make informed decisions."""

        return """I can help you understand student performance predictions and suggest interventions.

You can ask me:
- \"Why is student X at risk?\"
- \"How can I help improve this student's performance?\"
- \"What interventions work for at-risk students?\"
- \"Explain the prediction model\"
- \"What factors indicate a student is at risk?\"

Please provide more details about your question, and I'll do my best to assist you."""

    def _explain_risk(self, student_context: Dict) -> str:
        if not student_context:
            return "Unable to retrieve student information."
        risk_factors = student_context.get('risk_factors', [])
        if not risk_factors:
            return "This student shows positive indicators and is not currently classified as at-risk."
        explanation = f"Student {student_context.get('student_id')} is at risk due to:\n\n"
        for i, factor in enumerate(risk_factors, 1):
            explanation += f"{i}. {factor}\n"
        explanation += "\nThese factors suggest the student may benefit from additional support and intervention."
        return explanation

    def _suggest_improvements(self, student_context: Dict) -> str:
        if not student_context:
            return "Unable to retrieve student information."
        risk_factors = student_context.get('risk_factors', [])
        strategies = self.rag_pipeline.retrieve_intervention_strategies(risk_factors)
        response = f"To help Student {student_context.get('student_id')} improve, consider:\n\n"
        for i, strategy in enumerate(strategies[:5], 1):
            response += f"{i}. {strategy}\n"
        response += "\nFocus on building a supportive relationship and addressing underlying issues."
        return response

    def _suggest_interventions(self, student_context: Dict) -> str:
        if not student_context:
            return "Unable to retrieve student information."
        risk_factors = student_context.get('risk_factors', [])
        strategies = self.rag_pipeline.retrieve_intervention_strategies(risk_factors)
        response = f"Intervention Plan for Student {student_context.get('student_id')}:\n\n"
        response += "IMMEDIATE ACTIONS:\n"
        for strategy in strategies[:3]:
            response += f"• {strategy}\n"
        response += "\nSHORT-TERM GOALS (1-2 months):\n"
        response += "• Improve attendance to 85%+\n"
        response += "• Complete all assignments on time\n"
        response += "• Show measurable academic improvement\n"
        response += "\nLONG-TERM STRATEGIES:\n"
        for strategy in strategies[3:6]:
            response += f"• {strategy}\n"
        response += "\nMonitor progress weekly and adjust the plan as needed."
        return response

    def get_conversation_history(self) -> List[Dict]:
        return self.conversation_history

    def clear_history(self):
        self.conversation_history = []


def get_chatbot_response(message: str, student_id: Optional[str] = None, students_data: Optional[List[Dict]] = None) -> str:
    chatbot = StudentPerformanceChatbot()
    if students_data:
        chatbot.index_student_data(students_data)
    return chatbot.chat(message, student_id)
