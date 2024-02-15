import os
import django
import json

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "clockInOutDjango.settings")
django.setup()

# Import the Django model
from clockInOut.models import CompanyTarget

# Function to get company targets from the database
def get_company_targets():
    targets = CompanyTarget.objects.all()
    return {target.job_role: target.target_hours for target in targets}

# Load the JSON data
json_file_path = 'calculated_hours.json'
with open(json_file_path, 'r') as infile:
    data = json.load(infile)

# Get the latest company targets from your Django model
company_targets = get_company_targets()

# Prepare the data structure for the last 3 months' hours
last_3_months_hours = {role: [] for role in company_targets.keys()}

for entry in data:
    job_role = entry["job_role"]
    month = entry["month"]
    hours = entry["predicted_hours"]
    # Adjust job role names to match the keys in company_targets if necessary
    # This may need modification based on how your job roles are stored in the JSON vs the database
    adjusted_job_role = job_role  # Assuming job_role matches the database keys
    if adjusted_job_role in last_3_months_hours and month in [10, 11, 12]:  # Assuming 10, 11, 12 as the last 3 months
        last_3_months_hours[adjusted_job_role].append(hours)

# Calculate projection for the whole year based on the last 3 months
yearly_projection = {}
for job_role, hours in last_3_months_hours.items():
    if hours:
        monthly_average = sum(hours) / len(hours)
        yearly_projection[job_role] = monthly_average * 12

# Compare with company targets
comparison = []
for job_role, target_hours in company_targets.items():
    actual = yearly_projection.get(job_role, 0)
    comparison.append({
        "job_role": job_role,
        "target_hours": float(target_hours),  # Ensure numeric comparison
        "projected_hours": actual,
        "status": "Above Target" if actual > target_hours else "Below Target"
    })

# Print or save the comparison to a file
print(json.dumps(comparison, indent=4))
