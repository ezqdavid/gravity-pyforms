from dotenv import load_dotenv
from forms import Form
import os
from typing import List
from requests_oauthlib import OAuth1
from pandas import DataFrame

class Gravity:
    def __init__(self, client_key: str = None, client_secret: str = None, base_url: str =None) -> None:
        load_dotenv()
        self.oauth = OAuth1(client_key = client_key or os.getenv("CLIENT_KEY"), client_secret = client_secret or os.getenv("CLIENT_SECRET"))
        self.base_url = base_url or os.getenv("BASE_URL")
        self.forms = []
    
    def add_form(self, form_id: int) -> None:
        """
        Add a form to the Gravity object

        Parameters
        ---------- 
        form_id : int
            The form id
        """
        self.forms.append(Form(form_id))
    
    def get_forms(self) -> List[Form]:
        """
        Get the forms of the Gravity object

        Returns
        -------
        List[Form]
            The forms of the Gravity object
        """
        return self.forms
    
    def get_df_entries(self, form_id: int) -> DataFrame:
        """
        Get the entries of a form

        Parameters
        ----------
        form_id : int
            The form id

        Returns
        -------
        DataFrame
            The entries of the form
        """
        for form in self.forms:
            if form.form_id == form_id:
                return form.get_df_entries(self.base_url, self.oauth)