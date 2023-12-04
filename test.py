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

def exportFinancialRatioCompare (symbol='HPG'):
    financialRatioCompare = financial_ratio_compare (symbol_ls=["CTG", "TCB", "ACB"], industry_comparison=True, frequency='Yearly', start_year=2010)
    with pd.ExcelWriter(file_companyOverview_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        sheet_name = "financialRatioCompare"
        financialRatioCompare.to_excel(writer, sheet_name=sheet_name, index=True)

def exportFinancialReportIncomeStatement (symbol='HPG'):
    financialReport = financial_report (symbol=symbol, report_type='IncomeStatement', frequency='Quarterly')
    with pd.ExcelWriter(file_companyOverview_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        sheet_name = "Bao_cao_doanh_thu"
        financialReport.to_excel(writer, sheet_name=sheet_name, index=True)

def exportFinancialReportBalanceSheet (symbol='HPG'):
    financialReport = financial_report (symbol=symbol, report_type='BalanceSheet', frequency='Quarterly')
    with pd.ExcelWriter(file_companyOverview_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        sheet_name = "Bang_can_doi_tien_te"
        financialReport.to_excel(writer, sheet_name=sheet_name, index=True)

def exportFinancialReportCashFlow (symbol='HPG'):
    financialReport = financial_report (symbol='SSI', report_type='CashFlow', frequency='Quarterly')
    with pd.ExcelWriter(file_companyOverview_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        sheet_name = "Bang_luu_chuyen_tien_te"
        financialReport.to_excel(writer, sheet_name=sheet_name, index=True)

def exportStockEvaluation (symbol='HPG'):
    stockEvaluation = stock_evaluation (symbol=symbol, period=1, time_window='D')
    print(">>>stockEvaluation :\n",stockEvaluation);
    with pd.ExcelWriter(file_companyOverview_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        sheet_name = "stockEvaluation"
        stockEvaluation.to_excel(writer, sheet_name=sheet_name, index=True)

def main():
    print("Chương trình bắt đầu.")
    symbol='HPG'
    
    # exportListCompanies()
    # exportcompany_overview(symbol)
    # exportCompanyOfficers(symbol)
    # exportCompanyOfficers(symbol)
    # exportFinancialRatioCompare(symbol)

    # # Báo cáo tài chính
    # # Income Statement: Báo cáo doanh thu
    # exportFinancialReportIncomeStatement(symbol)
    # # Balance Sheet: Bảng cân đối kế toán
    # exportFinancialReportBalanceSheet(symbol)
    # # Cashflow: Báo cáo lưu chuyển tiền tệ
    # exportFinancialReportCashFlow(symbol)
    
    # exportStockEvaluation (symbol='HPG')

    df = stock_historical_data(symbol='VNINDEX', start_date='2022-01-01', end_date='2023-10-10', resolution='1D', type='index')
    print(">>>DEBUG df",type(df))
    fig = candlestick_chart(df, 
                    title='VNINDEX Candlestick Chart with MA and Volume', x_label='Date', y_label='Price', ma_periods=[50,200], 
                    show_volume=True, figure_size=(15, 8), reference_period=300, 
                    colors=('lightgray', 'gray'), reference_colors=('black', 'blue'))
    fig.show()
    fig.write_image("VNINDEX_candlestick.png")



    price_board('TCB,SSI,VND')

    print("Chương trình kết thúc.")

if __name__ == "__main__":
    main()
