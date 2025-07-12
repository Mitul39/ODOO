from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from bson import ObjectId
from src.models.user import get_db, User

skill_suggestion_bp = Blueprint('skill_suggestion', __name__)

# Skill categories and related skills
SKILL_CATEGORIES = {
    'Programming': {
        'skills': ['Python', 'JavaScript', 'Java', 'C++', 'React', 'Node.js', 'Django', 'Flask', 'Angular', 'Vue.js', 'TypeScript', 'Go', 'Rust', 'Swift', 'Kotlin'],
        'related_domains': ['Web Development', 'Mobile Development', 'Data Science', 'Machine Learning']
    },
    'Web Development': {
        'skills': ['HTML', 'CSS', 'JavaScript', 'React', 'Angular', 'Vue.js', 'Node.js', 'Express.js', 'MongoDB', 'PostgreSQL', 'MySQL', 'Bootstrap', 'Tailwind CSS', 'Sass', 'Webpack'],
        'related_domains': ['Programming', 'UI/UX Design', 'Mobile Development']
    },
    'Data Science': {
        'skills': ['Python', 'R', 'SQL', 'Pandas', 'NumPy', 'Matplotlib', 'Seaborn', 'Jupyter', 'Tableau', 'Power BI', 'Excel', 'Statistics', 'Data Visualization'],
        'related_domains': ['Programming', 'Machine Learning', 'Business Analytics']
    },
    'Machine Learning': {
        'skills': ['Python', 'TensorFlow', 'PyTorch', 'Scikit-learn', 'Keras', 'Deep Learning', 'Neural Networks', 'Computer Vision', 'NLP', 'Data Preprocessing'],
        'related_domains': ['Programming', 'Data Science', 'AI']
    },
    'Design': {
        'skills': ['Photoshop', 'Illustrator', 'Figma', 'Sketch', 'InDesign', 'After Effects', 'Premiere Pro', 'UI Design', 'UX Design', 'Graphic Design', 'Logo Design'],
        'related_domains': ['Web Development', 'Marketing', 'Branding']
    },
    'UI/UX Design': {
        'skills': ['Figma', 'Sketch', 'Adobe XD', 'Prototyping', 'Wireframing', 'User Research', 'Usability Testing', 'Design Systems', 'Information Architecture'],
        'related_domains': ['Design', 'Web Development', 'Mobile Development']
    },
    'Mobile Development': {
        'skills': ['React Native', 'Flutter', 'Swift', 'Kotlin', 'Java', 'Objective-C', 'Xamarin', 'Ionic', 'Android Studio', 'Xcode'],
        'related_domains': ['Programming', 'Web Development', 'UI/UX Design']
    },
    'Digital Marketing': {
        'skills': ['SEO', 'SEM', 'Google Ads', 'Facebook Ads', 'Content Marketing', 'Email Marketing', 'Social Media Marketing', 'Analytics', 'Copywriting'],
        'related_domains': ['Business', 'Content Creation', 'Analytics']
    },
    'Business': {
        'skills': ['Project Management', 'Business Analysis', 'Strategy', 'Leadership', 'Communication', 'Negotiation', 'Sales', 'Customer Service', 'Operations'],
        'related_domains': ['Digital Marketing', 'Finance', 'Management']
    },
    'Content Creation': {
        'skills': ['Writing', 'Copywriting', 'Video Editing', 'Photography', 'Blogging', 'Podcasting', 'YouTube', 'Content Strategy', 'Storytelling'],
        'related_domains': ['Digital Marketing', 'Design', 'Social Media']
    },
    'Languages': {
        'skills': ['English', 'Spanish', 'French', 'German', 'Chinese', 'Japanese', 'Korean', 'Italian', 'Portuguese', 'Arabic', 'Hindi', 'Russian'],
        'related_domains': ['Communication', 'Culture', 'Travel']
    },
    'Music': {
        'skills': ['Guitar', 'Piano', 'Violin', 'Drums', 'Singing', 'Music Theory', 'Music Production', 'Audio Engineering', 'Songwriting', 'DJ'],
        'related_domains': ['Audio', 'Performance', 'Creative Arts']
    },
    'Fitness': {
        'skills': ['Yoga', 'Pilates', 'Weight Training', 'Cardio', 'Nutrition', 'Personal Training', 'CrossFit', 'Running', 'Swimming', 'Martial Arts'],
        'related_domains': ['Health', 'Wellness', 'Sports']
    },
    'Cooking': {
        'skills': ['Baking', 'Italian Cuisine', 'Asian Cuisine', 'Vegetarian Cooking', 'Vegan Cooking', 'Grilling', 'Pastry', 'Wine Pairing', 'Food Photography'],
        'related_domains': ['Nutrition', 'Culture', 'Photography']
    }
}

