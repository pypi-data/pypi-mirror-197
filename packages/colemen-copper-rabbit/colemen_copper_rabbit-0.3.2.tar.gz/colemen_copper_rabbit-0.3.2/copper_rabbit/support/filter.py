
import colemen_utils as c

def get_filter(model,exclude_deleted=True,**kwargs):
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