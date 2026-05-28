import csv
import os

def main():
    filepath = r"C:\Users\Guilherme Lettmann\STM32CubeIDE\workspace_1.18.1\AMP\log_280526_183138.csv"
    
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        
        # Mappings of (name, value_col, time_col)
        def find_col_group(name_substring):
            val_idx = next((idx for idx, name in enumerate(header) if name_substring in name), None)
            if val_idx is not None:
                time_idx = val_idx - 1
                return val_idx, time_idx
            return None, None

        vars_to_parse = {
            'target_id': '1. Target Id',
            'id_act': '1. Id A',
            'target_iq': '1. Target Iq',
            'iq_act': '1. Iq A',
            'speed': 'Velocity RPM',
            'mod': 'Voltage modulation',
            'fault': 'Fault_code',
            'cc_fault': 'Current_Control_Fault',
            'pulsing_dis': 'Pulsing_Disabled',
            'vcap': 'Capacitor Voltage',
        }
        
        col_mappings = {}
        for key, name_sub in vars_to_parse.items():
            val_idx, time_idx = find_col_group(name_sub)
            col_mappings[key] = (val_idx, time_idx)

        all_rows = list(reader)
        
        # Extract time series for each variable
        series = {}
        for key, (val_idx, time_idx) in col_mappings.items():
            series[key] = []
            if val_idx is None or time_idx is None:
                continue
            for r in all_rows:
                if val_idx < len(r) and time_idx < len(r):
                    t_str = r[time_idx].strip()
                    val_str = r[val_idx].strip()
                    if t_str and val_str:
                        try:
                            t = float(t_str)
                            try:
                                val = float(val_str)
                            except ValueError:
                                if val_str.startswith('0x'):
                                    val = int(val_str, 16)
                                else:
                                    val = 0.0
                            series[key].append((t, val))
                        except ValueError:
                            pass
            series[key].sort(key=lambda x: x[0])
            
        print(f"Total time range in log: {series['target_id'][0][0]:.3f}s to {series['target_id'][-1][0]:.3f}s")
        
        # Let's find all periods where speed > 10 RPM
        speed_series = series['speed']
        running_periods = []
        in_run = False
        run_start = 0
        for t, v in speed_series:
            if abs(v) > 50:
                if not in_run:
                    in_run = True
                    run_start = t
            else:
                if in_run:
                    in_run = False
                    running_periods.append((run_start, t))
        if in_run:
            running_periods.append((run_start, speed_series[-1][0]))
            
        print("\nActive running periods (speed > 50 RPM):")
        for idx, (start, end) in enumerate(running_periods):
            # find max speed in this period
            max_spd_in_period = max([abs(v) for t, v in speed_series if start <= t <= end])
            print(f"  Period {idx+1}: {start:.3f}s to {end:.3f}s (Max Speed: {max_spd_in_period:.1f} RPM)")
            
        # Let's find all instances of cc_fault transitions (0 to 1)
        cc_fault_series = series['cc_fault']
        cc_fault_transitions = []
        last_val = 0
        for t, val in cc_fault_series:
            if val == 1 and last_val == 0:
                cc_fault_transitions.append(t)
            last_val = val
            
        print("\nCurrent Control Fault (cc_fault) triggers (0 -> 1):")
        for t in cc_fault_transitions:
            print(f"  At t = {t:.3f}s")
            
        # Let's find fault code changes
        fault_series = series['fault']
        fault_changes = []
        last_f = 0
        for t, val in fault_series:
            if val != last_f:
                fault_changes.append((t, last_f, val))
            last_f = val
            
        print("\nFault Code Changes:")
        for t, old_f, new_f in fault_changes:
            print(f"  At t = {t:.3f}s: {hex(int(old_f))} -> {hex(int(new_f))}")

if __name__ == "__main__":
    main()
