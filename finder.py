try:
    import streamlit as st
    import json
    import xmltodict
    import os
    import re
    from collections import defaultdict
    from fpdf import FPDF
    import base64

except:
    import pip
    pip.main(['install', 'streamlit'])
    pip.main(['install', 'json'])
    pip.main(['install', 'xmltodict'])
    pip.main(['install', 'fpdf'])
    
    import streamlit as st
    import json
    import xmltodict
    import os
    import re
    from collections import defaultdict
    from fpdf import FPDF
    import base64
    
def fun(path):
    # returns the final component of a url
    f_url = os.path.basename(path)
      
    # convert the url into link
    return '<a href="{}">{}</a>'.format(path, f_url)
    
def usable_code_gen(code, try_again = False):
    code_num = re.findall('[0-9]+', code)[0]
    if try_again == True:
        return 'UH0'+code_num
    return 'UH'+code_num
    
def refresh_json():
    path = 'G:\\My Drive\\Estimator\\Jobs'
    path_onsite = 'G:\\My Drive\\Estimator\\Jobs\\ONSITE JOBS'

    dirs = os.listdir( path )
    dirs_onsite = os.listdir( path_onsite )
    code_dict, address_dict = {}, {}
    for dir in dirs:
        if dir.split()[0][0] == 'U':

            dir_path = path +'\\'+ dir
            code = re.findall('U[H 0]*[0-9]+', dir_path)[0]

            address = re.findall('Lot.+', dir_path)[0]

            code_dict[code] = path +'\\'+ dir
            address_dict[address] = path +'\\'+ dir

    for dir in dirs_onsite:
        if dir.split()[0][0] == 'U':

            dir_path = path_onsite +'\\'+ dir
            code = re.findall('U[H 0]*[0-9]+', dir_path)[0]

            address = re.findall('Lot.+', dir_path)[0]

            code_dict[code] = path_onsite +'\\'+ dir
            address_dict[address] = path_onsite +'\\'+ dir

    out_file = open("path.json", "w")

    json.dump({"Code": code_dict, "Address": address_dict}, out_file, indent = 6)

    out_file.close()
    
    return {"Code": code_dict, "Address": address_dict}

if st.button('Refresh Jobs GDrive main'):
    path_dict = refresh_json()
    
    f = open("path.json")
    path_dict = json.load(f)


    with open("JobTest.xml") as xml_file:
        data_dict = xmltodict.parse(xml_file.read())

    json_data = json.dumps(data_dict)
    data = json.loads(json_data)

    jobs_list = data["Databuild"]["Jobs"]["JobsRecord"]
    contacts_list = data["Databuild"]["Contacts"]["ContactsRecord"]

tab1, tab2, tab3 = st.tabs(["Jobs", "Cost Centers", "General Ledger Accounts"])

f = open("path.json")
path_dict = json.load(f)
    
with open("JobTest.xml") as xml_file:
    data_dict = xmltodict.parse(xml_file.read())

json_data = json.dumps(data_dict)
data = json.loads(json_data)

try:
    jobs_list = data["Databuild"]["Jobs"]["JobsRecord"]
    contacts_list = data["Databuild"]["Contacts"]["ContactsRecord"]
except:
    jobs_list = data["Databuild"]["Jobs"][0]["JobsRecord"]
    contacts_list = data["Databuild"]["Contacts"][0]["ContactsRecord"]


with tab1:
    job_code_list, address_list, customer_list = {}, {}, {}
    for num, job in enumerate(jobs_list):
        res = jobs_list[num]|contacts_list[num]

        customer_list[res["Name"]] = res
        address_list[res["Site_Address"]] = res
        job_code_list[res["Code"]] = res


    variable_chosen = st.selectbox(
        'Choose your field',
        ['Customer', 'Address', 'Job Code', 'All']
    )

    if variable_chosen == 'Customer':

        customer_chosen_list = st.multiselect(
            'Choose a Customer',
           list(customer_list))

        for customer_chosen in customer_chosen_list:
            st.json(customer_list[customer_chosen])

    elif variable_chosen == 'Address':

        address_chosen_list = st.multiselect(
            'Choose an Address',
            list(address_list))

        for address_chosen in address_chosen_list:
            st.write(address_list[address_chosen]["Code"])
            st.json(address_list[address_chosen])

            # Changing code to usable job code
            specific_code = address_list[address_chosen]["Code"]
            
            try:
                specific_code_usable = usable_code_gen(specific_code)
                path = path_dict["Code"][specific_code_usable]
            except:
                specific_code_usable = usable_code_gen(specific_code, True)
                path = path_dict["Code"][specific_code_usable]

            st.write(path)

            dirs = os.listdir( path )
            
            dir_selected = st.selectbox("", dirs)
            
            file_in_dirs_selected = os.listdir(path + "\\" + dir_selected)
            
            st.write(file_in_dirs_selected)

    elif variable_chosen == 'Job Code':

        job_code_chosen_list2 = st.multiselect(
            'Choose a Job Code',
            list(job_code_list))

        for job_code_chosen in job_code_chosen_list2:
            st.json(job_code_list[job_code_chosen])

            specific_code = job_code_chosen
            
            try:
                specific_code_usable = usable_code_gen(specific_code)
                path = path_dict["Code"][specific_code_usable]
            except:
                specific_code_usable = usable_code_gen(specific_code, True)
                path = path_dict["Code"][specific_code_usable]

            path = path_dict["Code"][specific_code_usable]
            st.write(path)

            dirs = os.listdir( path )

            dir_selected = st.selectbox("", dirs)
            
            file_in_dirs_selected = os.listdir(path + "\\" + dir_selected)
            
            st.write(file_in_dirs_selected)
            
    elif variable_chosen == "All":
        
        customer_chosen_list2 = st.multiselect(
            'Choose a Customer',
           list(customer_list))

        for customer_chosen in customer_chosen_list2:
            st.json(customer_list[customer_chosen])
            
        
        address_chosen_list2 = st.multiselect(
            'Choose an Address',
            list(address_list))

        for address_chosen in address_chosen_list2:
            st.write(address_list[address_chosen]["Code"])
            st.json(address_list[address_chosen])

            # Changing code to usable job code
            specific_code = address_list[address_chosen]["Code"]
            
            try:
                specific_code_usable = usable_code_gen(specific_code)
                path = path_dict["Code"][specific_code_usable]
            except:
                specific_code_usable = usable_code_gen(specific_code, True)
                path = path_dict["Code"][specific_code_usable]

            st.write(path)

            dirs = os.listdir( path )
            
            dir_selected = st.selectbox("", dirs)
            
            file_in_dirs_selected = os.listdir(path + "\\" + dir_selected)
            
            st.write(file_in_dirs_selected)
            
            
        job_code_chosen_list2 = st.multiselect(
            'Choose a Job Code',
            list(job_code_list))

        for job_code_chosen in job_code_chosen_list2:
            st.json(job_code_list[job_code_chosen])

            specific_code = job_code_chosen
            
            try:
                specific_code_usable = usable_code_gen(specific_code)
                path = path_dict["Code"][specific_code_usable]
            except:
                specific_code_usable = usable_code_gen(specific_code, True)
                path = path_dict["Code"][specific_code_usable]

            path = path_dict["Code"][specific_code_usable]
            st.write(path)

            dirs = os.listdir( path )

            dir_selected = st.selectbox("", dirs)
            
            file_in_dirs_selected = os.listdir(path + "\\" + dir_selected)
            
            st.write(file_in_dirs_selected)
        
            
