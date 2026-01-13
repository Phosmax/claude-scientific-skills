import subprocess
import sys
import os
import time

def run_test(script_name):
    print(f"\n{'='*60}")
    print(f"Running {script_name}...")
    print(f"{'='*60}\n")
    
    start_time = time.time()
    try:
        # Use sys.executable to ensure we use the same python interpreter
        result = subprocess.run(
            [sys.executable, script_name], 
            cwd=os.path.dirname(os.path.abspath(__file__)) + "/..", # Run from project root
            capture_output=True,
            text=True
        )
        
        duration = time.time() - start_time
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
            
        if result.returncode == 0:
            print(f"\n✅ {script_name} PASSED ({duration:.2f}s)")
            return True
        else:
            print(f"\n❌ {script_name} FAILED ({duration:.2f}s)")
            return False
            
    except Exception as e:
        print(f"\n❌ {script_name} CRASHED: {e}")
        return False

def main():
    print("🚀 Starting AuraMax System Verification Suite")
    
    scripts = [
        "tests/verify_coach_logic.py",
        "tests/verify_wearables_manual.py",
        "tests/verify_fhir.py"
    ]
    
    results = []
    
    for script in scripts:
        if os.path.exists(script):
            success = run_test(script)
            results.append((script, success))
        else:
            print(f"⚠️ Script not found: {script}")
            results.append((script, False))
            
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    
    all_passed = True
    for script, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {script}")
        if not success:
            all_passed = False
            
    if all_passed:
        print("\n🎉 ALL SYSTEMS GO! AuraMax is stable.")
        sys.exit(0)
    else:
        print("\n⚠️ SOME CHECKS FAILED.")
        sys.exit(1)

if __name__ == "__main__":
    main()
