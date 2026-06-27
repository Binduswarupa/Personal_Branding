"""
============================================
Content Generation Routes
LinkedIn Branding Assistant
============================================
Handles headline, about section, post, and hashtag generation.
"""

from flask import Blueprint, request, jsonify
from groq import Groq
import json
from config import Config
from routes.auth import token_required
from models.user import UserModel
from models.branding import BrandingModel

content_bp = Blueprint('content', __name__)

def get_groq_client():
    return Groq(api_key=Config.GROQ_API_KEY)

def parse_ai_response(text):
    text = text.strip()
    if text.startswith('```'):
        text = text.split('```')[1]
        if text.startswith('json'):
            text = text[4:]
        text = text.strip()
    return json.loads(text)

@content_bp.route('/generate-headlines', methods=['POST'])
@token_required
def generate_headlines(current_user):
    """Generate 10 recruiter-friendly LinkedIn headlines."""
    try:
        data = request.get_json()
        skills = data.get('skills', '')
        experience = data.get('experience', '')
        career_goal = data.get('career_goal', '')

        if not skills:
            return jsonify({'error': 'Skills are required'}), 400

        prompt = f"""Generate 10 recruiter-friendly LinkedIn headlines for a professional.
SKILLS: {skills}
EXPERIENCE: {experience}
CAREER GOAL: {career_goal}

Return JSON only:
{{"headlines": ["headline1", "headline2", ...], "tips": ["tip1", "tip2", "tip3"]}}

Make headlines compelling, keyword-rich, and optimized for LinkedIn search.
Include relevant emojis where appropriate. Each headline should be unique in style."""

        client = get_groq_client()
        completion = client.chat.completions.create(
            model=Config.GROQ_MODEL,
            messages=[
                {"role": "system", "content": "Expert LinkedIn headline writer. JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8, max_tokens=1500
        )
        result = parse_ai_response(completion.choices[0].message.content)

        # Save to history
        BrandingModel.save_headline(
            str(current_user['_id']),
            result.get('headlines', []),
            skills, experience, career_goal
        )

        return jsonify({'message': 'Headlines generated', 'result': result}), 200
    except Exception as e:
        return jsonify({'error': f'Headline generation failed: {str(e)}'}), 500

@content_bp.route('/generate-about', methods=['POST'])
@token_required
def generate_about(current_user):
    """Generate a professional LinkedIn About section."""
    try:
        data = request.get_json()
        skills = data.get('skills', '')
        education = data.get('education', '')
        career_goals = data.get('career_goals', '')
        projects = data.get('projects', '')
        experience = data.get('experience', '')
        tone = data.get('tone', 'professional')

        prompt = f"""Write a professional LinkedIn About section.
SKILLS: {skills}
EDUCATION: {education}
CAREER GOALS: {career_goals}
PROJECTS: {projects}
EXPERIENCE: {experience}
TONE: {tone}

Return JSON only:
{{"about_section": "<the complete about section text>", "word_count": <number>, "ats_keywords_used": [], "tips": []}}

Make it ATS-friendly, recruiter-friendly, compelling, and personal. Include relevant keywords naturally."""

        client = get_groq_client()
        completion = client.chat.completions.create(
            model=Config.GROQ_MODEL,
            messages=[
                {"role": "system", "content": "Expert LinkedIn copywriter. JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8, max_tokens=2000
        )
        result = parse_ai_response(completion.choices[0].message.content)

        # Save to history
        BrandingModel.save_about(
            str(current_user['_id']),
            result.get('about_section', ''),
            {'skills': skills, 'education': education, 'career_goals': career_goals,
             'projects': projects, 'experience': experience, 'tone': tone}
        )

        return jsonify({'message': 'About section generated', 'result': result}), 200
    except Exception as e:
        return jsonify({'error': f'About generation failed: {str(e)}'}), 500

@content_bp.route('/generate-post', methods=['POST'])
@token_required
def generate_post(current_user):
    """Generate a LinkedIn post based on category and length."""
    try:
        data = request.get_json()
        category = data.get('category', 'Career Growth')
        post_length = data.get('post_length', 'medium')
        topic = data.get('topic', '')
        tone = data.get('tone', 'professional')

        length_guide = {
            'short': '50-100 words',
            'medium': '150-250 words',
            'long': '300-500 words'
        }

        prompt = f"""Write a LinkedIn post.
CATEGORY: {category}
TOPIC: {topic if topic else category}
LENGTH: {length_guide.get(post_length, '150-250 words')}
TONE: {tone}

Return JSON only:
{{"post_content": "<the post with line breaks and formatting>", "emoji_suggestions": ["emoji1", "emoji2"], "cta_suggestions": ["cta1", "cta2"], "best_posting_time": "", "engagement_tips": []}}

Make it engaging, valuable, and optimized for LinkedIn algorithm. Include appropriate emojis and line breaks for readability."""

        client = get_groq_client()
        completion = client.chat.completions.create(
            model=Config.GROQ_MODEL,
            messages=[
                {"role": "system", "content": "Expert LinkedIn content creator. JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.85, max_tokens=2000
        )
        result = parse_ai_response(completion.choices[0].message.content)

        # Save to history and increment counter
        BrandingModel.save_post(
            str(current_user['_id']),
            result.get('post_content', ''),
            category, post_length
        )
        UserModel.increment_posts_count(str(current_user['_id']))

        return jsonify({'message': 'Post generated', 'result': result}), 200
    except Exception as e:
        return jsonify({'error': f'Post generation failed: {str(e)}'}), 500

@content_bp.route('/generate-hashtags', methods=['POST'])
@token_required
def generate_hashtags(current_user):
    """Generate trending, niche, and high-reach hashtags."""
    try:
        data = request.get_json()
        topic = data.get('topic', '')
        industry = data.get('industry', '')
        target_audience = data.get('target_audience', '')

        prompt = f"""Generate LinkedIn hashtags.
TOPIC: {topic}
INDUSTRY: {industry}
TARGET AUDIENCE: {target_audience}

Return JSON only:
{{"trending_hashtags": ["#hashtag1", "#hashtag2", ...], "niche_hashtags": ["#hashtag1", ...], "high_reach_hashtags": ["#hashtag1", ...], "recommended_combination": ["#hashtag1", ...], "usage_tips": []}}

Provide exactly 20 total hashtags across categories. Make them relevant and currently popular on LinkedIn."""

        client = get_groq_client()
        completion = client.chat.completions.create(
            model=Config.GROQ_MODEL,
            messages=[
                {"role": "system", "content": "LinkedIn hashtag strategy expert. JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8, max_tokens=1000
        )
        result = parse_ai_response(completion.choices[0].message.content)
        return jsonify({'message': 'Hashtags generated', 'result': result}), 200
    except Exception as e:
        return jsonify({'error': f'Hashtag generation failed: {str(e)}'}), 500

@content_bp.route('/content-calendar', methods=['POST'])
@token_required
def generate_content_calendar(current_user):
    """Generate a 30-day LinkedIn content calendar."""
    try:
        data = request.get_json()
        niche = data.get('niche', '')
        goals = data.get('goals', '')
        frequency = data.get('frequency', '5 posts per week')

        prompt = f"""Create a 30-day LinkedIn content calendar.
NICHE: {niche}
GOALS: {goals}
POSTING FREQUENCY: {frequency}

Return JSON only:
{{"calendar": [{{"day": 1, "type": "post/article/carousel/poll", "topic": "", "hook": "", "cta": "", "hashtags": [], "best_time": ""}}], "strategy_notes": "", "engagement_tactics": []}}

Make it strategic, varied, and optimized for growth. Include different content types."""

        client = get_groq_client()
        completion = client.chat.completions.create(
            model=Config.GROQ_MODEL,
            messages=[
                {"role": "system", "content": "LinkedIn content strategist. JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8, max_tokens=4000
        )
        result = parse_ai_response(completion.choices[0].message.content)
        return jsonify({'message': 'Content calendar generated', 'result': result}), 200
    except Exception as e:
        return jsonify({'error': f'Calendar generation failed: {str(e)}'}), 500
