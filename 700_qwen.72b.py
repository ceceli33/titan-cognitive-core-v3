
import torch,psutil,shutil,platform,json
print("="*72)
print("AKBASCORE TEST700 — QWEN2.5-72B HARDWARE CALIBRATION")
print("="*72)
assert torch.cuda.is_available(),"CUDA GPU bulunamadi"
p=torch.cuda.get_device_properties(0)
vram=p.total_memory/2**30
ram=psutil.virtual_memory()
disk=shutil.disk_usage("/content")
print("GPU:",p.name)
print("GPU_VRAM_GiB:",round(vram,3))
print("RAM_TOTAL_GiB:",round(ram.total/2**30,3))
print("RAM_AVAILABLE_GiB:",round(ram.available/2**30,3))
print("DISK_FREE_GiB:",round(disk.free/2**30,3))
print("TORCH:",torch.__version__)
print("CUDA:",torch.version.cuda)
print("PYTHON:",platform.python_version())
print("-"*72)
layers=80
hidden=8192
kv_heads=8
head_dim=128
kv_bytes_per_token=layers*2*kv_heads*head_dim*2
print("MODEL_RAW_4BIT_GiB:",round(72.7e9*0.5/2**30,3))
print("KV_BF16_BYTES_PER_TOKEN:",kv_bytes_per_token)
print("KV_BF16_MiB_PER_1024_TOKENS:",round(kv_bytes_per_token*1024/2**20,3))
print("NOTE: Model memory excludes quantization metadata and runtime overhead.")
print("NOTE: KV capacity is theoretical, not a validated cartridge limit.")
print("="*72)
