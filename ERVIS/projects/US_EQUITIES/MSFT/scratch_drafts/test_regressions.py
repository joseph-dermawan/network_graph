import numpy as np
import json

# 1. Driver 1: Azure Cloud Revenue ($B) vs Enterprise Cloud Infrastructure Spend ($B)
cloud_infra_spend = np.array([178.0, 215.0, 260.0, 312.0, 380.0]) # FY22 to FY26
azure_cloud_rev = np.array([34.0, 45.0, 58.0, 75.0, 98.0]) # Azure standalone est
slope_1, intercept_1 = np.polyfit(cloud_infra_spend, azure_cloud_rev, 1)
r2_1 = (np.corrcoef(cloud_infra_spend, azure_cloud_rev)[0, 1])**2

# 2. Driver 2: Microsoft 365 Copilot Paid Seats (M) vs Commercial Cloud Revenue ($B)
copilot_seats = np.array([0.5, 3.5, 12.0, 28.0]) # Millions of paid enterprise seats
comm_cloud_rev = np.array([110.0, 137.0, 168.0, 210.0])
slope_2, intercept_2 = np.polyfit(copilot_seats, comm_cloud_rev, 1)
r2_2 = (np.corrcoef(copilot_seats, comm_cloud_rev)[0, 1])**2

# 3. Driver 3: Global IaaS/PaaS Volume Index vs Total Revenue ($B)
iaas_index = np.array([100.0, 128.0, 162.0, 205.0, 260.0])
msft_total_rev = np.array([198.3, 211.9, 245.1, 281.7, 331.8])
slope_3, intercept_3 = np.polyfit(iaas_index, msft_total_rev, 1)
r2_3 = (np.corrcoef(iaas_index, msft_total_rev)[0, 1])**2

print(f"Driver 1 R2: {r2_1:.4f} (slope: {slope_1:.2f}, int: {intercept_1:.2f})")
print(f"Driver 2 R2: {r2_2:.4f} (slope: {slope_2:.2f}, int: {intercept_2:.2f})")
print(f"Driver 3 R2: {r2_3:.4f} (slope: {slope_3:.2f}, int: {intercept_3:.2f})")
