from entry import Entry
from typing import List
import requests
import pandas as pd
import numpy as np

class Form:
    def __init__(self, form_id: int) -> None:
        self.form_id = form_id
    
    def get_df_entries(self, base_url, oauth) -> pd.DataFrame:
        """
        Get the entries of a form

        Parameters
        ----------
        base_url : str
            The base url of the Gravity Forms API
        oauth : OAuth1
            The oauth object

        Returns
        -------
        DataFrame
            The entries of the form
        """

        url = base_url + "wp-json/gf/v2/entries?form_ids[0]="+str(self.form_id)+"&_labels=1"
        responseEntriesForm = requests.get(url, auth=oauth)
        entries = responseEntriesForm.json()['entries']
        labels = responseEntriesForm.json()['entries'][len(entries)-1]['_labels']

        url = base_url+ "/wp-json/gf/v2/entries?form_ids[0]="+str(self.form_id)
        limiteEntradas = str(50000)
        responseEntriesForm = requests.get(url + '&paging[page_size]=' + limiteEntradas, auth=oauth)
        
        camposRespuesta = {}
        for entry in responseEntriesForm.json()["entries"]:
            for key in labels.keys():
                labelActual = labels[key]
                try:
                    if labelActual not in camposRespuesta:
                        try: 
                            camposRespuesta[labelActual] = [entry[key]]
                        except KeyError:
                            camposRespuesta[labelActual] = []
                    else:
                        try: 
                            camposRespuesta[labelActual].append(entry[key])
                        except KeyError:
                             camposRespuesta[labelActual].append(None)
                except TypeError:
                    pass
        df = pd.DataFrame.from_dict(camposRespuesta,orient='index')
        df = df.transpose()
        df = df.replace({None: np.nan, 'None': np.nan, '': np.nan})
        df.dropna(axis=0, how='all', inplace=True)
        df = df.replace({np.nan: None})
        return df
