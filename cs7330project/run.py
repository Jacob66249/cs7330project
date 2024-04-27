import os
import sys
import django
from django.test import RequestFactory

sys.path.append('C:/Users/jeans/cs7330project/cs7330project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cs7330project.settings')
django.setup()

from university import views

# 创建一个RequestFactory实例
rf = RequestFactory()

# 创建一个GET请求
request = rf.get('/fake-url')

# 调用视图函数，传入请求对象
response = views.your_evaluation_view(request)

# 打印响应的内容（假设它是HTTP响应对象）
print(response.content)
