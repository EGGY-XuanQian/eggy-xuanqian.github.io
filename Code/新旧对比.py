import os
import hashlib
import shutil

def get_file_md5(file_path):
    """计算文件的MD5哈希值，增加错误处理"""
    if not os.path.isfile(file_path):
        print(f"警告：{file_path} 不是有效的文件，跳过MD5计算")
        return None
    
    hash_md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception as e:
        print(f"计算 {file_path} 的MD5时出错: {str(e)}")
        return None

def get_all_files(folder):
    """获取文件夹中所有文件（包括子目录）"""
    if not os.path.isdir(folder):
        print(f"错误：{folder} 不是有效的文件夹路径")
        return []
    
    all_files = []
    for root, _, files in os.walk(folder):
        for file in files:
            all_files.append(os.path.join(root, file))
    
    return all_files

def main():
    # ==== 直接在这里修改你的路径 ====
    old_folder = r"D:\\新旧对比\\OLD"    # 旧文件夹
    new_folder = r"D:\\新旧对比\\NEW"    # 新文件夹
    # ==============================
    
    print("开始扫描旧文件夹...")
    # 扫描旧文件夹的所有文件MD5（包括子文件夹）
    old_files = get_all_files(old_folder)
    old_files_md5 = set()
    
    for file_path in old_files:
        md5 = get_file_md5(file_path)
        if md5:
            old_files_md5.add(md5)
    
    print(f"旧文件夹共扫描到 {len(old_files)} 个文件，计算了 {len(old_files_md5)} 个有效MD5值")
    
    print("开始扫描新文件夹...")
    # 扫描新文件夹，找出新增文件（包括子文件夹）
    new_files = get_all_files(new_folder)
    added_files = []
    
    for file_path in new_files:
        md5 = get_file_md5(file_path)
        if md5 and md5 not in old_files_md5:
            added_files.append(file_path)
    
    print(f"新文件夹共扫描到 {len(new_files)} 个文件，其中新增文件 {len(added_files)} 个")
    
    # 所有扫描完成后才创建新增文件夹
    if added_files:  # 只有存在新增文件时才创建文件夹
        new_wem_dir = os.path.join(new_folder, "NEW")
        try:
            os.makedirs(new_wem_dir, exist_ok=True)
            print(f"创建目标文件夹: {new_wem_dir}")
            
            # 复制新增文件
            for file_path in added_files:
                try:
                    filename = os.path.basename(file_path)
                    dest_path = os.path.join(new_wem_dir, filename)
                    if os.path.exists(dest_path):
                        print(f"跳过已存在文件: {filename}")
                        continue
                    shutil.copy2(file_path, dest_path)
                    print(f"复制: {filename}")
                except Exception as e:
                    print(f"复制 {file_path} 失败: {str(e)}")
            
            print(f"完成！新增文件已复制到: {new_wem_dir}")
        except Exception as e:
            print(f"创建文件夹失败: {str(e)}")
    else:
        print("没有发现新增文件，无需创建文件夹")

if __name__ == "__main__":
    main()