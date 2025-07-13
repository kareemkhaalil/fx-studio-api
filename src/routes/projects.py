from flask import Blueprint, jsonify
from src.services.notion_service import NotionService

projects_bp = Blueprint('projects', __name__)

@projects_bp.route('/projects', methods=['GET'])
def get_projects():
    """جلب جميع المشاريع من Notion"""
    notion_service = NotionService()
    result = notion_service.get_projects()
    
    if result['success']:
        return jsonify({
            'success': True,
            'projects': result['projects']
        })
    else:
        return jsonify({
            'success': False,
            'error': result['error']
        }), 500

@projects_bp.route('/projects/categories', methods=['GET'])
def get_categories():
    """جلب جميع التصنيفات المتاحة"""
    categories = [
        'إعلانات تجارية',
        'فيديوهات شركات',
        'رسوم متحركة',
        'حفلات زفاف',
        'تعليمي',
        'أخرى'
    ]
    
    return jsonify({
        'success': True,
        'categories': categories
    })

@projects_bp.route('/projects/tags', methods=['GET'])
def get_tags():
    """جلب جميع الوسوم المتاحة"""
    tags = [
        'موشن جرافيك',
        'تصوير احترافي',
        'تصوير جوي',
        'تصوير سينمائي',
        'محتوى رقمي',
        'مونتاج',
        'تصميم',
        'أخرى'
    ]
    
    return jsonify({
        'success': True,
        'tags': tags
    })

