"""
============================================
History Routes
LinkedIn Branding Assistant
============================================
"""

from flask import Blueprint, request, jsonify
from routes.auth import token_required
from models.branding import BrandingModel

history_bp = Blueprint('history', __name__)

@history_bp.route('/', methods=['GET'])
@token_required
def get_history(current_user):
    """Get full generation history for the current user."""
    try:
        limit = request.args.get('limit', 50, type=int)
        history = BrandingModel.get_full_history(str(current_user['_id']), limit)

        # Convert datetime objects to strings
        for item in history:
            if item.get('created_at'):
                item['created_at'] = str(item['created_at'])

        return jsonify({'history': history}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@history_bp.route('/<item_type>/<item_id>', methods=['DELETE'])
@token_required
def delete_history_item(current_user, item_type, item_id):
    """Delete a specific history item."""
    try:
        success = BrandingModel.delete_history_item(
            str(current_user['_id']), item_id, item_type
        )
        if success:
            return jsonify({'message': 'Item deleted successfully'}), 200
        return jsonify({'error': 'Item not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@history_bp.route('/posts', methods=['GET'])
@token_required
def get_posts_history(current_user):
    """Get posts history."""
    try:
        posts = BrandingModel.get_user_posts(str(current_user['_id']))
        for p in posts:
            p['_id'] = str(p['_id'])
            p['user_id'] = str(p['user_id'])
            if p.get('created_at'):
                p['created_at'] = str(p['created_at'])
        return jsonify({'posts': posts}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@history_bp.route('/headlines', methods=['GET'])
@token_required
def get_headlines_history(current_user):
    """Get headlines history."""
    try:
        headlines = BrandingModel.get_user_headlines(str(current_user['_id']))
        for h in headlines:
            h['_id'] = str(h['_id'])
            h['user_id'] = str(h['user_id'])
            if h.get('created_at'):
                h['created_at'] = str(h['created_at'])
        return jsonify({'headlines': headlines}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@history_bp.route('/stats', methods=['GET'])
@token_required
def get_stats(current_user):
    """Get user statistics for dashboard."""
    try:
        user_id = str(current_user['_id'])
        posts_count = BrandingModel.get_posts_count(user_id)
        latest_report = BrandingModel.get_latest_report(user_id)

        stats = {
            'posts_generated': posts_count,
            'branding_score': current_user.get('branding_score', 0),
            'headlines_generated': len(BrandingModel.get_user_headlines(user_id)),
            'abouts_generated': len(BrandingModel.get_user_abouts(user_id)),
            'reports_generated': len(BrandingModel.get_all_reports(user_id)),
            'latest_report_score': latest_report.get('score', 0) if latest_report else 0,
            'profile_completion': _calculate_profile_completion(current_user)
        }
        return jsonify({'stats': stats}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def _calculate_profile_completion(user):
    """Calculate profile completion percentage."""
    profile = user.get('profile_data', {})
    fields = ['headline', 'about', 'skills', 'experience', 'projects', 'education']
    filled = 0
    for field in fields:
        value = profile.get(field, '')
        if isinstance(value, list) and len(value) > 0:
            filled += 1
        elif isinstance(value, str) and value.strip():
            filled += 1
    # Also count career_goal and name
    if user.get('career_goal', '').strip():
        filled += 1
    if user.get('name', '').strip():
        filled += 1
    return int((filled / 8) * 100)
