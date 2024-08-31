import shutil
#
#  Capacidad de disco
total, used, free = shutil.disk_usage("/")

# Convertir bytes
total_gb = total // (2**30)
used_gb = used // (2**30)
free_gb = free // (2**30)

print(f"Total:  {total_gb} GB")
print(f"Usado:  {used_gb} GB")
print(f"Libre:  {free_gb} GB")