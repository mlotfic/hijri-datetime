# ===================== UTILITY FUNCTIONS =====================

def safe_get(data, path, default=""):
    """
    Safely extract nested dictionary values with dot notation.
    
    Navigates through nested dictionaries using a dot-separated path string.
    Returns the default value if any key in the path doesn't exist or if
    the data structure is invalid.
    
    Parameters
    ----------
    data : dict
        The dictionary to extract from
    path : str
        Dot-separated path to the value (e.g., 'hijri.month.number')
    default : any, optional
        Default value to return if path doesn't exist, by default ""
    
    Returns
    -------
    any
        The value at the specified path, or default if not found
        
    Examples
    --------
    >>> data = {'hijri': {'month': {'number': 7}}}
    >>> safe_get(data, 'hijri.month.number', 0)
    7
    >>> safe_get(data, 'hijri.month.missing', 'N/A')
    'N/A'
    >>> safe_get(None, 'any.path', 'fallback')
    'fallback'
    """
    try:
        keys = path.split('.')
        result = data
        # Navigate through each key in the path
        for key in keys:
            result = result[key]
        return result if result is not None else default
    except (KeyError, TypeError, AttributeError):
        return default
