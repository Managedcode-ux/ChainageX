import requests
from datetime import datetime
from app.app_config.setting import get_settings
from app.schemas.diesel_schema import DieselReceivedCreateSchema

settings = get_settings()

TALLY_URL = settings.TALLY_URL

voucher_date = "20250401"


def tallyVoucher_DieselReceived(payload: DieselReceivedCreateSchema):
    """
    Sends a Purchase Voucher  to Tally for Diesel Received
    """

    # voucher_date = payload.received_date_time.strftime("%Y%m%d")
    xml_payload = f"""
        <ENVELOPE>
          <HEADER>
            <TALLYREQUEST>Import Data</TALLYREQUEST>
          </HEADER>
        
          <BODY>
            <IMPORTDATA>
              <REQUESTDESC>
                <REPORTNAME>Vouchers</REPORTNAME>
                <STATICVARIABLES>
                  <SVCURRENTCOMPANY>ChainageX</SVCURRENTCOMPANY>
                </STATICVARIABLES>
              </REQUESTDESC>
        
              <REQUESTDATA>
                <TALLYMESSAGE>
                  <VOUCHER ACTION="Create">
                    <VOUCHERTYPENAME>Purchase</VOUCHERTYPENAME>
                    <PERSISTEDVIEW>Accounting Voucher View</PERSISTEDVIEW>
        
                    <DATE>{voucher_date}</DATE>
                    <EFFECTIVEDATE>{voucher_date}</EFFECTIVEDATE>
        
                    <VOUCHERNUMBER>{payload.purchase_invoice}</VOUCHERNUMBER>
                    <NARRATION>
                      Diesel received for project {payload.project_name}
                    </NARRATION>
        
                    <!-- Debit: Diesel Received -->
                    <ALLLEDGERENTRIES.LIST>
                      <LEDGERNAME>Diesel Received</LEDGERNAME>
                      <ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE>
                      <AMOUNT>-{payload.total_price}</AMOUNT>
                    </ALLLEDGERENTRIES.LIST>
        
                    <!-- Credit: Cash -->
                    <ALLLEDGERENTRIES.LIST>
                      <LEDGERNAME>Cash</LEDGERNAME>
                      <ISDEEMEDPOSITIVE>No</ISDEEMEDPOSITIVE>
                      <AMOUNT>{payload.total_price}</AMOUNT>
                    </ALLLEDGERENTRIES.LIST>
        
                  </VOUCHER>
                </TALLYMESSAGE>
              </REQUESTDATA>
            </IMPORTDATA>
          </BODY>
        </ENVELOPE>
    """

    header = {
        "Content-Type": "text/xml",
    }

    response = requests.post(TALLY_URL, data=xml_payload, headers=header)

    if response.status_code != 200:
        raise Exception("Failed to connect to Tally")

    if "<CREATED>1</CREATED>" not in response.text:
        raise Exception(f"Tally error: {response.text}")

    return True


def tallyVoucher_DieselIssued(payload):
    xml_payload = f"""
        <ENVELOPE>
      <HEADER>
        <TALLYREQUEST>Import Data</TALLYREQUEST>
      </HEADER>
    
      <BODY>
        <IMPORTDATA>
          <REQUESTDESC>
            <REPORTNAME>Vouchers</REPORTNAME>
            <STATICVARIABLES>
              <SVCURRENTCOMPANY>ChainageX</SVCURRENTCOMPANY>
            </STATICVARIABLES>
          </REQUESTDESC>
    
          <REQUESTDATA>
            <TALLYMESSAGE>
              <VOUCHER ACTION="Create">
                <VOUCHERTYPENAME>Journal</VOUCHERTYPENAME>
                <PERSISTEDVIEW>Accounting Voucher View</PERSISTEDVIEW>
    
                <DATE>{voucher_date}</DATE>
                <EFFECTIVEDATE>{voucher_date}</EFFECTIVEDATE>
    
                <NARRATION>
                  Diesel issued for project {payload.project_name}
                </NARRATION>
    
                <!-- Debit: Diesel Issued -->
                <ALLLEDGERENTRIES.LIST>
                  <LEDGERNAME>Diesel Issued</LEDGERNAME>
                  <ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE>
                  <AMOUNT>-{payload.total_price}</AMOUNT>
                </ALLLEDGERENTRIES.LIST>
    
                <!-- Credit: Diesel Received -->
                <ALLLEDGERENTRIES.LIST>
                  <LEDGERNAME>Diesel Received</LEDGERNAME>
                  <ISDEEMEDPOSITIVE>No</ISDEEMEDPOSITIVE>
                  <AMOUNT>{payload.total_price}</AMOUNT>
                </ALLLEDGERENTRIES.LIST>
    
              </VOUCHER>
            </TALLYMESSAGE>
          </REQUESTDATA>
        </IMPORTDATA>
      </BODY>
    </ENVELOPE>
    """

    header = {"Content-Type":"application/xml"}

    response = requests.post(TALLY_URL, data=xml_payload, headers=header)
    if response.status_code != 200:
        raise Exception("Failed to connect to Tally")

    return True