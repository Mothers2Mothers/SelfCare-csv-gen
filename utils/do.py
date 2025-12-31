import streamlit as st
import pandas as pd
import io

# path = r"C:\Users\Siphiwe Themba\Desktop\code\files\2025 Self-Care Outputs (Q2).xlsx"
# path2 = r"C:\Users\Siphiwe Themba\Desktop\code\files\DHIS2 events (Q3).csv"

def run_pipeline(path2, curr, path=None):

    # sco = pd.read_excel(path)  # self care outputs  -  the one we must match
    de = pd.read_csv(path2)  # dhis2 events

    # if isinstance(sco, pd.DataFrame):
    #     print(sco.info())

    st.write("Processing Starting...")

    st.write(de.head())

    st.write(de.info())

    de.columns = de.columns.str.strip()

    # de['DSC 14   Positive relationships with co-workers'].unique()

    # de['DSC  19  Ask for support from family and friends'].unique()


    # ## Actions
    # - group cols to domains (physical, emotional, spiritual, professional, personal/social, financial, and psychological)
    # - assign scores: 1: Never, 2: Rarely, 3: Sometimes, 4: Often, 5: All the time
    # - agg avg per domain

    df = de.rename(columns={'DSC  28   Access psychotherapy':'PSYCHOLOGICAL_Access_psychotherapy',
                            'DSC 13  Maintain work-life balance':'PROFESSIONAL_Maintain_work-life_balance', 
                            'DSC 10  Meditate':'SPIRITUAL_Meditate',
                            'DSC  19  Ask for support from family and friends':'PERSONAL/SOCIAL_Ask_for_support_from_family_and_friends', 
                            'DSC 4 Medical check-ups,':'PHYSICAL_Medical_check-ups', 
                            'DSC  27    Learn new skills':'PSYCHOLOGICAL_Learn_new_skills',
                            'DSC 5  Engage in positive activities':'PHYSICAL_Engage_in_positive_activities', 
                            'DSC  10  Spend time in nature':'SPIRITUAL_Spend_time_in_nature',
                            'DSC  9   Self-reflection':'SPIRITUAL_Self-reflection', 
                            'DSC  2 Good sleep habits':'PHYSICAL_Good_sleep_habits',
                            'DSC 15   Time management skills':'PROFESSIONAL_Time_management_skills', 
                            'DSC 12  Pursue meaningful work':'PROFESSIONAL_Pursue_meaningful_work', 
                            'DSC  26    Pursue new interests':'PSYCHOLOGICAL_Pursue_new_interests',
                            'DSC  1eat regular and healthy meals,':'PHYSICAL_Eat_regular_and_healthy_meals',
                            'DSC 25  Journal':'PSYCHOLOGICAL_Journal',
                            'DSC 17  Make time for family and friends':'PERSONAL/SOCIAL_Make_time_for_family_and_friends',
                            'DSC  20  Understand how finances impact your quality of life':'FINANCIAL_Understand_how_finances_impact_your_quality_of_life',
                            'DSC  7  Express emotions in a healthy way':'EMOTIONAL_Express_emotions_in_a_healthy_way', 
                            'DSC 3  Regular exercise':'PHYSICAL_Regular_exercise',
                            'DSC 16    Healthy relationships':'PERSONAL/SOCIAL_Healthy_relationships',
                            'DSC  6  Acknowledge own accomplishments':'EMOTIONAL_Acknowledge_own_accomplishments',
                            'DSC  11  Explore spiritual connections':'SPIRITUAL_Explore_spiritual_connections',
                            'DSC 18  Schedule dates with partner or spouse':'PERSONAL/SOCIAL_Schedule_dates_with_partner_or_spouse',
                            'DSC  8   Read inspirational literature':'SPIRITUAL_Read_inspirational_literature',
                            'DSC  21   Create a budget or financial plan':'FINANCIAL_Create_a_budget_or_financial_plan', 
                            'DSC  22   Pay off debt':'FINANCIAL_Pay_off_debt',
                            'DSC 24  Disconnect from electrical devices':'PSYCHOLOGICAL_Disconnect_from_electrical_devices',
                            'DSC  23   Take time for yourself':'PSYCHOLOGICAL_Take_time_for_yourself',
                            'DSC  28  Life coaching or counselling support.':'PSYCHOLOGICAL_Life_coaching_or_counselling_support',
                            'DSC 14   Positive relationships with co-workers':'PROFESSIONAL_Positive_relationships_with_co-workers'})

    df['EMOTIONAL_Medical_check-ups'] = df['PHYSICAL_Medical_check-ups']
    df['Person'] = de[['First Name', 'Surname']].fillna('').agg(' '.join, axis=1).str.strip()

    cols = ['PHYSICAL_Eat_regular_and_healthy_meals', 'PHYSICAL_Good_sleep_habits',
        'PHYSICAL_Regular_exercise', 'PHYSICAL_Engage_in_positive_activities',
        'PHYSICAL_Medical_check-ups',
        'EMOTIONAL_Acknowledge_own_accomplishments',
        'EMOTIONAL_Express_emotions_in_a_healthy_way',
        'EMOTIONAL_Medical_check-ups',
        'SPIRITUAL_Read_inspirational_literature', 'SPIRITUAL_Self-reflection',
        'SPIRITUAL_Meditate', 'SPIRITUAL_Explore_spiritual_connections',
        'SPIRITUAL_Spend_time_in_nature', 'PROFESSIONAL_Pursue_meaningful_work',
        'PROFESSIONAL_Maintain_work-life_balance',
        'PROFESSIONAL_Positive_relationships_with_co-workers',
        'PROFESSIONAL_Time_management_skills',
        'PERSONAL/SOCIAL_Healthy_relationships',
        'PERSONAL/SOCIAL_Make_time_for_family_and_friends',
        'PERSONAL/SOCIAL_Schedule_dates_with_partner_or_spouse',
        'PERSONAL/SOCIAL_Ask_for_support_from_family_and_friends',
        'FINANCIAL_Understand_how_finances_impact_your_quality_of_life',
        'FINANCIAL_Create_a_budget_or_financial_plan', 'FINANCIAL_Pay_off_debt',
        'PSYCHOLOGICAL_Take_time_for_yourself',
        'PSYCHOLOGICAL_Pursue_new_interests', 'PSYCHOLOGICAL_Learn_new_skills',
        'PSYCHOLOGICAL_Access_psychotherapy',
        'PSYCHOLOGICAL_Life_coaching_or_counselling_support',
        'PSYCHOLOGICAL_Disconnect_from_electrical_devices',
        'PSYCHOLOGICAL_Journal']

    mapping = {r'^\s*never\s*$': 1, r'^\s*not\s*at\s*all\s*$': 1,
            r'^\s*rarely\s*$': 2,
            r'^\s*sometimes\s*$': 3,
            r'^\s*often\s*$': 4,
            r'^\s*all\s*the\s*time\s*$': 5
        }
    for col in cols:
        if col not in df.columns:
            st.write(f"Missing column: {col}")
            continue
        df[col] = df[col].astype(str).str.lower().replace(mapping, regex=True)
        # print(col, "\t", df[col].unique())
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df = df.drop(columns=['First Name', 'Surname'])

    st.write(df.info())

    qrtrs = ['2026-01-01', '2026-04-01', '2026-07-01', '2026-10-01']

    current_month = curr.month

    quarter_index = (current_month - 1) // 3

    q = qrtrs[quarter_index]
    
    st.write("Length of total df:\t", len(df))
    df['Last updated on'] = pd.to_datetime(df['Last updated on'], errors='coerce')
    df_rec = df[df['Last updated on']>=q]
    st.write("Length of filtered df:\t", len(df_rec))

    ## done
    # - add the domain prefixes
    # - cols 'EMOTIONAL_Medical_check-ups' and 'PHYSICAL_Medical_check-ups' have same answer
    # - col 'Person' = 'First Name' + 'Surname'
    # - encode the numeric cols
    # - filter on date

    domains = ["physical", "emotional", "spiritual", "professional", "personal", "financial", "psychological"]

    for dom in domains:
        group = [col for col in df_rec.columns if dom in col.lower()]

        if group:
            df_rec[dom] = df_rec[group].sum(axis=1)

    st.write(df_rec.head())

    df_rec['Month'] = 'Oct-25'

    df_rec = df_rec.drop(columns=['Event', 'Program stage', 'Event date', 'Stored by', 'Created by',
        'Last updated by', 'Last updated on', 'Scheduled date',
        'Enrollment date', 'Incident date', 'Tracked entity instance',
        'Program instance', 'Geometry', 'Longitude', 'Latitude',
        'Organisation unit name', 'Organisation unit name hierarchy',
        'Organisation unit code', 'Program status', 'Event status',
        'Organisation unit'])

    output = io.StringIO()  # StringIO creates an in-memory file object
    df_rec.to_csv(output, index=False)
    output.seek(0)

    st.write("Processing Finished...")

    return output
