#!/usr/bin/env python3
"""
VCD Analysis Script for Hardware Trojan Detection
Parses VCD files and compares switching activity between clean and trojan designs
"""

import re
import matplotlib.pyplot as plt
import numpy as np

def parse_vcd(filename):
    """Parse VCD file and extract toggle counts for each signal
    Returns: dictionary of {signal_name: toggle_count}
    """
    toggles = {}
    signal_map = {}  # Maps VCD identifier to signal name
    
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    # Parse variable declarations
    for line in lines:
        line = line.strip()
        
        if line.startswith('$var'):
            parts = line.split()
            if len(parts) >= 5:
                identifier = parts[3]
                signal_name = parts[4]
                signal_map[identifier] = signal_name
                toggles[signal_name] = 0
        
        if line.startswith('$enddefinitions'):
            break
    
    # Count value changes (toggles)
    prev_values = {}
    for line in lines:
        line = line.strip()
        # Match both single-bit (0!, 1!) and multi-bit (b0000 !, b1111 +) formats
        match = re.match(r'^([b01x]+)\s*(\S+)', line)
        if match:
            value = match.group(1)
            identifier = match.group(2)
            if identifier in signal_map:
                signal_name = signal_map[identifier]
                if identifier in prev_values:
                    if prev_values[identifier] != value:
                        toggles[signal_name] += 1
                prev_values[identifier] = value
    
    return toggles

def compare_toggles(clean_toggles, trojan_toggles):
    """Compare toggle counts and calculate deviations
    Returns: dictionary with signal names and their deviation percentages
    """
    deviations = {}
    for signal in clean_toggles.keys():
        if signal in trojan_toggles:
            clean_count = clean_toggles[signal]
            trojan_count = trojan_toggles[signal]
            if clean_count > 0:
                deviation = abs(trojan_count - clean_count) / clean_count * 100
            else:
                deviation = 0 if trojan_count == 0 else 100
            deviations[signal] = {'clean': clean_count, 'trojan': trojan_count, 'deviation_pct': deviation}
    return deviations

def plot_comparison(deviations, threshold=25):
    """Create bar chart comparing toggle counts"""
    signals = list(deviations.keys())
    clean_counts = [deviations[s]['clean'] for s in signals]
    trojan_counts = [deviations[s]['trojan'] for s in signals]
    deviation_pcts = [deviations[s]['deviation_pct'] for s in signals]
    
    import matplotlib.pyplot as plt
    import numpy as np
    
    x = np.arange(len(signals))
    width = 0.35
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    ax1.bar(x - width/2, clean_counts, width, label='Clean ALU', color='green', alpha=0.7)
    ax1.bar(x + width/2, trojan_counts, width, label='Trojan ALU', color='red', alpha=0.7)
    ax1.set_xlabel('Signal Name')
    ax1.set_ylabel('Toggle Count')
    ax1.set_title('Switching Activity Comparison: Clean vs Trojan ALU')
    ax1.set_xticks(x)
    ax1.set_xticklabels(signals, rotation=45, ha='right')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    colors = ['red' if d > threshold else 'blue' for d in deviation_pcts]
    ax2.bar(signals, deviation_pcts, color=colors, alpha=0.7)
    ax2.axhline(y=threshold, color='orange', linestyle='--', linewidth=2, label=f'{threshold}% Threshold')
    ax2.set_xlabel('Signal Name')
    ax2.set_ylabel('Percentage Deviation')
    ax2.set_title('Percentage Deviation in Toggle Counts')
    ax2.set_xticklabels(signals, rotation=45, ha='right')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('trojan_detection_analysis.png', dpi=300, bbox_inches='tight')
    print("\n✓ Saved visualization: trojan_detection_analysis.png")
    plt.show()

def main():
    print("="*70)
    print("HARDWARE TROJAN DETECTION - VCD ANALYSIS")
    print("="*70)
    
    print("\n[1/4] Parsing clean ALU VCD file...")
    clean_toggles = parse_vcd('alu_clean.vcd')
    print(f"     Found {len(clean_toggles)} signals")
    
    print("\n[2/4] Parsing trojan ALU VCD file...")
    trojan_toggles = parse_vcd('alu_trojan.vcd')
    print(f"     Found {len(trojan_toggles)} signals")
    
    print("\n[3/4] Comparing switching activity...")
    deviations = compare_toggles(clean_toggles, trojan_toggles)
    
    print("\n" + "="*70)
    print("ANALYSIS RESULTS")
    print("="*70)
    print(f"{'Signal':<15} {'Clean':<10} {'Trojan':<10} {'Deviation':<12} {'Status'}")
    print("-"*70)
    
    suspicious_signals = []
    for signal, data in deviations.items():
        status = "⚠ SUSPICIOUS" if data['deviation_pct'] > 25 else "✓ Normal"
        print(f"{signal:<15} {data['clean']:<10} {data['trojan']:<10} {data['deviation_pct']:<11.2f}% {status}")
        if data['deviation_pct'] > 25:
            suspicious_signals.append(signal)
    print("="*70)
    print(f"\nSuspicious signals detected: {len(suspicious_signals)}")
    if suspicious_signals:
        print(f"Signals: {', '.join(suspicious_signals)}")
    
    print("\n[4/4] Generating visualization...")
    plot_comparison(deviations)
    
    print("\n✓ Analysis complete!")

if __name__ == "__main__":
    main()
