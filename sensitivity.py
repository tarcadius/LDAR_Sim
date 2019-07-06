#------------------------------------------------------------------------------
# Name:         LDAR-Sim Sensitivity Analysis - Operator
#
# Authors:      Thomas Fox, Mozhou Gao, Thomas Barchyn, Chris Hugenholtz
#
# Created:      2019-Jul-02
#
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
import numpy as np
import pandas as pd
import os

class sensitivity:
    def __init__ (self, parameters, timeseries, state):
        '''
        Initialize a sensitivity analysis.

        '''   
        self.parameters = parameters
        self.timeseries = timeseries
        self.state = state
        
        if self.parameters['sensitivity'][1] == 'operator':

            # Define SA parameters
            self.sens_params = {
            'LSD_outliers': int(np.round(np.random.normal(0, 1))),
            'LSD_samples': int(np.random.normal(len(self.state['empirical_leaks']), len(self.state['empirical_leaks'])/4)),
            
            'LCD_outliers': int(np.round(np.random.normal(0, 1))),
            'LCD_samples': int(np.random.normal(len(self.state['empirical_counts']), len(self.state['empirical_counts'])/4)),
            
            'site_rate_outliers': int(np.round(np.random.normal(0, 1))),
            'site_rate_samples': int(np.random.normal(len(self.state['empirical_sites']), len(self.state['empirical_sites'])/4)),
            
            'LPR': np.random.gamma(1.39, 0.00338),
            'repair_delay': np.random.uniform(0, 100),
            'max_det_op': np.random.exponential(1/10)
            }  
            
            # Set scalar parameters
            self.parameters['LPR'] = self.sens_params['LPR']
            self.parameters['repair_delay'] = self.sens_params['repair_delay']
            self.parameters['max_det_op'] = self.sens_params['max_det_op']
            
            # Modify input distributions - leak rates
            if self.sens_params['LSD_outliers'] < 0:
                for i in range(abs(self.sens_params['LSD_outliers'])):
                    self.state['empirical_leaks'] = np.delete(self.state['empirical_leaks'], np.where(self.state['empirical_leaks'] == max(self.state['empirical_leaks'])))
            if self.sens_params['LSD_outliers'] > 0:
                for i in range(self.sens_params['LSD_outliers']):
                    new_value = max(self.state['empirical_leaks']) * 2
                    self.state['empirical_leaks'] = np.append(self.state['empirical_leaks'], new_value)

            while self.sens_params['LSD_samples'] < 10:
                self.sens_params['LSD_samples'] = int(np.random.normal(len(self.state['empirical_leaks']), len(self.state['empirical_leaks'])/4))
                        
            self.state['empirical_leaks'] = np.random.choice(self.state['empirical_leaks'], self.sens_params['LSD_samples'])
                
            # Modify input distributions - leak counts
            if self.sens_params['LCD_outliers'] < 0:
                for i in range(abs(self.sens_params['LCD_outliers'])):
                    self.state['empirical_counts'] = np.delete(self.state['empirical_counts'], np.where(self.state['empirical_counts'] == max(self.state['empirical_counts'])))                
            if self.sens_params['LCD_outliers'] > 0:
                for i in range(self.sens_params['LCD_outliers']):
                    new_value = max(self.state['empirical_counts']) * 2
                    self.state['empirical_counts'] = np.append(self.state['empirical_counts'], new_value)

            while self.sens_params['LCD_samples'] < 10:
                self.sens_params['LCD_samples'] = int(np.random.normal(len(self.state['empirical_counts']), len(self.state['empirical_counts'])/4))
                        
            self.state['empirical_counts'] = np.random.choice(self.state['empirical_counts'], self.sens_params['LCD_samples'])

            
            # Modify input distributions - site emissions (for venting - if requested)
            if self.parameters['consider_venting'] == True:
                if self.sens_params['site_rate_outliers'] < 0:
                    for i in range(abs(self.sens_params['site_rate_outliers'])):
                        self.state['empirical_sites'] = np.delete(self.state['empirical_sites'], np.where(self.state['empirical_sites'] == max(self.state['empirical_sites'])))               
                if self.sens_params['site_rate_outliers'] > 0:
                    for i in range(self.sens_params['site_rate_outliers']):
                        new_value = max(self.state['empirical_sites']) * 2
                        self.state['empirical_sites'] = np.append(self.state['empirical_sites'], new_value)

            while self.sens_params['site_rate_samples'] < 10:
                self.sens_params['site_rate_samples'] = int(np.random.normal(len(self.state['empirical_sites']), len(self.state['empirical_sites'])/4))
                        
            self.state['empirical_sites'] = np.random.choice(self.state['empirical_sites'], self.sens_params['site_rate_samples'])
                      
        
        if self.parameters['sensitivity'][1] == 'OGI':
            self.sens_params = {
            'consider_daylight': bool(np.random.binomial(1, 0.5)),
            'n_crews': np.random.poisson(0.5) + 1,
            'min_temp': np.random.normal(-20, 10),
            'max_wind': np.random.normal(15, 3), 
            'max_precip': np.random.normal(3, 1), # Need to change according to measurement units
            'max_workday': round(np.random.uniform(6, 14)),  
            'reporting_delay': np.random.uniform(0,7),
            'OGI_time': np.random.uniform(30,300),
            'OGI_required_surveys': np.random.uniform(1, 4),
            'min_interval': np.random.uniform(0, 90),
            'MDL': [np.random.uniform(0, 2.5), 0.01]
            }     

            # Set scalar parameters
            self.parameters['consider_daylight'] = self.sens_params['consider_daylight']
            self.parameters['methods']['OGI']['min_temp'] = self.sens_params['min_temp']
            self.parameters['methods']['OGI']['max_wind'] = self.sens_params['max_wind']
            self.parameters['methods']['OGI']['max_precip'] = self.sens_params['max_precip']
            self.parameters['methods']['OGI']['min_interval'] = self.sens_params['min_interval']
            self.parameters['methods']['OGI']['max_workday'] = self.sens_params['max_workday']
            self.parameters['methods']['OGI']['reporting_delay'] = self.sens_params['reporting_delay']
            self.parameters['methods']['OGI']['MDL'] = self.sens_params['MDL']

            for site in self.state['sites']:
                site['OGI_time'] = self.sens_params['OGI_time']
                site['OGI_required_surveys'] = self.sens_params['OGI_required_surveys']

            return

    def write_data (self):
              
        if self.parameters['sensitivity'][1] == 'operator':

            # Make folder for sensitivity analysis outputs
            output_directory = os.path.join(self.parameters['working_directory'], self.parameters['output_folder'], 'sensitivity_analysis')
            if not os.path.exists(output_directory):
                os.makedirs(output_directory) 

            
            # Build output dataframe
            df_dict = {
            # SA inputs
            'simulation': [self.parameters['simulation']],
            'LSD_outliers': [self.sens_params['LSD_outliers']],
            'LSD_samples': [self.sens_params['LSD_samples']],
            'LCD_outliers': [self.sens_params['LCD_outliers']],
            'LCD_samples': [self.sens_params['LCD_samples']],
            'site_rate_outliers': [self.sens_params['site_rate_outliers']],
            'site_rate_samples': [self.sens_params['site_rate_samples']],
            'LPR': [self.sens_params['LPR']],
            'repair_delay': [self.sens_params['repair_delay']],
            'max_det_op': [self.sens_params['max_det_op']],

            # SA outputs
            'mean_dail_site_em': np.mean(np.array(self.timeseries['daily_emissions_kg'][self.parameters['spin_up']:])/len(self.state['sites'])),
            'std_dail_site_em': np.std(np.array(self.timeseries['daily_emissions_kg'][self.parameters['spin_up']:])/len(self.state['sites'])),
            'cum_repaired_leaks': self.timeseries['cum_repaired_leaks'][-1:],
            'med_active_leaks': np.median(np.array(self.timeseries['active_leaks'][self.parameters['spin_up']:])),
            'med_days_active': np.median(pd.DataFrame(self.state['leaks'])['days_active']),
            'med_leak_rate': np.median(pd.DataFrame(self.state['leaks'])['rate']),
            'cum_init_leaks': np.sum(pd.DataFrame(self.state['sites'])['initial_leaks']),
                    }
            
            # Build a dataframe for export
            df_new = pd.DataFrame(df_dict)  
            
            # Set output file name
            output_file = os.path.join(output_directory, 'sensitivity_operator.csv')            
            
            if not os.path.exists(output_file):
                df_new.to_csv(output_file, index = False)
                
            elif os.path.exists(output_file):
                df_old = pd.read_csv(output_file)
                df_old = df_old.append(df_new)
                df_old.to_csv(output_file, index = False)
                
                
        if self.parameters['sensitivity'][1] == 'reference':

            # Make folder for sensitivity analysis outputs
            output_directory = os.path.join(self.parameters['working_directory'], self.parameters['master_output_folder'], 'sensitivity_analysis')
            if not os.path.exists(output_directory):
                os.makedirs(output_directory) 

            
            # Sensitivity input variables here
            OGI_times = []
            for site in self.state['sites']:
                OGI_times.append(float(site['OGI_time']))
            mean_OGI_time = np.mean(OGI_times)

            OGI_surveys = []
            for site in self.state['sites']:
                OGI_surveys.append(float(site['OGI_required_surveys']))
            mean_OGI_required_surveys = np.mean(OGI_surveys)
            
            df_dict = {
            # SA inputs
            'simulation': [self.parameters['simulation']],
            'consider_daylight': [self.parameters['consider_daylight']],
            'n_crews': [self.parameters['methods']['OGI']['n_crews']],
            'min_temp': [self.parameters['methods']['OGI']['min_temp']],
            'max_wind': [self.parameters['methods']['OGI']['max_wind']],
            'max_precip': [self.parameters['methods']['OGI']['max_precip']],
            'min_interval': [self.parameters['methods']['OGI']['min_interval']],
            'max_workday': [self.parameters['methods']['OGI']['max_workday']],  
            'reporting_delay': [self.parameters['methods']['OGI']['reporting_delay']],
            'MDL': [self.parameters['methods']['OGI']['MDL'][0]],
            'MDL_std': [self.parameters['methods']['OGI']['MDL'][1]],            
            'mean_OGI_time': [mean_OGI_time],
            'mean_OGI_required_surveys': [mean_OGI_required_surveys],
           
            # SA outputs
            'mean_dail_site_em': np.mean(np.array(self.timeseries['daily_emissions_kg'][self.parameters['spin_up']:])/len(self.state['sites'])),
            'std_dail_site_em': np.std(np.array(self.timeseries['daily_emissions_kg'][self.parameters['spin_up']:])/len(self.state['sites'])),
            'cum_program_cost': np.sum(np.array(self.timeseries['OGI_cost'][self.parameters['spin_up']:])),
            'cum_repaired_leaks': self.timeseries['cum_repaired_leaks'][-1:],
            'med_active_leaks': np.median(np.array(self.timeseries['active_leaks'][self.parameters['spin_up']:])),
            'med_prop_sites_avail': np.median(np.array(self.timeseries['OGI_prop_sites_avail'][self.parameters['spin_up']:])),

            'med_days_active': np.median(pd.DataFrame(self.state['leaks'])['days_active']),
            'med_leak_rate': np.median(pd.DataFrame(self.state['leaks'])['rate']),

            'cum_init_leaks': np.sum(pd.DataFrame(self.state['sites'])['initial_leaks']),
            'cum_missed_leaks': np.sum(pd.DataFrame(self.state['sites'])['OGI_missed_leaks']),
            'cum_OGI_surveys': np.sum(pd.DataFrame(self.state['sites'])['OGI_surveys_conducted'])
                }

            # Build a dataframe for export
            df_new = pd.DataFrame(df_dict)  
            
            # Set output file name
            output_file = os.path.join(output_directory, 'sensitivity_reference.csv')            
            
            if not os.path.exists(output_file):
                df_new.to_csv(output_file, index = False)
                
            elif os.path.exists(output_file):
                df_old = pd.read_csv(output_file)
                df_old = df_old.append(df_new)
                df_old.to_csv(output_file, index = False)
                        
        
        if self.parameters['sensitivity'][1] == 'OGI':
            
            # Make folder for sensitivity analysis outputs
            output_directory = os.path.join(self.parameters['working_directory'], self.parameters['master_output_folder'], 'sensitivity_analysis')
            if not os.path.exists(output_directory):
                os.makedirs(output_directory) 

            # Sensitivity input variables here
            OGI_times = []
            for site in self.state['sites']:
                OGI_times.append(float(site['OGI_time']))
            mean_OGI_time = np.mean(OGI_times)

            OGI_surveys = []
            for site in self.state['sites']:
                OGI_surveys.append(float(site['OGI_required_surveys']))
            mean_OGI_required_surveys = np.mean(OGI_surveys)

            df_dict = {
            # SA inputs
            'simulation': [self.parameters['simulation']],
            'consider_daylight': [self.sens_params['consider_daylight']],
            'n_crews': [self.sens_params['n_crews']],
            'min_temp': [self.sens_params['min_temp']],
            'max_wind': [self.sens_params['max_wind']],
            'max_precip': [self.sens_params['max_precip']],
            'min_interval': [self.sens_params['min_interval']],
            'max_workday': [self.sens_params['max_workday']],  
            'reporting_delay': [self.sens_params['reporting_delay']],
            'MDL': [self.sens_params['MDL'][0]],
            'MDL_std': [self.sens_params['MDL'][1]],
            'mean_OGI_time': mean_OGI_time,
            'mean_OGI_required_surveys': mean_OGI_required_surveys,
            
            # SA outputs
            'mean_dail_site_em': np.mean(np.array(self.timeseries['daily_emissions_kg'][self.parameters['spin_up']:])/len(self.state['sites'])),
            'std_dail_site_em': np.std(np.array(self.timeseries['daily_emissions_kg'][self.parameters['spin_up']:])/len(self.state['sites'])),
            'cum_program_cost': np.sum(np.array(self.timeseries['OGI_cost'][self.parameters['spin_up']:])),
            'cum_repaired_leaks': self.timeseries['cum_repaired_leaks'][-1:],
            'med_active_leaks': np.median(np.array(self.timeseries['active_leaks'][self.parameters['spin_up']:])),
            'med_prop_sites_avail': np.median(np.array(self.timeseries['OGI_prop_sites_avail'][self.parameters['spin_up']:])),

            'med_days_active': np.median(pd.DataFrame(self.state['leaks'])['days_active']),
            'med_leak_rate': np.median(pd.DataFrame(self.state['leaks'])['rate']),

            'cum_init_leaks': np.sum(pd.DataFrame(self.state['sites'])['initial_leaks']),
            'cum_missed_leaks': np.sum(pd.DataFrame(self.state['sites'])['OGI_missed_leaks']),
            'cum_OGI_surveys': np.sum(pd.DataFrame(self.state['sites'])['OGI_surveys_conducted'])
                }

            # Build a dataframe for export
            df_new = pd.DataFrame(df_dict)  
            
            # Set output file name
            output_file = os.path.join(output_directory, 'sensitivity_OGI.csv')            
            
            if not os.path.exists(output_file):
                df_new.to_csv(output_file, index = False)
                
            elif os.path.exists(output_file):
                df_old = pd.read_csv(output_file)
                df_old = df_old.append(df_new)
                df_old.to_csv(output_file, index = False)
            
            
            # Finally, can load the two csv files we just exported and process into main results
            df_ref = pd.read_csv(os.path.join(output_directory, 'sensitivity_reference.csv'))
            df_OGI = pd.read_csv(os.path.join(output_directory, 'sensitivity_OGI.csv'))
            
            if len(df_ref) == len(df_OGI):
            
                # Build new dataframe
                df_combine = {
                
                # SA inputs
                'simulation': list(df_OGI['simulation']),
                'consider_daylight': list(df_OGI['consider_daylight']),
                'n_crews_dif': list(df_ref['n_crews'] - df_OGI['n_crews']),
                'min_temp_dif': list(df_ref['min_temp'] - df_OGI['min_temp']),
                'max_wind_dif': list(df_ref['max_wind'] - df_OGI['max_wind']),
                'max_precip_dif': list(df_ref['max_precip'] - df_OGI['max_precip']),
                'min_interval_dif': list(df_ref['min_interval'] - df_OGI['min_interval']),
                'max_workday_dif': list(df_ref['max_workday'] - df_OGI['max_workday']),  
                'reporting_delay_dif': list(df_ref['reporting_delay'] - df_OGI['reporting_delay']),
                'MDL_dif': list(df_ref['MDL'] - df_OGI['MDL']),
                'MDL_std_dif': list(df_ref['MDL_std'] - df_OGI['MDL_std']),
                'mean_OGI_time_dif': list(df_ref['mean_OGI_time'] - df_OGI['mean_OGI_time']),
                'mean_OGI_required_surveys_dif': list(df_ref['mean_OGI_required_surveys'] - df_OGI['mean_OGI_required_surveys']),
                
                # SA outputs
                'mean_dail_site_em_dif': list(df_ref['mean_dail_site_em'] - df_OGI['mean_dail_site_em']),
                'std_dail_site_em_dif': list(df_ref['std_dail_site_em'] - df_OGI['std_dail_site_em']),

                'cum_program_cost_dif': list(df_ref['cum_program_cost'] - df_OGI['cum_program_cost']),
                'repaired_leaks_dif': list(df_ref['cum_repaired_leaks'] - df_OGI['cum_repaired_leaks']),
                'med_active_leaks_dif': list(df_ref['med_active_leaks'] - df_OGI['med_active_leaks']),
                'med_prop_sites_avail_dif': list(df_ref['med_prop_sites_avail'] - df_OGI['med_prop_sites_avail']),

                'med_days_active_dif': list(df_ref['med_days_active'] - df_OGI['med_days_active']),
                'med_leak_rate_dif': list(df_ref['med_leak_rate'] - df_OGI['med_leak_rate']),

                'cum_init_leaks_dif': list(df_ref['cum_init_leaks'] - df_OGI['cum_init_leaks']),
                'cum_missed_leaks_dif': list(df_ref['cum_missed_leaks'] - df_OGI['cum_missed_leaks']),
                'cum_OGI_surveys_dif': list(df_ref['cum_OGI_surveys'] - df_OGI['cum_OGI_surveys'])                             
                    }
    
                # Export
                df_new = pd.DataFrame(df_combine) 
                output_file = os.path.join(output_directory, 'comparison.csv')                        
                df_new.to_csv(output_file, index = False)                                                                                   

            return