# works for ahern OER


import numpy as np
import sys
import pprint as pp
import time
import re
import json


def make_dict(PATH, filename):
    fields = {}
    with open(PATH + filename, 'r') as f:
        for line in f:
            line = line[:line.index('\n')]
            fields[line] ='NO_VALUE'
    return fields

def get_eval_id(file, fields):
    print('get_eval_id')
    count = 0
    for line in file:
        if count == 3:
            break
        count +=1
        m = re.search(r"(H.?QDA#)", line)
        if m:
            id = re.search(r"[0-9]+", line)
            fields['EVAL_ID'] = id.group()
            break
    return fields

def get_name_id_rank_date_of_rank(file, fields):
    print('get_ind_name')
    for line in file:
        t = re.search(r"(\(YYYYMMDD\).+)(\(Status Code\))", line)
        # t = re.search(r"(\(YYYYMMDD\).+)", line)
        if t:
            temp = file.readline()
            all = re.search(r"(\d{10}|\d{9}) (\w\w\w?\w?) (\d{8}) (\w\w)", temp)
            # print('found line: ' + temp)

            IND_NM = temp[:all.start()-1]
            DOD_ID = all.group(1)
            RANK = all.group(2)
            RANK_DT = all.group(3)
            OFF_BAS_BR_CD = all.group(4)

            fields['IND_NM'] = IND_NM
            fields['SSN_DOD_ID'] = DOD_ID
            fields['RANK_AB'] = RANK
            fields['RANK_DT'] = RANK_DT
            fields['OFF_BAS_BR_CD'] = OFF_BAS_BR_CD
            break
    return fields

def get_unit_uic_reason(file, fields):
    print('get_unit')
    for line in file:
        t = re.search(r"ZIP", line)
        if t:
            temp = file.readline()
            # print('temp: '+ temp)
            EVAL_RPT_RSN_CD_match = re.search(r"\d+.?\|.?\w*.*", temp)
            EVAL_RPT_RSN_CD = EVAL_RPT_RSN_CD_match.group().replace('\n', '')
            # print('EVAL_RPT_RSN_CD: ' + EVAL_RPT_RSN_CD)

            temp = temp[:EVAL_RPT_RSN_CD_match.start()]
            # print('temp: ' + temp)
            UIC_CD = re.findall(r"\b\w{6}\b", temp)[-1]
            # print('UIC_CD: ' + UIC_CD)

            UNIT = temp[:temp.index(UIC_CD)]
            # print('UNIT: ' + UNIT)

            fields['UNIT'] = UNIT
            fields['UIC_CD'] = UIC_CD
            fields['EVAL_RPT_RSN_CD'] = EVAL_RPT_RSN_CD
            # fields['RANK_DT'] = RANK_DT
            break
    return fields

def get_times_months_enclosures_email(file, fields):
    print('get_times')
    for line in file:
        # print(line)
        t = re.search(r"THRU.?\(YYYYMMDD\)", line)
        if t:
            # print('found t. line: ' + line)
            temp = file.readline()
            # print('trash: ' + trash)
            while temp == '\n':
                temp = file.readline()
            # temp = file.readline()
            # print('temp: ' + temp)
            # print('temp ' + temp)
            all = re.search(r"(\d{8}) (\d{8})", temp)
            EVAL_PD_ST_DT = all.group(1)
            EVAL_PD_END_DT = all.group(2)
            # print('EVAL_PD_ST_DT: ' +EVAL_PD_ST_DT)
            # print('EVAL_PD_END_DT: ' +EVAL_PD_END_DT)
            MNTHS_match = re.search(r" \d{2} | \d{1} ", temp)
            MNTHS = MNTHS_match.group(0).replace(" ", '')
            # print('MNTHS: '+MNTHS)

            temp = temp[MNTHS_match.end():]
            # print('new temp: '+temp)
            GOVT_EMAIL_ADDR_TX_match = re.search(r"\w\w.*.mil", temp, re.IGNORECASE)
            GOVT_EMAIL_ADDR_TX = GOVT_EMAIL_ADDR_TX_match.group(0).replace(" ", '')
            temp = temp[:GOVT_EMAIL_ADDR_TX_match.start()]
            # print('new temp: '+temp)

            ENCLOSURES_match = re.search(r"\d", temp)
            ENCLOSURES = ENCLOSURES_match.group(0).replace(" ", '')
            NON_RATED_CODES = temp[:ENCLOSURES_match.start()]


            fields['EVAL_PD_ST_DT'] = EVAL_PD_ST_DT
            fields['EVAL_PD_END_DT'] = EVAL_PD_END_DT
            fields['MNTHS'] = MNTHS
            fields['GOVT_EMAIL_ADDR_TX'] = GOVT_EMAIL_ADDR_TX
            fields['x_ENCLOSURES'] = ENCLOSURES
            if NON_RATED_CODES:
                # if not blank string
                fields['EVAL_RPT_TYP_CD'] = NON_RATED_CODES
            break
    return fields