def categorize_skill(skill):
    """Find the category for a given skill"""
    skill_lower = skill.lower()
    for category, data in SKILL_CATEGORIES.items():
        for cat_skill in data['skills']:
            if skill_lower in cat_skill.lower() or cat_skill.lower() in skill_lower:
                return category
    return 'Other'

def get_related_skills(user_skills):
    """Get related skills based on user's current skills"""
    user_categories = set()
    related_skills = set()
    
    # Find categories for user's skills
    for skill in user_skills:
        category = categorize_skill(skill)
        if category != 'Other':
            user_categories.add(category)
    
    # Get related skills from same and related categories
    for category in user_categories:
        if category in SKILL_CATEGORIES:
            # Add skills from same category
            for skill in SKILL_CATEGORIES[category]['skills']:
                if skill.lower() not in [s.lower() for s in user_skills]:
                    related_skills.add(skill)
            
            # Add skills from related domains
            for related_domain in SKILL_CATEGORIES[category]['related_domains']:
                if related_domain in SKILL_CATEGORIES:
                    for skill in SKILL_CATEGORIES[related_domain]['skills'][:3]:  # Limit to 3 per related domain
                        if skill.lower() not in [s.lower() for s in user_skills]:
                            related_skills.add(skill)
    
    return list(related_skills)

@skill_suggestion_bp.route('/skill-suggestions/<user_id>', methods=['GET'])
@jwt_required()
def get_skill_suggestions(user_id):
    try:
        current_user_id = get_jwt_identity()
        
        # Check if user is requesting their own suggestions
        if current_user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        user = User.find_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Get related skills based on what user wants to learn
        related_skills = get_related_skills(user.skills_learn)
        
        # Get trending skills from the platform
        db = get_db()
        trending_skills = []
        
        if db is not None:
            # Find most popular skills being taught
            pipeline = [
                {'$unwind': '$skills_teach'},
                {'$group': {'_id': '$skills_teach', 'count': {'$sum': 1}}},
                {'$sort': {'count': -1}},
                {'$limit': 10}
            ]
            
            popular_skills = list(db.users.aggregate(pipeline))
            trending_skills = [skill['_id'] for skill in popular_skills 
                             if skill['_id'].lower() not in [s.lower() for s in user.skills_learn]]
        
        # Get skills from users with similar interests
        similar_user_skills = []
        if db is not None:
            # Find users with overlapping skills_learn
            similar_users = db.users.find({
                'skills_learn': {'$in': user.skills_learn},
                '_id': {'$ne': ObjectId(user_id)},
                'is_public': True
            }).limit(10)
            
            for similar_user in similar_users:
                for skill in similar_user.get('skills_learn', []):
                    if skill.lower() not in [s.lower() for s in user.skills_learn]:
                        similar_user_skills.append(skill)
        
        # Remove duplicates and limit results
        related_skills = list(set(related_skills))[:15]
        trending_skills = list(set(trending_skills))[:10]
        similar_user_skills = list(set(similar_user_skills))[:10]
        
        # Create categorized suggestions
        suggestions = {
            'related_skills': {
                'title': 'Skills Related to Your Interests',
                'description': 'Based on what you want to learn',
                'skills': related_skills
            },
            'trending_skills': {
                'title': 'Trending Skills',
                'description': 'Popular skills on the platform',
                'skills': trending_skills
            },
            'similar_users': {
                'title': 'What Similar Users Are Learning',
                'description': 'Skills popular among users with similar interests',
                'skills': similar_user_skills
            }
        }
        
        return jsonify({
            'success': True,
            'suggestions': suggestions
        }), 200
        
    except Exception as e:
        print(f"Get skill suggestions error: {str(e)}")
        return jsonify({'error': 'Failed to fetch skill suggestions'}), 500