import pandas as pd
construction = pd.read_csv("costCentreConstruction.csv").reset_index().rename(columns = {"index": "code"})
construction_col = construction.columns
expenses = pd.read_csv("costCentreExpenses.csv").reset_index()
expenses_col = expenses.columns
construction_GL = [5.13,5.11,5.11,5.11,5.12,5.11,5.11,5.11,5.11,5.11,5.11,5.11,5.11,5.11,5.11,5.11,5.11,5.12,5.11,5.11,5.12,5.12,5.11,5.12,5.12,5.11,5.12,5.12,5.11,5.12,5.11,5.11,5.12,5.11,5.11,5.11,5.11,5.11,5.12,5.12,5.11,5.11,5.12,5.12,5.11,5.11,5.12,5.11,5.12,5.12,5.12,5.11,5.11,5.11,5.12,5.12,5.12,5.11,5.11,5.11,5.11,5.11,5.12,5.12,5.12,5.11,5.11,5.11,5.11,5.12, 5.11, 5.12, 5.11, 5.11, 5.12, 5.11, 5.11, 5.11, 5.11, 5.11, 5.11, 5.11, 5.11, 5.11, 5.11, 5.11, 5.12, 5.12, 5.12, 5.11, 5.12, 5.11, 5.11]

construction["GLAccount"] = construction_GL

GL_dict = {5.11: "Subcontractors", 5.12: "Materials", 5.13: "Design and Consultants"}
construction_GL_name = []
for GL in construction_GL:
    construction_GL_name.append(GL_dict[GL])
    
construction["GL_info"] = construction_GL_name

construction.to_csv("costCentreConstruction_GL.csv")

with tab2:
    construction_code = st.selectbox("Choose a Construction Code", list(construction["code"]))
    construction_category_given = construction[construction["code"] == construction_code][construction_col[-1]].values[0]
    
    st.write(str(construction_category_given))
    st.write(str(construction[construction[construction_col[-1]] == construction_category_given]["GLAccount"].values[0]))
    st.write(construction[construction[construction_col[-1]] == construction_category_given]["GL_info"].values[0])
    
    construction_category = st.selectbox("Choose a Construction Category", list(construction[construction_col[-1]]))
    construction_code_given = construction[construction[construction_col[-1]] == construction_category]["code"].values[0]
        
    st.write(str(construction_code_given))
    st.write(str(construction[construction["code"] == construction_code_given]["GLAccount"].values[0]))
    st.write(construction[construction["code"] == construction_code_given]["GL_info"].values[0])
    
    expenses_code = st.selectbox("Choose a Expenses Code", list(expenses["code"]))
    expenses_category_given = expenses[expenses["code"] == expenses_code][expenses_col[-1]].values[0]
    
    st.write(expenses_category_given)
    
    expenses_category = st.selectbox("Choose a Expenses Category", list(expenses[expenses_col[-1]]))
    expenses_code_given = expenses[expenses["code"] == expenses_code]["code"].values[0]
    
    st.write(expenses_code_given)
    

GL_accounts = pd.read_csv("GeneralLedgerFull.csv")
with tab3:
    GL_code = st.selectbox("Choose a General Ledger Code", list(GL_accounts["code"]))
    GL_name_given = GL_accounts[GL_accounts["code"] == GL_code]["A/c code"].values[0]
    
    st.write(GL_name_given)
    
    GL_name = st.selectbox("Choose a General Ledger Name", list(GL_accounts["A/c code"]))
    GL_code_given = GL_accounts[GL_accounts["A/c code"] == GL_name]["code"].values[0]
    
    st.write(str(GL_code_given))
    
    st.dataframe(GL_accounts.iloc[:, 1:4])

        
        