def get_rater_info1(file, fields):
    print('get_rater_info1')
    for line in file:
        t = re.search(r"a3.\W*RANK\W*a4.\WPOSITION", line)
        # for i in range(0, 5):
        #     temp = file.readline()
        #     print(str(i) + temp)
        # break
        if t:
            temp = file.readline()
            right_line = re.search(r"\d{9}|\d{10}", temp)
            while right_line == None:
                # print('temp == None so read again...')
                temp = file.readline()
                # print('new temp: ' + temp)
                right_line = re.search(r"\d{9}|\d{10}", temp)

            # print('temp reads: ' + temp)
            split1 = re.search(r"\d", temp)
            RATER = temp[:split1.start()]
            RATER_RANK_match = re.search(r"\d \w* ", temp)
            RATER_RANK = temp[RATER_RANK_match.start()+2:RATER_RANK_match.end()-1]
            RATER_TITLE = temp[RATER_RANK_match.end():-1]

            fields['RATER'] = RATER
            fields['RATER_RANK'] = RATER_RANK
            fields['RATER_TITLE'] = RATER_TITLE
            break
    return fields

def get_rater_email(file, fields):
    print('get_rater_info')
    for line in file:
        t = re.search(r"RATER SIGNATURE a", line)
        # print('found target' + line)

        if t:
            temp = file.readline()
            # print('temp: ' + temp)
            right_line = re.search(r"\w\w.*.mil", temp, re.IGNORECASE)
            while right_line == None:
                # print('not right line. reading temp again...')
                temp = file.readline()
                print('new temp: ' + temp)
                right_line = re.search(r"\w\w.*.mil", temp, re.IGNORECASE)
                if 'NAME OF INTERMEDIATE RATER' in temp:
                    print('cannot find rater email')
                    break
            # print('found right line. temp reads: ' + temp)
            RATER_EMAIL = right_line.group(0)

            fields['RATER_EMAIL'] = RATER_EMAIL.replace(' ', '')

            break
    return fields

def get_senior_rater_info1(file, fields):
    print('get_senior_rater_info')
    for line in file:
        t = re.search(r"NAME OF SENIOR RATER", line)
        # print('found target' + line)

        if t:
            temp = file.readline()
            # print('temp: ' + temp)
            SENIOR_RATER_ID_match = re.search(r"\d{10}|\d{9}", temp)
            while SENIOR_RATER_ID_match == None:
                # print('not right line. reading temp again...')
                temp = file.readline()
                # print('new temp: ' + temp)
                SENIOR_RATER_ID_match = re.search(r"\d{10}|\d{9}", temp)
                if 'SENIOR RATER\'S ORGANIZATION' in temp:
                    print('cannot find senior rater info')
                    break
            # print('found right line. temp reads: ' + temp)
            SENIOR_RATER = temp[:SENIOR_RATER_ID_match.start()-1]
            temp = temp[SENIOR_RATER_ID_match.end():]
            SENIOR_RANK_match = re.search(r" \w*", temp)
            SENIOR_RANK = temp[:SENIOR_RANK_match.end()]
            SENIOR_TITLE = temp[SENIOR_RANK_match.end():-1]


            fields['SENIOR_RATER'] = SENIOR_RATER
            fields['SENIOR_RANK'] = SENIOR_RANK.replace(' ', '')
            fields['SENIOR_TITLE'] = SENIOR_TITLE

            break
    return fields

def get_senior_rater_info2(file, fields):
    print('get_senior_rater_org and stuff...')
    for line in file:
        # print(line)
        t = re.search(r"(.*) (..) (USAR|RA)", line)
        if t:
            SENIOR_ORG = t.group(1)
            SENIOR_BRNCH = t.group(2)
            fields['SENIOR_BRNCH'] = SENIOR_BRNCH
            fields['SENIOR_ORG'] = SENIOR_ORG
            email = re.search(r"(\w*\..*.mil)", line, re.IGNORECASE)
            # print('looked for email in: ' + line)

            while not email:
                next = file.readline()
                email = re.search(r"(\w*\..*.mil)", line, re.IGNORECASE)
            if email:
                # print('found email in line: ' + line)
                SENIOR_EMAIL = email.group(1).replace(' ', '')
                # print('senior email: ' + SENIOR_EMAIL)
                fields['SENIOR_EMAIL'] = SENIOR_EMAIL

            break
    return fields

