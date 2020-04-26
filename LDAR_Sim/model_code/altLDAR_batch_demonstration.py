programs = [
        {
            'methods': {
                    'OGI': {
                             'name': 'OGI',
                             'n_crews': 3,
                             'min_temp': -30,
                             'max_wind': 20,
                             'max_precip': 0.01,
                             'min_interval': 120,
                             'max_workday': 10,  
                             'cost_per_day': 1500,
                             'reporting_delay': 2,
                             'MDL': [0.47, 0.01]
                             }
                        },        
            'master_output_folder': master_output_folder,
            'output_folder': master_output_folder + 'P_ref',
            'timesteps': n_timesteps,
            'start_year': start_year,
            'an_data': an_data,
            'fc_data': fc_data,
            'infrastructure_file': sites,
            'leak_file': leaks,
            'count_file': counts,
            'vent_file': vents,
            't_offsite_file': t_offsite,
            'working_directory': wd,
            'simulation': None,
            'consider_daylight': False,
            'consider_venting': False,
            'repair_delay': 14,
            'LPR': 0.0065,           
            'max_det_op': 0.00,
            'spin_up': spin_up,
            'write_data': write_data,
            'make_plots': make_plots,
            'make_maps': make_maps,
            'start_time': time.time(),
            'operator_strength': operator_strength,
            'sensitivity': {'perform': False, 
                            'program': 'operator', 
                            'batch': [True, 1]}
        },
        {
            'methods': {
                    'truck': {
                             'name': 'truck',
                             'n_crews': 1,
                             'min_temp': -30,
                             'max_wind': 20,
                             'max_precip': 0.01,
                             'min_interval': 50,
                             'max_workday': 10,
                             'cost_per_day': 1500,
                             'follow_up_thresh': 0,
                             'follow_up_ratio': 0.8,
                             'reporting_delay': 2
                             },
                    'OGI_FU': {
                             'name': 'OGI_FU',
                             'n_crews': 2,
                             'min_temp': -30,
                             'max_wind': 20,
                             'max_precip': 0.01,
                             'max_workday': 10,
                             'cost_per_day': 1500,
                             'reporting_delay': 2,
                             'MDL': [0.47, 0.01]
                             }
                        },        
            'master_output_folder': master_output_folder,
            'output_folder': master_output_folder + 'P1_truck',
            'timesteps': n_timesteps,
            'start_year': start_year,
            'an_data': an_data,
            'fc_data': fc_data,
            'infrastructure_file': sites,
            'leak_file': leaks,
            'count_file': counts,
            'vent_file': vents,
            't_offsite_file': t_offsite,
            'working_directory': wd,
            'simulation': None,
            'consider_daylight': True,
            'consider_venting': True,
            'repair_delay': 14,
            'LPR': 0.0065,           
            'max_det_op': 0.00,
            'spin_up': spin_up,
            'write_data': write_data,
            'make_plots': make_plots,
            'make_maps': make_maps,
            'start_time': time.time(),
            'operator_strength': operator_strength,
            'sensitivity': {'perform': False, 
                            'program': 'OGI', 
                            'batch': [True, 2]}
        },
        {
            'methods': {
                    'aircraft': {
                             'name': 'aircraft',
                             'n_crews': 1,
                             'min_temp': -30,
                             'max_wind': 20,
                             'max_precip': 0.01,
                             'min_interval': 50,
                             'max_workday': 10,
                             'cost_per_day': 5000,
                             'follow_up_thresh': 0,
                             'follow_up_ratio': 0.5,
                             't_lost_per_site': 10,                             
                             'reporting_delay': 2,
                             'MDL': 5000  # grams/hour
                             },
                    'OGI_FU': {
                             'name': 'OGI_FU',
                             'n_crews': 1,
                             'min_temp': -30,
                             'max_wind': 20,
                             'max_precip': 0.01,
                             'max_workday': 10,
                             'cost_per_day': 1500,
                             'reporting_delay': 2,
                             'MDL': [0.47, 0.01]
                             }
                        },        
            'master_output_folder': master_output_folder,
            'output_folder': master_output_folder + 'P2_aircraft',
            'timesteps': n_timesteps,
            'start_year': start_year,
            'an_data': an_data,
            'fc_data': fc_data,
            'infrastructure_file': sites,
            'leak_file': leaks,
            'count_file': counts,
            'vent_file': vents,
            't_offsite_file': t_offsite,
            'working_directory': wd,
            'simulation': None,
            'consider_daylight': True,
            'consider_venting': True,
            'repair_delay': 14,
            'LPR': 0.0065,           
            'max_det_op': 0.00,
            'spin_up': spin_up,
            'write_data': write_data,
            'make_plots': make_plots,
            'make_maps': make_maps,
            'start_time': time.time(),
            'operator_strength': operator_strength,
            'sensitivity': {'perform': False, 
                            'program': 'OGI', 
                            'batch': [True, 2]}
        }    
        ]
