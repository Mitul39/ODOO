from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from bson import ObjectId
from src.models.user import get_db, User

badge_bp = Blueprint('badge', __name__)

# Badge thresholds
BADGE_THRESHOLDS = {
    'Bronze': 0,
    'Silver': 10,
    'Gold': 25,
    'Platinum': 50
}

@badge_bp.route('/badges/leaderboard', methods=['GET'])
def get_leaderboard():
    try:
        db = get_db()
        if db is None:
            return jsonify({'error': 'Database not available'}), 500
        
        # Get top users by sessions taught
        pipeline = [
            {
                '$match': {
                    'is_public': True,
                    'total_sessions_taught': {'$gt': 0}
                }
            },
            {
                '$sort': {'total_sessions_taught': -1}
            },
            {
                '$limit': 50
            },
            {
                '$project': {
                    'name': 1,
                    'photo_url': 1,
                    'total_sessions_taught': 1,
                    'badge_level': 1,
                    'rating': 1,
                    'skills_teach': 1
                }
            }
        ]
        
        top_users = list(db.users.aggregate(pipeline))
        
        # Format response
        leaderboard = []
        for i, user in enumerate(top_users):
            user_data = {
                '_id': str(user['_id']),
                'rank': i + 1,
                'name': user['name'],
                'photo_url': user.get('photo_url', ''),
                'total_sessions_taught': user['total_sessions_taught'],
                'badge_level': user['badge_level'],
                'rating': user.get('rating', 0.0),
                'skills_teach': user.get('skills_teach', [])[:3]  # Show only first 3 skills
            }
            leaderboard.append(user_data)
        
        return jsonify({
            'success': True,
            'leaderboard': leaderboard
        }), 200
        
    except Exception as e:
        print(f"Get leaderboard error: {str(e)}")
        return jsonify({'error': 'Failed to fetch leaderboard'}), 500

@badge_bp.route('/badges/stats', methods=['GET'])
def get_badge_stats():
    try:
        db = get_db()
        if db is None:
            return jsonify({'error': 'Database not available'}), 500
        
        # Get badge distribution
        pipeline = [
            {
                '$group': {
                    '_id': '$badge_level',
                    'count': {'$sum': 1}
                }
            }
        ]
        
        badge_distribution = list(db.users.aggregate(pipeline))
        
        # Format badge distribution
        distribution = {
            'Bronze': 0,
            'Silver': 0,
            'Gold': 0,
            'Platinum': 0
        }
        
        for badge in badge_distribution:
            if badge['_id'] in distribution:
                distribution[badge['_id']] = badge['count']
        
        # Get total stats
        total_users = db.users.count_documents({'is_public': True})
        total_sessions = db.sessions.count_documents({'status': 'completed'})
        
        # Get most active users this month
        from datetime import datetime, timedelta
        start_of_month = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        monthly_active_pipeline = [
            {
                '$match': {
                    'scheduled_date': {'$gte': start_of_month},
                    'status': 'completed'
                }
            },
            {
                '$group': {
                    '_id': '$teacher_id',
                    'sessions_this_month': {'$sum': 1}
                }
            },
            {
                '$lookup': {
                    'from': 'users',
                    'localField': '_id',
                    'foreignField': '_id',
                    'as': 'user'
                }
            },
            {
                '$unwind': '$user'
            },
            {
                '$sort': {'sessions_this_month': -1}
            },
            {
                '$limit': 5
            }
        ]
        
        monthly_active = list(db.sessions.aggregate(monthly_active_pipeline))
        
        # Format monthly active users
        monthly_leaders = []
        for user in monthly_active:
            user_data = {
                '_id': str(user['user']['_id']),
                'name': user['user']['name'],
                'photo_url': user['user'].get('photo_url', ''),
                'sessions_this_month': user['sessions_this_month'],
                'badge_level': user['user']['badge_level']
            }
            monthly_leaders.append(user_data)
        
        return jsonify({
            'success': True,
            'stats': {
                'badge_distribution': distribution,
                'total_users': total_users,
                'total_sessions': total_sessions,
                'monthly_leaders': monthly_leaders,
                'badge_thresholds': BADGE_THRESHOLDS
            }
        }), 200
        
    except Exception as e:
        print(f"Get badge stats error: {str(e)}")
        return jsonify({'error': 'Failed to fetch badge stats'}), 500

