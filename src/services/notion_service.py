import requests
import json
import os
from datetime import datetime

class NotionService:
    def __init__(self):
        self.notion_token = os.getenv('NOTION_TOKEN')
        self.projects_database_id = os.getenv('NOTION_PROJECTS_DATABASE_ID')
        self.messages_database_id = os.getenv('NOTION_MESSAGES_DATABASE_ID')
        self.base_url = 'https://api.notion.com/v1'
        self.headers = {
            'Authorization': f'Bearer {self.notion_token}',
            'Content-Type': 'application/json',
            'Notion-Version': '2022-06-28'
        }
    
    def get_projects(self):
        """جلب جميع المشاريع من قاعدة بيانات Notion"""
        try:
            url = f'{self.base_url}/databases/{self.projects_database_id}/query'
            response = requests.post(url, headers=self.headers)
            
            if response.status_code == 200:
                data = response.json()
                projects = []
                
                for page in data.get('results', []):
                    project = self._parse_project_page(page)
                    projects.append(project)
                
                return {'success': True, 'projects': projects}
            else:
                return {'success': False, 'error': f'Notion API error: {response.status_code}'}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def create_message(self, name, email, phone_number, message):
        """إنشاء رسالة جديدة في قاعدة بيانات Notion"""
        try:
            url = f'{self.base_url}/pages'
            
            data = {
                'parent': {'database_id': self.messages_database_id},
                'properties': {
                    'Name': {
                        'title': [{'text': {'content': name}}]
                    },
                    'Email': {
                        'email': email if email else None
                    },
                    'Phone Number': {
                        'phone_number': phone_number if phone_number else None
                    },
                    'Message': {
                        'rich_text': [{'text': {'content': message}}]
                    },
                    'Received Date': {
                        'date': {'start': datetime.now().isoformat()}
                    },
                    'Status': {
                        'select': {'name': 'جديد'}
                    }
                }
            }
            
            # إزالة الحقول الفارغة
            if not email:
                del data['properties']['Email']
            if not phone_number:
                del data['properties']['Phone Number']
            
            response = requests.post(url, headers=self.headers, json=data)
            
            if response.status_code == 200:
                return {'success': True, 'message': 'تم إرسال الرسالة بنجاح'}
            else:
                return {'success': False, 'error': f'Notion API error: {response.status_code}'}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _parse_project_page(self, page):
        """تحليل صفحة المشروع من Notion وتحويلها إلى كائن Python"""
        properties = page.get('properties', {})
        
        # استخراج الاسم
        name = ''
        if 'Name' in properties and properties['Name']['title']:
            name = properties['Name']['title'][0]['text']['content']
        
        # استخراج الوصف
        description = ''
        if 'Description' in properties and properties['Description']['rich_text']:
            description = properties['Description']['rich_text'][0]['text']['content']
        
        # استخراج رابط الفيديو
        video_url = ''
        if 'Video URL' in properties and properties['Video URL']['url']:
            video_url = properties['Video URL']['url']
        
        # استخراج التصنيف
        category = ''
        if 'Category' in properties and 'multi_select' in properties['Category'] and properties['Category']['multi_select']:
            categories = [cat['name'] for cat in properties['Category']['multi_select']]
            category = categories[0] if categories else ''
        
        # استخراج الوسوم
        tags = []
        if 'Tags' in properties and 'multi_select' in properties['Tags'] and properties['Tags']['multi_select']:
            tags = [tag['name'] for tag in properties['Tags']['multi_select']]
        
        # استخراج تاريخ الإنشاء
        created_date = ''
        if 'Created Date' in properties and properties['Created Date']['date']:
            created_date = properties['Created Date']['date']['start']
        
        # استخراج الحالة
        status = 'active'
        if 'Status' in properties and properties['Status']['select']:
            status = properties['Status']['select']['name']
        
        return {
            'id': page['id'],
            'name': name,
            'description': description,
            'video_url': video_url,
            'category': category,
            'tags': tags,
            'created_date': created_date,
            'status': status
        }

