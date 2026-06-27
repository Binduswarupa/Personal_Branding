"""
============================================
Branding Score Routes
LinkedIn Branding Assistant
============================================
"""

from flask import Blueprint, request, jsonify
from groq import Groq
import json
from config import Config
from routes.auth import token_required
from models.user import UserModel
from models.branding import BrandingModel

branding_bp = Blueprint('branding', __name__)

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

@branding_bp.route('/score', methods=['POST'])
@token_required
def calculate_branding_score(current_user):
    """Calculate comprehensive branding score with weighted average."""
    try:
        data = request.get_json()
        headline = data.get('headline', '')
        about = data.get('about', '')
        skills = data.get('skills', '')
        experience = data.get('experience', '')
        projects = data.get('projects', '')
        education = data.get('education', '')
        posts_count = current_user.get('posts_generated', 0)

        prompt = f"""Calculate a LinkedIn branding score.
HEADLINE: {headline}
ABOUT: {about}
SKILLS: {skills}
EXPERIENCE: {experience}
PROJECTS: {projects}
EDUCATION: {education}
POSTS GENERATED: {posts_count}

Return JSON only:
{{"overall_score": <0-100>,
"categories": {{
  "profile_completeness": {{"score": <0-100>, "weight": 0.3, "details": ""}},
  "skills_relevance": {{"score": <0-100>, "weight": 0.2, "details": ""}},
  "content_activity": {{"score": <0-100>, "weight": 0.2, "details": ""}},
  "keyword_optimization": {{"score": <0-100>, "weight": 0.15, "details": ""}},
  "professional_presence": {{"score": <0-100>, "weight": 0.15, "details": ""}}
}},
"recommendations": [],
"quick_wins": [],
"long_term_goals": []
}}"""

        client = get_groq_client()
        completion = client.chat.completions.create(
            model=Config.GROQ_MODEL,
            messages=[
                {"role": "system", "content": "LinkedIn branding expert. JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7, max_tokens=2000
        )
        result = parse_ai_response(completion.choices[0].message.content)

        # Save branding report
        BrandingModel.save_report(
            str(current_user['_id']),
            {'headline': headline, 'about': about, 'skills': skills,
             'experience': experience, 'projects': projects, 'education': education},
            result.get('overall_score', 0),
            result.get('recommendations', []),
            result.get('categories', {})
        )
        UserModel.update_branding_score(str(current_user['_id']), result.get('overall_score', 0))

        return jsonify({'message': 'Branding score calculated', 'result': result}), 200
    except Exception as e:
        return jsonify({'error': f'Branding score calculation failed: {str(e)}'}), 500

@branding_bp.route('/latest-report', methods=['GET'])
@token_required
def get_latest_report(current_user):
    """Get the latest branding report."""
    try:
        report = BrandingModel.get_latest_report(str(current_user['_id']))
        if report:
            report['_id'] = str(report['_id'])
            report['user_id'] = str(report['user_id'])
            report['created_at'] = str(report.get('created_at', ''))
        return jsonify({'report': report}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