# def get_senior_rater_email(file, fields):
#     print('='*50)
#     # print('get_senior_rater_email')
#     for line in file:
#         print(line)
#         email = re.search(r"(\w*\..*.mil)", line)
#         if email:
#             # print('found email ----- ' + line)
#             # print('found the line: ' + line)
#             next = file.readline()
#             while next == '\n':
#                 next = file.readline()
#             if 'SENIOR RATER PHONE NUMBER' in next:
#                 SENIOR_EMAIL = email.group().replace(' ', '')
#
#                 fields['SENIOR_EMAIL'] = SENIOR_EMAIL
#                 break
#
#     return fields

def get_principal_duty_tx_and_mos(file, fields):
    print('get_principal_duty_tx_and_mos')
    for line in file:
        # print(line)
        if 'PRINCIPAL DUTY TITLE' in line:
            # print('line: ' + line)
            next = file.readline()
            # print('next line: ' + next)
            next_list = next.split()
            MOS_DSG_TX = next_list[-1]
            # print('mos dsg tx: ' + MOS_DSG_TX)
            DUTY_TITLE_TX = next[:next.rindex(MOS_DSG_TX)]
            # print('duty title: '+DUTY_TITLE_TX)
            fields['MOS_DSG_TX'] = MOS_DSG_TX
            fields['DUTY_TITLE_TX'] = DUTY_TITLE_TX
            break
    return fields

def get_duty_des_tx(file, fields):
    print('get_duty_des_tx')
    DUTY_DESC_TX = ""
    for line in file:
        # print(line)
        if 'SIGNIFICANT DUTIES AND RESPONSIBILITIES' in line:
            next = file.readline()
            # print('next: ' + next)
            # print('next.isspace(): {}'.format(next.isspace()))
            while not next.isspace():
                DUTY_DESC_TX = DUTY_DESC_TX + next.replace('\n', ' ')
                next = file.readline()
                if 'PERFORMANCE EVALUATION' in next:
                    break
                if 'ATTRIBUTES' in next:
                    break

            fields['DUTY_DESC_TX'] = DUTY_DESC_TX
            break
    return fields

def get_height_weight_within_standard(file, fields):
    print('get_height_weight_within_standard')
    for line in file:
        # print(line)
        if 'APFT Pass' in line:
            print('hit APFT pass')
            result_end = re.search(r"Profile:", line).end()
            date_start = re.search(r"Date:", line).start()
            apft = re.search(r"\w+", line[result_end:date_start])
            if apft:
                APFT_RSLT_CD = apft.group()
                fields['APFT_RSLT_CD'] = APFT_RSLT_CD

            date_end = re.search(r"Date:", line).end()
            height_start = re.search(r"Height:", line).start()
            apft_date = re.search(r"\d{8}", line[date_end:height_start])
            if apft_date:
                APFT_DT = apft_date.group()
                fields['APFT_DT'] = APFT_DT

            PHYS_MEAS_HGT_IN_list = re.search(r"Height: \d*", line).group().split()
            PHYS_MEAS_HGT_IN = PHYS_MEAS_HGT_IN_list[-1]

            PHYS_MEAS_HGT_IN_list = re.search(r"Height: \d*", line).group().split()
            PHYS_MEAS_HGT_IN = PHYS_MEAS_HGT_IN_list[-1]

            PHYS_MEAS_WGT_LB_list = re.search(r"Weight: \d*", line).group().split()
            PHYS_MEAS_WGT_LB = PHYS_MEAS_WGT_LB_list[-1]

            BODY_FAT_STD_CD_list = line[re.search(r"Within Standard\?", line).end():].split()
            BODY_FAT_STD_CD = BODY_FAT_STD_CD_list[-1]

            fields['PHYS_MEAS_HGT_IN'] = PHYS_MEAS_HGT_IN
            fields['PHYS_MEAS_WGT_LB'] = PHYS_MEAS_WGT_LB
            fields['BODY_FAT_STD_CD'] = BODY_FAT_STD_CD
            break

        # elif '\"Profile\"' in line:
        #     print('hit profile part')
        #     next = file.readline()
        #     if 'Performance is Rated' in next:
        #         break
        #     while next.isspace():
        #         next=file.readline()
        #         if 'Performance is Rated' in next:
        #             break
        #     PHYS_FITNESS_TX = next.replace('\n', '')
        #     print('fitness text: ' + PHYS_FITNESS_TX)
        #     fields['PHYS_FITNESS_TX'] = PHYS_FITNESS_TX
        #     break
        # elif 'Performance is Rated' in next:
        #     break

    return fields

