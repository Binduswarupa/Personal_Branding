"""
============================================
Profile Analysis Routes
LinkedIn Branding Assistant
============================================
"""

from flask import Blueprint, request, jsonify
from groq import Groq
import json
from config import Config
from routes.auth import token_required
from models.user import UserModel

profile_bp = Blueprint('profile', __name__)

def get_groq_client():
    return Groq(api_key=Config.GROQ_API_KEY)

def parse_ai_response(text):
    """Parse AI response, stripping markdown code fences if present."""
    text = text.strip()
    if text.startswith('```'):
        text = text.split('```')[1]
        if text.startswith('json'):
            text = text[4:]
        text = text.strip()
    return json.loads(text)

@profile_bp.route('/analyze', methods=['POST'])
@token_required
def analyze_profile(current_user):
    try:
        data = request.get_json()
        headline = data.get('headline', '')
        about = data.get('about', '')
        skills = data.get('skills', '')
        experience = data.get('experience', '')
        projects = data.get('projects', '')
        education = data.get('education', '')

        prompt = f"""Analyze this LinkedIn profile. Return JSON only:
HEADLINE: {headline}
ABOUT: {about}
SKILLS: {skills}
EXPERIENCE: {experience}
PROJECTS: {projects}
EDUCATION: {education}

Return this JSON structure:
{{"overall_score":<0-100>,"breakdown":{{"completeness":<0-100>,"professionalism":<0-100>,"recruiter_visibility":<0-100>,"keyword_optimization":<0-100>,"content_quality":<0-100>}},"missing_sections":[],"strengths":[],"suggestions":[],"improvement_roadmap":[{{"priority":"high/medium/low","action":"","impact":""}}],"keyword_suggestions":[],"recruiter_tips":[]}}"""

        client = get_groq_client()
        completion = client.chat.completions.create(
            model=Config.GROQ_MODEL,
            messages=[
                {"role": "system", "content": "Expert LinkedIn profile analyzer. Respond with valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7, max_tokens=2000
        )
        analysis = parse_ai_response(completion.choices[0].message.content)

        profile_data = {
            'headline': headline, 'about': about,
            'skills': skills.split(',') if isinstance(skills, str) else skills,
            'experience': experience, 'projects': projects, 'education': education
        }
        UserModel.update_profile(str(current_user['_id']), profile_data)
        UserModel.update_branding_score(str(current_user['_id']), analysis.get('overall_score', 0))

        return jsonify({'message': 'Profile analysis complete', 'analysis': analysis}), 200
    except Exception as e:
        return jsonify({'error': f'Profile analysis failed: {str(e)}'}), 500

@profile_bp.route('/resume-analyze', methods=['POST'])
@token_required
def analyze_resume(current_user):
    try:
        data = request.get_json()
        resume_text = data.get('resume_text', '')
        target_role = data.get('target_role', '')
        if not resume_text:
            return jsonify({'error': 'Resume text is required'}), 400

        prompt = f"""Analyze this resume for ATS compatibility. TARGET ROLE: {target_role}
RESUME: {resume_text}
Return JSON: {{"ats_score":<0-100>,"format_score":<0-100>,"keyword_match_score":<0-100>,"content_score":<0-100>,"missing_keywords":[],"format_issues":[],"strengths":[],"improvements":[],"linkedin_suggestions":[],"overall_feedback":""}}"""

        client = get_groq_client()
        completion = client.chat.completions.create(
            model=Config.GROQ_MODEL,
            messages=[
                {"role": "system", "content": "Expert ATS resume analyzer. JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7, max_tokens=2000
        )
        analysis = parse_ai_response(completion.choices[0].message.content)
        return jsonify({'message': 'Resume analysis complete', 'analysis': analysis}), 200
    except Exception as e:
        return jsonify({'error': f'Resume analysis failed: {str(e)}'}), 500

@profile_bp.route('/career-roadmap', methods=['POST'])
@token_required
def generate_career_roadmap(current_user):
    try:
        data = request.get_json()
        prompt = f"""Create career roadmap. CURRENT: {data.get('current_role','')} TARGET: {data.get('target_role','')} SKILLS: {data.get('skills','')} EXP: {data.get('experience_years',0)} years
Return JSON: {{"current_assessment":"","target_analysis":"","skill_gap":[],"roadmap":[{{"phase":"Phase 1","title":"","actions":[],"skills_to_learn":[],"linkedin_strategy":""}}],"linkedin_content_plan":[{{"week":1,"topic":"","post_type":"","purpose":""}}],"recruiter_visibility_tips":[],"networking_strategy":"","estimated_timeline":""}}"""

        client = get_groq_client()
        completion = client.chat.completions.create(
            model=Config.GROQ_MODEL,
            messages=[
                {"role": "system", "content": "Expert career coach. JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7, max_tokens=3000
        )
        roadmap = parse_ai_response(completion.choices[0].message.content)
        return jsonify({'message': 'Career roadmap generated', 'roadmap': roadmap}), 200
    except Exception as e:
        return jsonify({'error': f'Career roadmap generation failed: {str(e)}'}), 500

@profile_bp.route('/recruiter-visibility', methods=['POST'])
@token_required
def predict_recruiter_visibility(current_user):
    try:
        data = request.get_json()
        prompt = f"""Analyze recruiter visibility. HEADLINE: {data.get('headline','')} ABOUT: {data.get('about','')} SKILLS: {data.get('skills','')} TARGET: {data.get('target_role','')}
Return JSON: {{"visibility_score":<0-100>,"search_appearance_estimate":"","top_keywords_found":[],"missing_keywords":[],"profile_rank_factors":{{"headline_strength":<0-100>,"skills_relevance":<0-100>,"experience_detail":<0-100>,"network_indicators":<0-100>}},"actionable_tips":[],"competitor_insight":""}}"""

        client = get_groq_client()
        completion = client.chat.completions.create(
            model=Config.GROQ_MODEL,
            messages=[
                {"role": "system", "content": "Recruiter visibility expert. JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7, max_tokens=2000
        )
        visibility = parse_ai_response(completion.choices[0].message.content)
        return jsonify({'message': 'Visibility analysis complete', 'visibility': visibility}), 200
    except Exception as e:
        return jsonify({'error': f'Visibility prediction failed: {str(e)}'}), 500
