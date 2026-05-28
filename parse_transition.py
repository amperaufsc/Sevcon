import csv

def parse_log():
    filepath = r"C:\Users\Guilherme Lettmann\STM32CubeIDE\workspace_1.18.1\AMP\log_280526_183138.csv"
    
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        
        target_cols = {
            'target_id': next((idx for idx, name in enumerate(header) if '1. Target Id' in name), None),
            'id_act': next((idx for idx, name in enumerate(header) if '1. Id A' in name), None),
            'target_iq': next((idx for idx, name in enumerate(header) if '1. Target Iq' in name), None),
            'iq_act': next((idx for idx, name in enumerate(header) if '1. Iq A' in name), None),
            'speed': next((idx for idx, name in enumerate(header) if 'Motor_speed' in name or 'Velocity RPM' in name), None),
            'mod': next((idx for idx, name in enumerate(header) if 'Mod_index' in name or 'Voltage modulation' in name), None),
            'fault': next((idx for idx, name in enumerate(header) if 'Fault_code' in name), None),
            'cc_fault': next((idx for idx, name in enumerate(header) if 'Current_Control_Fault' in name), None),
            'pulsing_dis': next((idx for idx, name in enumerate(header) if 'Pulsing_Disabled' in name), None),
            'vcap': next((idx for idx, name in enumerate(header) if 'Capacitor Voltage' in name or 'V_cap' in name), None),
        }
        
        print("Column mappings found:")
        for k, v in target_cols.items():
            print(f"  {k}: col {v} ({header[v] if v is not None else 'N/A'})")
            
        rows = []
        for idx, row in enumerate(reader):
            if not row:
                continue
            try:
                t_val = float(row[0])
                rows.append((t_val, row))
            except ValueError:
                pass

        last_values = {k: 0.0 for k in target_cols}
        
        data_points = []
        for t, row in rows:
            point = {'time': t}
            for k, col_idx in target_cols.items():
                if col_idx is not None and col_idx < len(row):
                    val_str = row[col_idx].strip()
                    if val_str:
                        try:
                            last_values[k] = float(val_str)
                        except ValueError:
                            if val_str.startswith('0x'):
                                try:
                                    last_values[k] = int(val_str, 16)
                                except ValueError:
                                    pass
                point[k] = last_values[k]
            data_points.append(point)
            
        # Filter data points for t > 150.0
        test_points = [p for p in data_points if p['time'] > 150.0]
        
        if not test_points:
            print("No data points after t = 150.0s!")
            return
            
        # Find when fault occurs for t > 150.0
        fault_points = [p for p in test_points if p['cc_fault'] > 0 or p['fault'] > 0]
        if fault_points:
            fault_time = fault_points[0]['time']
            print(f"\nFault detected at t={fault_time:.3f}s! Fault code = {fault_points[0]['fault']:.0f} (hex: {hex(int(fault_points[0]['fault']))}), CC Fault = {fault_points[0]['cc_fault']:.0f}")
        else:
            print("\nNo explicit fault found after t=150.0s, finding max speed point.")
            max_speed_p = max(test_points, key=lambda p: abs(p['speed']))
            fault_time = max_speed_p['time']
            print(f"Max Speed: {max_speed_p['speed']:.1f} RPM at t={fault_time:.3f}s")
            
        # Print a window around the fault_time
        start_t = fault_time - 2.5
        end_t = fault_time + 1.5
        
        print("\nTime (s) | Speed  | Tgt Id | Id Act | Tgt Iq | Iq Act | Vcap  | Mod % | CC Flt | Pulsing Dis | Fault Code")
        print("-" * 115)
        
        last_printed_t = 0
        for p in test_points:
            if start_t <= p['time'] <= end_t:
                if p['time'] - last_printed_t >= 0.04 or p['cc_fault'] > 0 or p['pulsing_dis'] > 0 or p['fault'] > 0:
                    flt_hex = hex(int(p['fault'])) if p['fault'] > 0 else "0"
                    print(f"{p['time']:8.3f} | {p['speed']:6.1f} | {p['target_id']:6.1f} | {p['id_act']:6.1f} | {p['target_iq']:6.1f} | {p['iq_act']:6.1f} | {p['vcap']:5.1f} | {p['mod']:5.1f} | {p['cc_fault']:6.0f} | {p['pulsing_dis']:11.0f} | {flt_hex}")
                    last_printed_t = p['time']

if __name__ == "__main__":
    parse_log()
