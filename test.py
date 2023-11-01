from vnstock import *
import pandas as pd
from unidecode import unidecode
import os

file_listcompanies_path = 'ListCompanies.xlsx'
file_companyOverview_path = 'companyOverview.xlsx'

def exportListCompanies():
    listCompanies = listing_companies(live=False)
    # print(">>>listing_companies :\n",listCompanies);
    data = pd.DataFrame(listCompanies)
    header = data.columns
    # print(">>>header :\n",header);
    subset_data = data[['ticker', 'comGroupCode', 'organName', 'organShortName',
                'organTypeCode', 'comTypeCode', 'icbName']]

    unique_icbNames = data['icbName'].unique()
    print(">>>unique_icbNames :\n",unique_icbNames);
    subset_data.to_excel(file_listcompanies_path, sheet_name="A_tong" ,index=False)

    icb_data_dict = {}

    for icbName in unique_icbNames:
        icbName_data = subset_data[subset_data['icbName'] == icbName]
        icb_data_dict[icbName] = icbName_data

    with pd.ExcelWriter(file_listcompanies_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        for icbName, icb_data in icb_data_dict.items():
            sheet_name = unidecode(icbName).replace(" ", "_")[:31]
            icb_data.to_excel(writer, sheet_name=sheet_name, index=False)

def exportcompany_overview(ticket):
    companyOverview = company_overview(ticket)
    print(">>>companyOverview :\n",companyOverview);
    companyOverview.to_excel(file_companyOverview_path, sheet_name="tong_quan" ,index=False)
    companyProfile = company_profile (ticket)
    with pd.ExcelWriter(file_companyOverview_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        sheet_name = "companyProfile"
        companyProfile.to_excel(writer, sheet_name=sheet_name, index=False)

def exportCompanyOfficers (symbol='HPG'):
    companyOfficers = company_officers (symbol=symbol, page_size=20, page=0)
    with pd.ExcelWriter(file_companyOverview_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        sheet_name = "CompanyOfficers"
        companyOfficers.to_excel(writer, sheet_name=sheet_name, index=False)

def exportCompanyOfficers (symbol='HPG'):
    financialRatio = financial_ratio("HPG", 'quarterly', True)
    with pd.ExcelWriter(file_companyOverview_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        sheet_name = "financialRatio"
        financialRatio.to_excel(writer, sheet_name=sheet_name, index=True)
    
def main():
    print("Chương trình bắt đầu.")
    
    
    # exportListCompanies()
    # exportcompany_overview(ticket="HPG")
    # exportCompanyOfficers('HPG')
    # exportCompanyOfficers('HPG')
    financialRatioCompare = financial_ratio_compare (symbol_ls=["CTG", "TCB", "ACB"], industry_comparison=True, frequency='Yearly', start_year=2010)
    print(">>>financialRatioCompare :\n",financialRatioCompare)
    with pd.ExcelWriter(file_companyOverview_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        sheet_name = "financialRatioCompare"
        financialRatioCompare.to_excel(writer, sheet_name=sheet_name, index=True)
    print("Chương trình kết thúc.")

    


if __name__ == "__main__":
    main()
