"""
Wellness Service for Patient Dashboard
Provides motivational quotes, health tips, and mental health support content
"""
import random
from typing import List, Dict


class WellnessService:
    """Service for providing wellness content and support"""

    def __init__(self):
        """Initialize wellness service with content"""
        self.recovery_quotes = [
            "Healing is a process. Be patient with yourself. Every day is a step towards recovery.",
            "Your body has an amazing capacity to heal. Trust the process and take care of yourself.",
            "Recovery is not a destination, it's a journey. Celebrate small victories along the way.",
            "You are stronger than you think. Take it one day at a time.",
            "Mental health is just as important as physical health. Be kind to yourself during recovery.",
            "Focus on what you can control today. Tomorrow will take care of itself.",
            "Recovery requires rest, patience, and self-compassion. You've got this!",
            "Hope is a powerful medicine. Believe in your recovery.",
            "Your health is your wealth. Invest in yourself every single day.",
            "Progress, not perfection. Every small step counts in your recovery journey.",
            "The only impossible journey is the one you never begin. Start your recovery today.",
            "Believe in yourself and all that you are. You have the strength to recover.",
            "Take care of your body. It's the only place you have to live.",
            "Healing doesn't mean the damage never existed. It means the damage no longer controls our lives.",
            "You deserve to heal. You deserve to feel better. You deserve to be happy."
        ]

        self.health_tips = [
            "Stay hydrated - drink plenty of water throughout the day to support your recovery",
            "Follow your doctor's medication schedule strictly for optimal treatment outcomes",
            "Get adequate rest - aim for 7-8 hours of quality sleep each night",
            "Light exercise as recommended by your doctor can speed up recovery",
            "Maintain a positive mindset - it significantly impacts your physical healing",
            "Eat nutritious, balanced meals to support your body's healing process",
            "Avoid stress - practice deep breathing, meditation, or gentle yoga",
            "Keep track of your vital signs and report any concerns to your doctor",
            "Stay connected with loved ones - social support aids recovery",
            "Follow infection prevention measures to avoid complications",
            "Take breaks and don't push yourself too hard during recovery",
            "Maintain good hygiene to prevent hospital-acquired infections",
            "Keep your living environment clean and organized for better rest",
            "Limit screen time before bed to improve sleep quality",
            "Gradually increase activity as your doctor recommends"
        ]

        self.mental_health_tips = [
            "It's okay to feel anxious or worried about your health - these feelings are normal",
            "Practice mindfulness or meditation for 10 minutes daily to reduce stress",
            "Talk to someone you trust about how you're feeling - don't keep emotions bottled up",
            "Keep a gratitude journal - write 3 things you're grateful for daily",
            "Set small, achievable goals each day to build confidence and momentum",
            "Engage in hobbies or activities you enjoy when you feel up to it",
            "Limit news and social media consumption to reduce anxiety",
            "Practice positive self-talk - replace negative thoughts with constructive ones",
            "Consider talking to a therapist or counselor if anxiety becomes overwhelming",
            "Remember that recovery is not linear - ups and downs are normal",
            "Build a support network of friends, family, and healthcare providers",
            "Practice self-compassion - you're doing your best during a difficult time",
            "Engage in relaxation techniques like deep breathing or progressive muscle relaxation",
            "Maintain a sense of humor - laughter is therapeutic for recovery",
            "Give yourself permission to ask for help when you need it"
        ]

        self.coping_strategies = [
            {
                'title': 'Breathing Exercises',
                'description': 'Practice deep breathing: Inhale for 4 counts, hold for 4, exhale for 4'
            },
            {
                'title': 'Visualization',
                'description': 'Imagine yourself healthy and strong, going about your daily activities'
            },
            {
                'title': 'Progressive Muscle Relaxation',
                'description': 'Tense and relax different muscle groups to release physical tension'
            },
            {
                'title': 'Journaling',
                'description': 'Write down your thoughts, feelings, and recovery milestones'
            },
            {
                'title': 'Gratitude Practice',
                'description': 'Focus on things you\'re grateful for, even the small things'
            },
            {
                'title': 'Music Therapy',
                'description': 'Listen to calming or uplifting music to improve mood'
            },
            {
                'title': 'Art & Creativity',
                'description': 'Express yourself through drawing, painting, or other creative activities'
            },
            {
                'title': 'Gentle Stretching',
                'description': 'Do light stretches as approved by your physical therapist'
            }
        ]

    def get_wellness_quote(self) -> str:
        """Get a random recovery/wellness quote"""
        return random.choice(self.recovery_quotes)

    def get_daily_health_tips(self, num_tips: int = 5) -> List[str]:
        """
        Get random daily health tips

        Args:
            num_tips: Number of tips to return

        Returns:
            List of health tips
        """
        return random.sample(self.health_tips, min(num_tips, len(self.health_tips)))

    def get_mental_health_tips(self, num_tips: int = 5) -> List[str]:
        """
        Get random mental health and wellness tips

        Args:
            num_tips: Number of tips to return

        Returns:
            List of mental health tips
        """
        return random.sample(self.mental_health_tips, min(num_tips, len(self.mental_health_tips)))

    def get_combined_wellness_tips(self, num_tips: int = 5) -> List[str]:
        """
        Get combined physical and mental health tips

        Args:
            num_tips: Number of tips to return

        Returns:
            List of combined wellness tips
        """
        combined = self.health_tips + self.mental_health_tips
        return random.sample(combined, min(num_tips, len(combined)))

    def get_coping_strategies(self) -> List[Dict]:
        """Get list of coping strategies"""
        return self.coping_strategies

    def get_wellness_dashboard_data(self) -> Dict:
        """
        Get complete wellness data for dashboard

        Returns:
            Dictionary with quotes, tips, and strategies
        """
        return {
            'quote': self.get_wellness_quote(),
            'daily_tips': self.get_daily_health_tips(5),
            'mental_health_tips': self.get_mental_health_tips(3),
            'coping_strategies': random.sample(self.coping_strategies, 3),
            'reminder': 'Remember: Recovery is a journey, not a destination. Be patient and kind to yourself.'
        }

    def get_motivational_message(self, days_admitted: int) -> str:
        """
        Get motivational message based on recovery progress

        Args:
            days_admitted: Number of days patient has been in hospital

        Returns:
            Personalized motivational message
        """
        if days_admitted < 3:
            return "You're in the early stages of recovery. Focus on rest and following medical advice."
        elif days_admitted < 7:
            return "You're making progress! Keep up with your treatment and stay positive."
        elif days_admitted < 14:
            return "Great job! You're showing real improvement. Your strength is inspiring."
        else:
            return "You've come so far! Your resilience and determination are admirable. Keep moving forward!"


# Singleton instance
_wellness_service = None


def get_wellness_service() -> WellnessService:
    """Get or create wellness service instance"""
    global _wellness_service
    if _wellness_service is None:
        _wellness_service = WellnessService()
    return _wellness_service