@badge_bp.route('/badges/user/<user_id>', methods=['GET'])
def get_user_badges(user_id):
    try:
        user = User.find_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Calculate progress to next badge
        current_sessions = user.total_sessions_taught
        current_badge = user.badge_level
        
        # Find next badge level
        next_badge = None
        sessions_to_next = 0
        
        badge_levels = ['Bronze', 'Silver', 'Gold', 'Platinum']
        current_index = badge_levels.index(current_badge) if current_badge in badge_levels else 0
        
        if current_index < len(badge_levels) - 1:
            next_badge = badge_levels[current_index + 1]
            sessions_to_next = BADGE_THRESHOLDS[next_badge] - current_sessions
        
        # Get user's achievements
        achievements = []
        
        # Basic achievements
        if current_sessions >= 1:
            achievements.append({
                'title': 'First Session',
                'description': 'Completed your first teaching session',
                'icon': '🎯',
                'earned_at': user.created_at
            })
        
        if current_sessions >= 5:
            achievements.append({
                'title': 'Getting Started',
                'description': 'Taught 5 sessions',
                'icon': '🌟',
                'earned_at': user.created_at
            })
        
        if current_sessions >= 10:
            achievements.append({
                'title': 'Silver Teacher',
                'description': 'Reached Silver badge level',
                'icon': '🥈',
                'earned_at': user.created_at
            })
        
        if current_sessions >= 25:
            achievements.append({
                'title': 'Gold Teacher',
                'description': 'Reached Gold badge level',
                'icon': '🥇',
                'earned_at': user.created_at
            })
        
        if current_sessions >= 50:
            achievements.append({
                'title': 'Platinum Master',
                'description': 'Reached Platinum badge level',
                'icon': '💎',
                'earned_at': user.created_at
            })
        
        # Skill-based achievements
        if len(user.skills_teach) >= 5:
            achievements.append({
                'title': 'Multi-Skilled',
                'description': 'Teaching 5 or more skills',
                'icon': '🎨',
                'earned_at': user.created_at
            })
        
        return jsonify({
            'success': True,
            'badge_info': {
                'current_badge': current_badge,
                'next_badge': next_badge,
                'current_sessions': current_sessions,
                'sessions_to_next': sessions_to_next,
                'progress_percentage': min(100, (current_sessions / BADGE_THRESHOLDS.get(next_badge, current_sessions + 1)) * 100) if next_badge else 100,
                'achievements': achievements,
                'badge_thresholds': BADGE_THRESHOLDS
            }
        }), 200
        
    except Exception as e:
        print(f"Get user badges error: {str(e)}")
        return jsonify({'error': 'Failed to fetch user badges'}), 500

@badge_bp.route('/badges/update/<user_id>', methods=['POST'])
@jwt_required()
def update_user_badge(user_id):
    try:
        current_user_id = get_jwt_identity()
        
        # Check if user is updating their own badge or if it's an admin operation
        if current_user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        user = User.find_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Update badge level based on sessions taught
        old_badge = user.badge_level
        user.update_badge_level()
        user.save()
        
        new_badge = user.badge_level
        badge_upgraded = old_badge != new_badge
        
        return jsonify({
            'success': True,
            'message': 'Badge updated successfully',
            'old_badge': old_badge,
            'new_badge': new_badge,
            'badge_upgraded': badge_upgraded
        }), 200
        
    except Exception as e:
        print(f"Update user badge error: {str(e)}")
        return jsonify({'error': 'Failed to update badge'}), 500

