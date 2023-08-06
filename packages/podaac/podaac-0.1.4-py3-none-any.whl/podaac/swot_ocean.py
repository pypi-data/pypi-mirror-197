import scipy as sp
import numpy as np
import xarray as xr

class swot_ocean:

    def __init__(self):
        
        return

    def list_available_datasets(self,):
        """
        use this to list all swot-ocean-related collections (datasets)
        
        Return
        ------
        A list of all available SWOT-ocean related data products
        
        """
        
        return
        
        
    def find_L2_swath(self,concept_id,tstart,tend,bbox):
        """Get filenames of L2 KaRIN swaths
      
        PARAMETERS
        ----------
        tstart : numpy.datetime64
                The starting time
        tend : numpy.datetime64
                The end time 
    
        RETURNS
        -------
        flds : dict {'http': list for opendap, 's3':a list of s3 links}
    
        """
        
        
        return
        
    def L2_subset(self,concept_id, temporal, bbox):
        """
        With the provided temporal and bounding box, use l2ss-py to subset and download
        
        Return
        ------
        Downloadable L2 subsets
        """
        
        
        return