def get_phys_fitness_tx_broadening_operational(file, fields):
    print('get_phys_fitness_tx_broadening_operational')
    for line in file:
        # print(line)

        if '\"Profile\"' in line:
            # print('=====hit profile part')
            next = file.readline()
            while next.isspace():
                next=file.readline() # ensures next is not a blank line
            PHYS_FITNESS_TX = ""
            while not 'BROADENING' in next:
                PHYS_FITNESS_TX = PHYS_FITNESS_TX + next.replace('\n', ' ')
                next = file.readline()
                if 'Character:' in next:
                    break
                if 'DA FORM' in next:
                    break
            if 'BROADENING' in next:
                # print('=====found broadening')
                temp = file.readline()
                print('temp1: ' + temp)
                BRDING_match = re.search(r"\w.*;|, \w.*;|, \w.*", temp)
                if BRDING_match:
                    fields['BRDING'] = BRDING_match.group()
                temp = file.readline()
                # print('temp2: ' + temp)
                if 'OPERATIONAL' in temp:
                    # print('=====found operational')
                    temp = file.readline()
                    OPERAT = re.search(r"\w.*;|, \w.*;|, \w.*", temp).group()
                    fields['OPERAT'] = OPERAT
            if not PHYS_FITNESS_TX == "":
                fields['PHYS_FITNESS_TX'] = PHYS_FITNESS_TX
            break




    return fields


def get_rt_rating(file, fields):
    print('get_rt_rating')
    for line in file:
        if '67-10-1A' in line:
            next = file.readline()
            # print('next: ' + next)
            ratings = ['EXCELS', 'PROFICIENT', 'CAPABLE', 'UNSATISFACTORY']
            while not any(rating in next.upper() for rating in ratings):
                next = file.readline()
            RT_RATING = next.replace(' ', '').replace('\n', '')

            fields['RT_RATING'] = RT_RATING
            break
    return fields

def get_rt_num_ratings(file, fields):
    print('get_rt_num_ratings\n')
    for line in file:
        tbig = re.search(r"TOTAL RATINGS:.?\d* RATINGS THIS OFFICER:.?\d*", line)
        if tbig:

            t1 = re.search(r"TOTAL RATINGS:.?\d*", line)
            RATER_TOTAL = t1.group().split(':')[-1].replace(' ', '')


            t2 = re.search(r"RATINGS THIS OFFICER:.?\d*", line)
            RATER_RATED = t2.group().split(':')[-1].replace(' ', '')

            fields['RATER_TOTAL'] = RATER_TOTAL
            fields['RATER_RATED'] = RATER_RATED
            break
    return fields

def get_rt_comments(file, fields):
    print('get_rt_comments')
    RT_CMT = ''
    for line in file:
        print('line in file: ' + line)
        if 'Comments:' in line:
            print('line: ' + line)
            next = file.readline()
            print('next: ' + next)
            while next.isspace():
                print('while next.isspace()')
                next = file.readline()
            count = 0
            while not 'UNCLASSIFIED' in next:
                if count == 6:
                    print('hard count == 6')
                    break
                if 'INTERMEDIATE' in next:
                    break
                if 'SENIOR' in next:
                    break
                print('while not 67....')
                print('next is: ' + next)
                RT_CMT = RT_CMT + next.replace('\n', ' ')
                # print('RT_CMT: ' + RT_CMT)
                next = file.readline()
                count +=1


            fields['RT_CMT'] = RT_CMT
            break
    return fields

def get_sr_rating(file, fields):
    print('get_sr_rating')
    for line in file:
        if 'OFFICERS SENIOR RATED' in line:
            # print('line: ' + line)
            next = file.readline()
            potentials = ['MOST QUALIFIED', 'HIGHLY QUALIFIED', 'QUALIFIED', 'NOT QUALIFIED']
            while not any(potential in next for potential in potentials):
                next = file.readline()
                if 'SUCCESSIVE' in next.upper():
                    break
            # print('next: ' + next)
            SR_RATING = re.search(r"\w.*", next).group()
            fields['SR_RATING'] = SR_RATING
            break
    return fields

