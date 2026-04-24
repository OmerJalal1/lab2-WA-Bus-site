import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'buses_project.settings')
django.setup()

from routes.models import Station

stations_data = [
    ('Central', 'Ramadi'),
    ('University', 'Ramadi'),
    ('Downtown', 'Baghdad'),
    ('Airport', 'Baghdad'),
]

for name, city in stations_data:
    Station.objects.create(name=name, city=city)

print("Stations created successfully!")
