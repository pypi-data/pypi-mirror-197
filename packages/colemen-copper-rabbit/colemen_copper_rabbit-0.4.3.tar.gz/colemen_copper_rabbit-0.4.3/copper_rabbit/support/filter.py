
import colemen_utils as c

def get_filter(model,exclude_deleted=True,**kwargs):
    '''
        Filter the kwargs by what the model is capable of.
        This will produce the filter_args that are used by the sqlalchemy filter method.

        If the model supports timestamp and modified_timestamp columns, it will search the kwargs
        for created_start,created_end,modified_start,modified_end keys, this allows the 
        search to filter by dates or date ranges

        ----------

        Arguments
        -------------------------
        `model` {model}
            The model to filter the kwargs by

        [`exclude_deleted`=True] {bool}
            If False and the model supports the deleted column, then deleted rows will be included.


        Return {tuple}
        ----------------------
        A tuple containing the filter_args and the kwargs dict with non-column keys removed.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 03-16-2023 09:59:14
        `version`: 1.0
        `method_name`: get_filter
        * @xxx [03-16-2023 10:02:53]: documentation for get_filter
    '''
    created_start,kwargs = c.obj.get_kwarg_remove(['created_start'],None,(int),**kwargs)
    created_end,kwargs = c.obj.get_kwarg_remove(['created_end'],None,(int),**kwargs)
    modified_start,kwargs = c.obj.get_kwarg_remove(['modified_start'],None,(int),**kwargs)
    modified_end,kwargs = c.obj.get_kwarg_remove(['modified_end'],None,(int),**kwargs)

    filter_args = []
    if hasattr(model,'timestamp'):
        if created_start is not None:
            filter_args.append(model.timestamp >= created_start)
        if created_end is not None:
            filter_args.append(model.timestamp <= created_end)

    if hasattr(model,'modified_timestamp'):
        if modified_start is not None:
            filter_args.append(model.modified_timestamp >= modified_start)
        if modified_end is not None:
            filter_args.append(model.modified_timestamp <= modified_end)

    if hasattr(model,'deleted'):
        if exclude_deleted is True:
            kwargs['deleted'] = None

    return (filter_args,kwargs)