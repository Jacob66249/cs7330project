import os
import django
from django.core.management import call_command
from django.conf import settings

# 设置Django环境
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cs7330project.settings")
django.setup()

# 指定fixture文件所在的目录
fixtures_dir = 'university/fixtures/'

# 遍历目录，加载每个JSON文件
for fixture_file in os.listdir(fixtures_dir):
    if fixture_file.endswith('.json'):
        fixture_path = os.path.join(fixtures_dir, fixture_file)
        print(f"Loading {fixture_path}...")
        call_command('loaddata', fixture_path)

print("All fixtures loaded.")
