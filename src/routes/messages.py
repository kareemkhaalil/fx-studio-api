from flask import Blueprint, request, jsonify
from src.services.notion_service import NotionService

messages_bp = Blueprint('messages', __name__)

@messages_bp.route('/messages', methods=['POST'])
def create_message():
    """إنشاء رسالة جديدة وإرسالها إلى Notion"""
    try:
        data = request.get_json()
        
        # التحقق من البيانات المطلوبة
        if not data.get('name') or not data.get('message'):
            return jsonify({
                'success': False,
                'error': 'الاسم والرسالة مطلوبان'
            }), 400
        
        name = data.get('name')
        email = data.get('email')
        phone_number = data.get('phone_number')
        message = data.get('message')
        
        # إرسال الرسالة إلى Notion
        notion_service = NotionService()
        result = notion_service.create_message(name, email, phone_number, message)
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': 'تم إرسال رسالتك بنجاح. سنتواصل معك قريباً!'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'حدث خطأ أثناء إرسال الرسالة. يرجى المحاولة مرة أخرى.'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'حدث خطأ غير متوقع'
        }), 500