def get_sr_total_and_successive_assignments(file, fields):
    print('get_sr_total')
    for line in file:
        print(line)
        if 'SR:' in line:
            # print('line: ' + line)
            next = file.readline()
            print('next' + next)
            count = 0
            while not '67-10-2' in next:
                if count == 6:
                    break
                # print('unclassified not in next')
                t = re.search(r"TOTAL RATINGS: ?\d+", next)
                assignments = re.search(r"(\w.*), (\w.*), (\w.*)", next)
                if assignments:
                    fields['SUCCSIV'] = assignments.group(0)

                if t:
                    SENIOR_TOTAL = t.group().split(':')[-1].replace(' ', '')
                    fields['SENIOR_TOTAL'] = SENIOR_TOTAL
                next=file.readline()
                count += 1

            break
    return fields

# def get_sr_comments(file, fields):
#     # print('get_sr_comments')
#     SR_CMT = ''
#     for line in file:
#         # print('line in file: ' + line)
#         if 'COMMENTS ON POTENTIAL' in line:
#             print('line: ' + line)
#             next = file.readline()
#             # print('next: ' + next)
#             while next.isspace():
#                 next = file.readline()
#             while not next.isspace():
#                 SR_CMT = SR_CMT + next.replace('\n', ' ')
#                 # print('RT_CMT: ' + RT_CMT)
#                 next = file.readline()
#
#             fields['SR_CMT'] = SR_CMT
#             break
#     return fields

# def get_successive(file, fields):
#     # print('get_successive')
#     for line in file:
#         if 'SUCCESSIVE' in line:
#             # print('line: ' + line)
#             next = file.readline()
#             while next.isspace():
#                 next = file.readline()
#             SUCCSIV = next.replace('\n', '')
#             fields['SUCCSIV'] = SUCCSIV
#             break
#     return fields


### main
def main():
    print('=======67_10_2=========')
    # load text
    txt_filename= str(sys.argv[1])
    txt_name = txt_filename[0:txt_filename.index('.')]


    # streamlit
    TEXT_PATH = './data/text/'
    OUTPUT_PATH = './data/output/'
    fields = make_dict('./data/', 'dict_keys.txt')

    # local
    # TEXT_PATH = '../data/text/'
    # OUTPUT_PATH = '../data/output/'
    # fields = make_dict('../data/', 'dict_keys.txt')

    # pp.pprint(fields, sort_dicts = False)
    print('reading: ' + txt_filename)
    print('from: ' + TEXT_PATH)
    print('name: ' + txt_name + '\n')

    with open(TEXT_PATH + txt_filename) as file:
        print('successfully opened file\n')
        count = 0
        # for line in file:
        #     print('Line #{}: '.format(count))
        #     print(line)
        #     count += 1
        fields = get_eval_id(file, fields)
        fields = get_name_id_rank_date_of_rank(file, fields)
        fields = get_unit_uic_reason(file, fields)
        fields = get_times_months_enclosures_email(file, fields)
        fields = get_rater_info1(file, fields)
        fields = get_rater_email(file, fields)
        fields = get_senior_rater_info1(file, fields)
        fields = get_senior_rater_info2(file, fields)
        # fields = get_senior_rater_email(file, fields)
        fields = get_principal_duty_tx_and_mos(file, fields)
        # # ^ asumes that MOS_DSG_TX is OER recipient's MOS
        fields = get_duty_des_tx(file, fields)
        fields = get_height_weight_within_standard(file, fields)
        fields = get_phys_fitness_tx_broadening_operational(file, fields)
        fields = get_rt_rating(file, fields)
        fields = get_rt_num_ratings(file, fields)
        fields = get_rt_comments(file, fields)
        # # ^ assumes RATER_RATED is 'Ratings this Officer'
        fields = get_sr_rating(file, fields)
        fields = get_sr_total_and_successive_assignments(file, fields)
        # fields = get_sr_comments(file, fields)
        # fields = get_successive(file, fields)



    with open(OUTPUT_PATH+txt_name + '.json', 'w') as f:
        json.dump(fields, f, indent=4)
        print('saved oer data to json')
        print('path: ' + OUTPUT_PATH)
        print('name: ' + txt_name+'.json')
    # pp.pprint(fields, sort_dicts = False)










if __name__ == "__main__" :
    main()
