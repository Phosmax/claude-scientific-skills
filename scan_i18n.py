
import os
import re
import json

def scan_translations(src_dir, lang_file):
    # Load keys
    with open(lang_file, 'r') as f:
        try:
            translations = json.load(f)
        except json.JSONDecodeError as e:
            print(f"ERROR: JSON Decode Error in {lang_file}: {e}")
            return

    # Flatten keys for easier lookup: "dashboard.title" -> "仪表盘"
    flat_keys = set()
    def flatten(obj, prefix=""):
        for k, v in obj.items():
            if isinstance(v, dict):
                flatten(v, f"{prefix}{k}.")
            else:
                flat_keys.add(f"{prefix}{k}")
    flatten(translations)

    # Regex for useTranslations and t()
    # 1. const t = useTranslations('namespace');
    # 2. t('key')
    
    missing = []
    
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            if not file.endswith(('.tsx', '.ts')):
                continue
            
            path = os.path.join(root, file)
            with open(path, 'r') as f:
                content = f.read()
                
            # Find namespaces: const t = useTranslations('namespace');
            # Also handle: const t2 = useTranslations("common");
            # Also handle: const t = useTranslations(); -> implying global or invalid? Usually specific.
            
            # Map variable name to namespace
            # e.g. { 't': 'dashboard', 'tValid': 'validation' }
            t_vars = {}
            
            # Regex for useTranslations
            # Matches: const t = useTranslations('ns') OR const {t} = use...
            ns_matches = re.finditer(r"(?:const|let|var)\s+(\w+)\s*=\s*useTranslations\(['\"]([^'\"]+)['\"]\)", content)
            for match in ns_matches:
                var_name = match.group(1)
                ns = match.group(2)
                t_vars[var_name] = ns
                
            # If no useTranslations found, maybe it uses `useIntl` or passed props? 
            # For this project, we assume useTranslations pattern dominant.
            
            if not t_vars:
                continue

            # Now find usages for each var
            for var_name, ns in t_vars.items():
                # Matches: t('key') or t("key") or t(`key`)
                # We need to handle t("key", { ... }) too. Just grabbing the first arg.
                
                # key_regex = fr"\b{var_name}\(['\"]([^'\"]+)['\"]"
                # Improved regex to handle nested parenthesis safely? No, simple regex first.
                key_pattern = re.compile(fr"\b{var_name}\(\s*['\"]([^'\"]+)['\"]")
                
                usages = key_pattern.findall(content)
                
                for key in usages:
                    full_key = f"{ns}.{key}"
                    if full_key not in flat_keys:
                        # Ignore dynamic keys like `reportTypes.${type}`
                        if "${" in key:
                            continue
                        missing.append((file, full_key))

    return missing

src_path = "/Users/franklin/Github/claude-scientific-skills/auramax-web/src"
zh_json = "/Users/franklin/Github/claude-scientific-skills/auramax-web/messages/zh.json"
en_json = "/Users/franklin/Github/claude-scientific-skills/auramax-web/messages/en.json"

print("Scanning for missing keys in ZH...")
missing_zh = scan_translations(src_path, zh_json)
if missing_zh:
    for file, key in missing_zh:
        print(f"MISSING in ZH: {key} (found in {file})")
else:
    print("ZH JSON is clean (based on simple heuristic).")

print("\nScanning for missing keys in EN...")
missing_en = scan_translations(src_path, en_json)
if missing_en:
    for file, key in missing_en:
        print(f"MISSING in EN: {key} (found in {file})")
else:
    print("EN JSON is clean.")
