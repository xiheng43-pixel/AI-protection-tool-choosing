class ClawSecurityMatch:
    def __init__(self):
        # 2026 Mainstream Security Tool Database
        self.tools = {
            "Tencent Lobster Guardian": {"def": 85, "perf": 78, "ease": 98, "priv": 80, "desc": "Top choice for beginners, one-click protection, supports WeChat and mobile alerts."},
            "Baidu Lobster Guard": {"def": 82, "perf": 80, "ease": 95, "priv": 78, "desc": "Baidu security ecosystem, excels at blocking malicious plugins, deeply integrated with browsers."},
            "ClawSecure": {"def": 92, "perf": 92, "ease": 85, "priv": 65, "desc": "Google cloud-based defense, excellent performance, may not be suitable for high-privacy needs."},
            "NemoClaw": {"def": 96, "perf": 88, "ease": 60, "priv": 90, "desc": "NVIDIA hardware isolation, extremely secure, ideal for high-end GPU environments."},
            "ZeroClaw": {"def": 90, "perf": 65, "ease": 40, "priv": 98, "desc": "Ultimate privacy, fully offline, suitable for military/financial sensitive tasks."},
            "OpenFang": {"def": 75, "perf": 98, "ease": 55, "priv": 85, "desc": "Built with Rust, near-zero latency, perfect for performance-focused developers."}
        }

    def run_quiz(self):
        print("="*50)
        print("   2026 OpenClaw Security Expert System (Veto Enabled)")
        print("="*50)
        
        # 1. Collect user requirements
        ans = {}
        ans['tech'] = input("\n1. Your technical skill level?\n(A. Beginner B. Can configure C. Developer): ").upper()
        ans['hw'] = input("\n2. Device performance?\n(A. Basic B. Good C. High-end): ").upper()
        ans['scene'] = input("\n3. Main usage scenario?\n(A. Daily use B. Office work C. Confidential tasks): ").upper()
        ans['cloud'] = input("\n4. Privacy requirement?\n(A. Cloud allowed B. Local preferred C. No internet): ").upper()
        ans['speed'] = input("\n5. Response priority?\n(A. Security first B. Balanced C. Instant response): ").upper()

        # 2. Initialize weights
        w = {"def": 0.2, "perf": 0.2, "ease": 0.2, "priv": 0.2}

        # 3. Dynamic weight adjustment (Soft Logic)
        if ans['tech'] == 'A': w['ease'] += 0.5
        if ans['scene'] == 'C': w['def'] += 0.5
        if ans['speed'] == 'C': w['perf'] += 0.4
        if ans['cloud'] == 'C': w['priv'] += 0.6

        # 4. Hard Veto Constraints
        filtered_tools = {}
        for name, m in self.tools.items():
            # Rule 1: If confidential task (C), defense < 90 is rejected
            if ans['scene'] == 'C' and m['def'] < 90:
                continue
            # Rule 2: If no internet (C), privacy < 90 is rejected
            if ans['cloud'] == 'C' and m['priv'] < 90:
                continue
            # Rule 3: If beginner (A), ease of use < 70 is rejected
            if ans['tech'] == 'A' and m['ease'] < 70:
                continue
            
            filtered_tools[name] = m

        # 5. Calculate scores
        results = []
        for name, m in filtered_tools.items():
            score = (m['def'] * w['def'] + m['perf'] * w['perf'] + 
                     m['ease'] * w['ease'] + m['priv'] * w['priv'])
            results.append({"name": name, "score": round(score, 2), "desc": m['desc']})

        # 6. Show results
        results.sort(key=lambda x: x['score'], reverse=True)

        if not results:
            print("\n[WARNING]: No security tools fully match your strict requirements. Please relax some constraints.")
        else:
            top = results[0]
            print(f"\n🏆 Best Match: 【{top['name']}】")
            print(f"Compatibility Score: {top['score']}")
            print(f"Description: {top['desc']}")
            
            if len(results) > 1:
                print("\nOther qualified alternatives:")
                for r in results[1:3]:
                    print(f"- {r['name']} (Score: {r['score']})")

if __name__ == "__main__":
    matcher = ClawSecurityMatch()
    matcher.run_quiz()
