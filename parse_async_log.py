import csv
import os
import bisect

def get_value_at_time(time_series, t):
    if not time_series:
        return 0.0
    idx = bisect.bisect_right(time_series, (t, float('inf'))) - 1
    if idx < 0:
        return time_series[0][1]
    return time_series[idx][1]

def main():
    filepath = r"C:\Users\Guilherme Lettmann\STM32CubeIDE\workspace_1.18.1\AMP\log_280526_183138.csv"
    
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        
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

        # Find first fault after t = 150.0
        fault_events = []
        for t, val in series['cc_fault']:
            if t > 150.0 and val > 0:
                fault_events.append(t)
        
        if fault_events:
            first_fault_time = min(fault_events)
            print(f"First fault after 150s detected at t={first_fault_time:.3f}s")
            t_start = first_fault_time - 1.5
            t_end = first_fault_time + 1.0
        else:
            t_start = 174.0
            t_end = 178.0

        t_current = t_start
        grid_step = 0.020 # 20ms
        
        print("\nTime (s) | Speed  | Tgt Id | Id Act | Tgt Iq | Iq Act | Vcap  | Mod % | CC Flt | Pulsing Dis | Fault Code")
        print("-" * 115)
        
        while t_current <= t_end:
            speed_val = get_value_at_time(series['speed'], t_current)
            tgt_id_val = get_value_at_time(series['target_id'], t_current)
            id_act_val = get_value_at_time(series['id_act'], t_current)
            tgt_iq_val = get_value_at_time(series['target_iq'], t_current)
            iq_act_val = get_value_at_time(series['iq_act'], t_current)
            vcap_val = get_value_at_time(series['vcap'], t_current)
            mod_val = get_value_at_time(series['mod'], t_current)
            cc_fault_val = get_value_at_time(series['cc_fault'], t_current)
            puls_dis_val = get_value_at_time(series['pulsing_dis'], t_current)
            fault_val = get_value_at_time(series['fault'], t_current)
            
            flt_hex = hex(int(fault_val)) if fault_val > 0 else "0"
            print(f"{t_current:8.3f} | {speed_val:6.1f} | {tgt_id_val:6.1f} | {id_act_val:6.1f} | {tgt_iq_val:6.1f} | {iq_act_val:6.1f} | {vcap_val:5.1f} | {mod_val:5.1f} | {cc_fault_val:6.0f} | {puls_dis_val:11.0f} | {flt_hex}")
            
            t_current += grid_step

if __name__ == "__main__":
    main()
