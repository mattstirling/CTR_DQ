'''
Created on Jan 20, 2016

@author: mstirling
'''
import time

#control variables
bWriteReport = 1

#file variables
in_folder = 'C:/Temp/python/in/'
in_file = 'Comparison Summary V3.56 vs V3.21.txt'
out_folder = 'C:/Temp/python/out/'
table_out_file = in_file + '_tables_' + time.strftime("%Y%m%d") + '.txt'
summary_out_file = in_file + '_changes_' + time.strftime("%Y%m%d") + '.txt'

#tables to look for
'''
table_list = ['BOND_FORWARD_L',
        'BOND_FUTURE_L',
        'BOND_FUTURE_OPTION_L',
        'BOND_L',
        'BOND_OPTION_L',
        'BRAZIL_IR_FUTURE_L',
        'CNV_BND_L',
        'COLLATERAL_L',
        'COMMODITY_FUTURE_L',
        'COMMODITY_OPTION_L',
        'EQUITY_FUTURE_L',
        'EQUITY_L',
        'EQUITY_OPTION_ETD_L',
        'EQUITY_VECTOR_L',
        'FRN_L',
        'FX_FORWARD_L',
        'FX_FUTURE_BRZ_L',
        'FX_FUTURE_L',
        'FX_OPTION_OTC_L',
        'FX_RATE_L',
        'IR_FUTURE_L',
        'IR_FUTURE_OPTION_L',
        'LANCELOT_CARDS_ID_EXP',
        'LANCELOT_COLLATERAL_EXP',
        'LANCELOT_CURRENCY_DATA_EXP',
        'LANCELOT_DEAL_L',
        'LANCELOT_TRADE_EXP',
        'LANCELOT_UNDERLYING_EXP',
        'PM_LOAN_L',
        'REPO_EXP',
        'REPO_L',
        'RISKWATCH_BONDOPTION_EXP',
        'RISKWATCH_BOND_EXP',
        'RISKWATCH_COLLATERAL_EXP',
        'RISKWATCH_EQUITY_EXP',
        'RISKWATCH_FRN_EXP',
        'RISKWATCH_FX_FORWARD_EXP',
        'RISKWATCH_REPO_EXP',
        'RISKWATCH_SBL_COLLATERAL_EXP',
        'RISKWATCH_SBL_EXPOSURE_EXP',
        'RISKWATCH_TBILL_EXP',
        'SBL_COLLATERAL_L',
        'SWAP_L',
        'T_BILL_L']
    '''
    
table_list = ['BOND_L',
        'CNV_BND_L',
        'EQUITY_L',
        'FRN_L',
        'FX_FORWARD_L',
        'FX_RATE_L',
        'LANCELOT_TRADE_EXP',
        'LANCELOT_UNDERLYING_EXP',
        'REPO_L',
        'RISKWATCH_BOND_EXP',
        'RISKWATCH_SBL_EXPOSURE_EXP',
        'SBL_COLLATERAL_L',
        'SBL_EXPOSURE_L',
        'TRADE_HOLDING_MEASURES_L',
        'T_BILL_L']
    
f_table_out = open(out_folder + table_out_file, 'w')
f_summary_out = open(out_folder + summary_out_file, 'w')
b_include_this_table = 0
b_begin_writing = 0
with open(in_folder + in_file, 'r') as this_in_file:
    line_count = 0
    for line in this_in_file:
        line_count+=1
        
        if '<Table>' in line:
            #check if this table is in scope
            b_include_this_table = 0
            for table in table_list:
                if (table in line) and (table + '_A' not in line): 
                    f_table_out.write(str(line_count) + ',' + line)
                    b_include_this_table = 1 
                    b_begin_writing = 1
        
        if b_include_this_table:
            if 'Columns' in line:b_begin_writing=1
            if '<Options>' in line or 'Indexes:' in line:b_begin_writing = 0
            
            if b_begin_writing: 
                
                f_summary_out.write(str(line_count) + ',' + line)
                    
                    
                    
                    
f_table_out.close()

print 'done.'  