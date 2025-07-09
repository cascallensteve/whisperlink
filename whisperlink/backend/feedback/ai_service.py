import requests
import json
from django.conf import settings


class TogetherAIService:
    def __init__(self):
        self.api_key = settings.TOGETHER_API_KEY
        self.base_url = "https://api.together.xyz/v1/chat/completions"
        
    def generate_feedback(self, user_input, recipient_name):
        """
        Generate polished feedback from user's raw thoughts using Together AI
        """
        if not self.api_key or self.api_key == "your-together-api-key-here":
            # Fallback to original input if API key not configured
            return user_input
        
        prompt = f"""
        You are an expert feedback coach helping someone give constructive, comprehensive feedback to {recipient_name}.
        
        Raw feedback provided: "{user_input}"
        
        Transform this into a well-structured, comprehensive feedback that includes:
        
        1. **Positive Recognition**: Start with what they do well or their strengths
        2. **Specific Observations**: Detailed, concrete examples of behaviors or actions
        3. **Impact Statement**: How their actions affect others or the situation
        4. **Growth Opportunities**: Specific areas for development with actionable suggestions
        5. **Encouragement**: End with support and confidence in their potential
        
        Format the feedback with clear structure using paragraph breaks. Make it:
        - Comprehensive and detailed (aim for 3-4 substantial paragraphs)
        - Professional yet warm and human
        - Specific with concrete examples when possible
        - Balanced between appreciation and growth areas
        - Actionable with clear next steps
        - Encouraging and supportive
        
        Return only the enhanced feedback message with proper paragraph spacing.
        """
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert feedback coach and communication specialist. Your role is to help people transform raw, unstructured feedback into comprehensive, professional, and constructive messages that promote growth and maintain positive relationships."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 1000,
            "temperature": 0.7
        }
        
        try:
            response = requests.post(self.base_url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            generated_text = result['choices'][0]['message']['content'].strip()
            
            # Ensure the generated text is not empty
            if generated_text:
                return generated_text
            else:
                return user_input
                
        except requests.exceptions.RequestException as e:
            print(f"Error calling Together AI API: {e}")
            return user_input
        except (KeyError, IndexError) as e:
            print(f"Error parsing API response: {e}")
            return user_input
        except Exception as e:
            print(f"Unexpected error: {e}")
            return user_input


# Initialize the service
ai_service = TogetherAIService()
