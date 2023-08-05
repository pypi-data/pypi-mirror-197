# import urllib.request
# from pathlib import Path
# from threading import Thread
# from urllib.error import HTTPError

# from tqdm import tqdm


# indian_models = {
#     "encoder": ("https://drive.google.com/uc?export=download&id=1QzZC9bNGC61fqo5GjCA2KddVaeKngV6j", 17095350),
#     "synthesizer": ("https://drive.google.com/uc?export=download&id=1hffQtoxuQisO8uyfwxm6QItmvfntwfEq", 370612245),
#     "vocoder": ("https://drive.google.com/uc?export=download&id=1TmN9ZAGThED8iMgBBicM0Dzx9W3lutRu", 53892437),
# }

# class DownloadProgressBar(tqdm):
#     def update_to(self, b=1, bsize=1, tsize=None):
#         if tsize is not None:
#             self.total = tsize
#         self.update(b * bsize - self.n)


# def download(url: str, target: Path, bar_pos=0):
#     # Ensure the directory exists
#     target.parent.mkdir(exist_ok=True, parents=True)

#     desc = f"Downloading {target.name}"
#     with DownloadProgressBar(unit="B", unit_scale=True, miniters=1, desc=desc, position=bar_pos, leave=False) as t:
#         try:
#             urllib.request.urlretrieve(url, filename=target, reporthook=t.update_to)
#         except HTTPError:
#             return


# def ensure_indian_models(models_dir: Path):
#     # Define download tasks
#     jobs = []
#     for model_name, (url, size) in indian_models.items():   
#         target_path = models_dir / "indian" / f"{model_name}.pt"
#         if target_path.exists():
#             print(target_path.stat().st_size)
#             if target_path.stat().st_size != size:
#                 print(f"File {target_path} is not of expected size, redownloading...")
#             else:
#                 continue

#         thread = Thread(target=download, args=(url, target_path, len(jobs)))
#         thread.start()
#         jobs.append((thread, target_path, size))

#     # Run and join threads
#     for thread, target_path, size in jobs:
#         thread.join()

#         assert target_path.exists() and target_path.stat().st_size == size, \
#             f"Download for {target_path.name} failed. You may download models manually instead.\n" \
#             f"https://drive.google.com/drive/folders/1YTldMyu5oy5zIANrJVJBsk2GFtb5VlMa?usp=share_link"

#%%

import os
os.chdir(r'D:\Research\Voice Cloning\python package\voice_cloning\saved_models')

# Install Git LFS
os.system("git lfs install")

# Clone the repository
os.system("git clone https://huggingface.co/d4data/Indian-voice-cloning")






















