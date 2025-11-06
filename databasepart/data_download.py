import requests
import zipfile
import os

def download_movielens_variant():
    """下载数据集"""
    dataset_size = "10M100K"
    url = "https://files.grouplens.org/datasets/movielens/ml-10m.zip"
    filename = f"ml-{dataset_size}.zip"
    extract_path = f"./movielens_data"

    if os.path.exists(f"{extract_path}/ml-{dataset_size}"):
        print(f"{dataset_size}数据集先前已经下载完毕")
        return

    os.makedirs(extract_path, exist_ok=True)

    try:
        print(f"正在下载MovieLens {dataset_size.upper()} 数据集...")
        response = requests.get(url, stream=True)
        response.raise_for_status()

        # 显示下载进度
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0

        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                downloaded += len(chunk)
                if total_size > 0:
                    progress = (downloaded / total_size) * 100
                    print(f"\r下载进度: {progress:.1f}%", end="")

        print("\n下载完成，正在解压...")
        with zipfile.ZipFile(filename, 'r') as zip_ref:
            # 解压所有文件
            zip_ref.extractall(extract_path)
        os.remove(filename)
        print(f"数据集已保存到: {extract_path}")

    except Exception as e:
        print(f"下载失败: {e}")

def main():
    download_movielens_variant()


if __name__ == '__main__':
    main()