@skill_suggestion_bp.route('/skill-categories', methods=['GET'])
def get_skill_categories():
    try:
        # Return available skill categories
        categories = []
        for category, data in SKILL_CATEGORIES.items():
            categories.append({
                'name': category,
                'skills': data['skills'],
                'related_domains': data['related_domains']
            })
        
        return jsonify({
            'success': True,
            'categories': categories
        }), 200
        
    except Exception as e:
        print(f"Get skill categories error: {str(e)}")
        return jsonify({'error': 'Failed to fetch skill categories'}), 500

@skill_suggestion_bp.route('/skills/search', methods=['GET'])
def search_skills():
    try:
        query = request.args.get('q', '').lower()
        if not query:
            return jsonify({'error': 'Query parameter is required'}), 400
        
        # Search through all skills
        matching_skills = []
        for category, data in SKILL_CATEGORIES.items():
            for skill in data['skills']:
                if query in skill.lower():
                    matching_skills.append({
                        'skill': skill,
                        'category': category
                    })
        
        # Also search in database for user-defined skills
        db = get_db()
        if db is not None:
            # Search in skills_teach
            teach_pipeline = [
                {'$unwind': '$skills_teach'},
                {'$match': {'skills_teach': {'$regex': query, '$options': 'i'}}},
                {'$group': {'_id': '$skills_teach', 'count': {'$sum': 1}}},
                {'$sort': {'count': -1}},
                {'$limit': 10}
            ]
            
            teach_skills = list(db.users.aggregate(teach_pipeline))
            for skill_data in teach_skills:
                skill = skill_data['_id']
                if not any(s['skill'].lower() == skill.lower() for s in matching_skills):
                    matching_skills.append({
                        'skill': skill,
                        'category': 'User Defined',
                        'popularity': skill_data['count']
                    })
        
        # Sort by relevance (exact matches first, then partial matches)
        exact_matches = [s for s in matching_skills if s['skill'].lower() == query]
        partial_matches = [s for s in matching_skills if s['skill'].lower() != query]
        
        sorted_skills = exact_matches + partial_matches
        
        return jsonify({
            'success': True,
            'skills': sorted_skills[:20]  # Limit to 20 results
        }), 200
        
    except Exception as e:
        print(f"Search skills error: {str(e)}")
        return jsonify({'error': 'Failed to search skills'}), 500

@skill_suggestion_bp.route('/skills/popular', methods=['GET'])
def get_popular_skills():
    try:
        db = get_db()
        if db is None:
            return jsonify({'error': 'Database not available'}), 500
        
        # Get most popular skills being taught
        teach_pipeline = [
            {'$unwind': '$skills_teach'},
            {'$group': {'_id': '$skills_teach', 'teachers': {'$sum': 1}}},
            {'$sort': {'teachers': -1}},
            {'$limit': 20}
        ]
        
        # Get most popular skills being learned
        learn_pipeline = [
            {'$unwind': '$skills_learn'},
            {'$group': {'_id': '$skills_learn', 'learners': {'$sum': 1}}},
            {'$sort': {'learners': -1}},
            {'$limit': 20}
        ]
        
        popular_teach = list(db.users.aggregate(teach_pipeline))
        popular_learn = list(db.users.aggregate(learn_pipeline))
        
        # Format response
        teach_skills = []
        for skill in popular_teach:
            teach_skills.append({
                'skill': skill['_id'],
                'teachers': skill['teachers'],
                'category': categorize_skill(skill['_id'])
            })
        
        learn_skills = []
        for skill in popular_learn:
            learn_skills.append({
                'skill': skill['_id'],
                'learners': skill['learners'],
                'category': categorize_skill(skill['_id'])
            })
        
        return jsonify({
            'success': True,
            'popular_skills': {
                'most_taught': teach_skills,
                'most_wanted': learn_skills
            }
        }), 200
        
    except Exception as e:
        print(f"Get popular skills error: {str(e)}")
        return jsonify({'error': 'Failed to fetch popular skills'}), 500

