import React, { useState, useEffect, useRef } from 'react';
import './Chatbot.css';

const Chatbot = ({ predictionResults }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [chatMessage, setChatMessage] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [isTyping, setIsTyping] = useState(false);
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatHistory]);

  const handleChatSubmit = async (e) => {
    e.preventDefault();
    if (!chatMessage.trim()) return;

    const userMessage = { role: 'user', content: chatMessage, timestamp: new Date() };
    setChatHistory([...chatHistory, userMessage]);
    setChatMessage('');
    setIsTyping(true);

    try {
      const response = await fetch('http://localhost:5000/api/chatbot', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: chatMessage,
          students_data: predictionResults?.predictions || [],
          context: {
            total_students: predictionResults?.total_students || 0,
            at_risk_count: predictionResults?.at_risk_count || 0,
            at_risk_percentage: predictionResults?.at_risk_percentage || 0
          }
        }),
      });

      const data = await response.json();

      const botResponse = {
        role: 'assistant',
        content: data.response || data.message || 'I apologize, but I encountered an issue. Please try again.',
        timestamp: new Date()
      };

      setTimeout(() => {
        setChatHistory(prev => [...prev, botResponse]);
        setIsTyping(false);
      }, 500);

    } catch (_error) {
      const botResponse = {
        role: 'assistant',
        content: generateFallbackResponse(chatMessage),
        timestamp: new Date()
      };

      setTimeout(() => {
        setChatHistory(prev => [...prev, botResponse]);
        setIsTyping(false);
      }, 500);
    }
  };

  const generateFallbackResponse = (message) => {
    const lowerMessage = message.toLowerCase();

    if (lowerMessage.includes('student') && (lowerMessage.match(/\d+/) || lowerMessage.includes('specific'))) {
      return `To analyze a specific student, please provide their ID. Based on the current predictions, ${predictionResults?.at_risk_count || 0} students are at risk. Click on individual students in the results table for detailed analysis.`;
    }

    if (lowerMessage.includes('at risk') || lowerMessage.includes('failing')) {
      const atRiskCount = predictionResults?.at_risk_count || 0;
      const atRiskPct = predictionResults?.at_risk_percentage || 0;
      return `Currently, ${atRiskCount} students (${atRiskPct.toFixed(1)}%) are identified as at-risk. These students show indicators like low marks, poor attendance, or declining performance. Early intervention can significantly improve their outcomes.`;
    }

    if (lowerMessage.includes('intervention') || lowerMessage.includes('help') || lowerMessage.includes('improve')) {
      return `Effective interventions include:\n\n1. **Personalized Support**: One-on-one tutoring tailored to individual needs\n2. **Regular Monitoring**: Weekly check-ins to track progress\n3. **Parent Engagement**: Involve parents in the improvement plan\n4. **Peer Mentoring**: Pair struggling students with high-achievers\n5. **Study Skills Training**: Teach time management and learning strategies\n6. **Address Root Causes**: Identify and resolve attendance or personal issues\n\nEarly intervention is key to success!`;
    }

    if (lowerMessage.includes('attendance')) {
      return `Attendance is one of the strongest predictors of academic success. To improve attendance:\n\n• Identify barriers (transportation, health, family issues)\n• Implement positive reinforcement programs\n• Communicate regularly with parents\n• Make learning engaging and relevant\n• Provide support for students facing challenges\n\nStudents with <75% attendance are at significantly higher risk.`;
    }

    if (lowerMessage.includes('mark') || lowerMessage.includes('grade') || lowerMessage.includes('score')) {
      return `Academic performance is analyzed across multiple subjects. Students with average marks below 50% are flagged as at-risk. Key factors affecting marks include:\n\n• Understanding of core concepts\n• Study habits and time management\n• Attendance and class participation\n• Assignment completion\n• Previous performance trends\n\nConsider subject-specific tutoring for students struggling in particular areas.`;
    }

    if (lowerMessage.includes('model') || lowerMessage.includes('prediction') || lowerMessage.includes('accurate') || lowerMessage.includes('how does')) {
      return `The system uses machine learning models (Random Forest and SVM) trained on historical student data. The models analyze:\n\n• Academic marks across subjects\n• Attendance rates\n• Assignment completion\n• Performance trends\n• Class participation\n\nTypical accuracy: 80-90%\n\nPredictions provide probability scores to help educators identify students who may need support. They should be used as one tool among many for decision-making.`;
    }

    if (lowerMessage.includes('factor') || lowerMessage.includes('indicator') || lowerMessage.includes('cause')) {
      return `Key risk factors identified by the model:\n\n🔴 **High Risk Indicators:**\n• Average marks < 40%\n• Attendance < 60%\n• Declining performance trend\n• Low assignment completion (<50%)\n\n🟡 **Moderate Risk Indicators:**\n• Marks between 40-50%\n• Attendance 60-75%\n• Inconsistent performance\n\n🟢 **Positive Indicators:**\n• Marks > 70%\n• Attendance > 85%\n• Improving trends\n• High engagement`;
    }

    if (lowerMessage.includes('recommend') || lowerMessage.includes('suggest') || lowerMessage.includes('strategy')) {
      const atRiskPct = predictionResults?.at_risk_percentage || 0;
      
      if (atRiskPct > 50) {
        return `🚨 **CRITICAL SITUATION**: Over 50% of students at risk.\n\n**Immediate Actions:**\n1. Emergency staff meeting to review situation\n2. Class-wide diagnostic assessment\n3. Implement intensive support program\n4. Review teaching methods and curriculum\n5. Engage parents with urgent communication\n6. Consider additional resources and tutoring\n\nThis requires systemic intervention, not just individual support.`;
      } else if (atRiskPct > 30) {
        return `⚠️ **HIGH ALERT**: Significant portion at risk.\n\n**Recommended Actions:**\n1. Form student support team\n2. Develop targeted intervention plans\n3. Increase parent-teacher communication\n4. Implement peer tutoring program\n5. Schedule regular progress reviews\n6. Provide additional learning resources\n\nFocus on both individual and small-group interventions.`;
      } else {
        return `✅ **MANAGEABLE SITUATION**: Focus on individual students.\n\n**Recommended Actions:**\n1. Schedule one-on-one meetings with at-risk students\n2. Create personalized learning plans\n3. Monitor progress weekly\n4. Maintain open communication with parents\n5. Celebrate small wins to build confidence\n6. Connect students with appropriate resources\n\nEarly identification gives you time for effective intervention!`;
      }
    }

    if (lowerMessage.includes('class') || lowerMessage.includes('overall') || lowerMessage.includes('summary')) {
      const total = predictionResults?.total_students || 0;
      const atRisk = predictionResults?.at_risk_count || 0;
      const safe = total - atRisk;
      return `📊 **Class Overview:**\n\n• Total Students: ${total}\n• At Risk: ${atRisk} students\n• Not at Risk: ${safe} students\n• Risk Percentage: ${predictionResults?.at_risk_percentage?.toFixed(1) || 0}%\n\nThe predictions help you identify which students need immediate attention. Focus your resources on the at-risk group while maintaining support for others.`;
    }

    if (lowerMessage.includes('how to use') || lowerMessage.includes('how do i')) {
      return `📖 **How to Use This System:**\n\n1. **Review Results**: Check the predictions table for at-risk students\n2. **Detailed Analysis**: Click on individual students to see risk factors\n3. **Action Items**: Note the recommendations for each student\n4. **Track Progress**: Re-upload data periodically to monitor improvements\n5. **Ask Questions**: Use this chatbot to get insights and advice\n\nRemember: Predictions are tools to guide decisions, not replace professional judgment.`;
    }

    return `I'm here to help you understand student performance predictions and provide guidance on interventions.\n\n**You can ask me about:**\n• Why specific students are at risk\n• What interventions work best\n• How to improve attendance or marks\n• Understanding the prediction model\n• Class-level statistics and recommendations\n• Specific risk factors and indicators\n\n**Try asking:**\n• "Why are students at risk?"\n• "What interventions do you recommend?"\n• "How can I improve attendance?"\n• "Tell me about the at-risk students"\n• "What factors indicate risk?"\n\nWhat would you like to know?`;
  };

  const handleSuggestedQuestion = (question) => {
    setChatMessage(question);
  };

  const toggleChat = () => {
    setIsOpen(!isOpen);
    if (!isOpen && chatHistory.length === 0) {
      const welcomeMessage = {
        role: 'assistant',
        content: `👋 Hi! I'm your AI teaching assistant. I can help you understand the student performance predictions and suggest interventions.\n\nWhat would you like to know?`,
        timestamp: new Date()
      };
      setChatHistory([welcomeMessage]);
    }
  };

  const clearChat = () => {
    setChatHistory([]);
    const welcomeMessage = {
      role: 'assistant',
      content: `Chat cleared! How can I help you?`,
      timestamp: new Date()
    };
    setChatHistory([welcomeMessage]);
  };

  return (
    <div className={`chatbot-widget ${isOpen ? 'open' : 'closed'}`}>
      {!isOpen && (
        <button className="chatbot-toggle-button" onClick={toggleChat}>
          <span className="chat-icon">💬</span>
          <span className="chat-label">AI Assistant</span>
        </button>
      )}

      {isOpen && (
        <div className="chatbot-window">
          <div className="chatbot-header">
            <div className="chatbot-header-content">
              <span className="chatbot-icon">🤖</span>
              <div className="chatbot-title">
                <h3>AI Teaching Assistant</h3>
                <span className="chatbot-status">● Online</span>
              </div>
            </div>
            <div className="chatbot-actions">
              <button className="chatbot-action-btn" onClick={clearChat} title="Clear chat">
                🗑️
              </button>
              <button className="chatbot-action-btn" onClick={toggleChat} title="Close">
                ✕
              </button>
            </div>
          </div>

          <div className="chatbot-messages">
            {chatHistory.length === 0 ? (
              <div className="chat-welcome">
                <div className="welcome-icon">👋</div>
                <h3>How can I assist you?</h3>
                <p>Ask me about student predictions, interventions, or teaching strategies.</p>
                
                <div className="suggested-questions">
                  <button onClick={() => handleSuggestedQuestion('Why are students at risk?')}>
                    Why are students at risk?
                  </button>
                  <button onClick={() => handleSuggestedQuestion('What interventions do you recommend?')}>
                    Recommended interventions?
                  </button>
                  <button onClick={() => handleSuggestedQuestion('Tell me about the at-risk students')}>
                    At-risk student details
                  </button>
                  <button onClick={() => handleSuggestedQuestion('How can I improve class performance?')}>
                    Improve performance
                  </button>
                </div>
              </div>
            ) : (
              <>
                {chatHistory.map((msg, idx) => (
                  <div key={idx} className={`chat-message ${msg.role}`}>
                    <div className="message-avatar">
                      {msg.role === 'user' ? '👤' : '🤖'}
                    </div>
                    <div className="message-bubble">
                      <div className="message-content">
                        {msg.content.split('\n').map((line, i) => (
                          <React.Fragment key={i}>
                            {line}
                            {i < msg.content.split('\n').length - 1 && <br />}
                          </React.Fragment>
                        ))}
                      </div>
                      <div className="message-time">
                        {msg.timestamp?.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                      </div>
                    </div>
                  </div>
                ))}
                {isTyping && (
                  <div className="chat-message assistant">
                    <div className="message-avatar">🤖</div>
                    <div className="message-bubble typing">
                      <div className="typing-indicator">
                        <span></span>
                        <span></span>
                        <span></span>
                      </div>
                    </div>
                  </div>
                )}
                <div ref={chatEndRef} />
              </>
            )}
          </div>

          <form onSubmit={handleChatSubmit} className="chatbot-input-form">
            <input
              type="text"
              value={chatMessage}
              onChange={(e) => setChatMessage(e.target.value)}
              placeholder="Type your question here..."
              className="chatbot-input"
              disabled={isTyping}
            />
            <button 
              type="submit" 
              className="chatbot-send-button"
              disabled={!chatMessage.trim() || isTyping}
            >
              ➤
            </button>
          </form>
        </div>
      )}
    </div>
  );
};

export default Chatbot;
