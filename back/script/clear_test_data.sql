with
    workinterval_ids as (
        select api_workinterval.id as workinterval_id
        from api_client, api_workinterval
        where
            api_client.id = api_workinterval.client_id
        and (   api_client.name like 'test%'
            or  api_client.name like 'next%'
            )
    )
delete from api_workinterval
using
    workinterval_ids
where api_workinterval.id = workinterval_ids.workinterval_id
;

with
    invoiceitem_ids as (
        select api_invoiceitem.id as invoiceitem_id
        from api_client, api_invoiceitem, api_invoice
        where
            api_client.id = api_invoice.client_id
        and api_invoice.id = api_invoiceitem.invoice_id
        and (   api_client.name like 'test%'
            or  api_client.name like 'next%'
            )
    )
delete from api_invoiceitem
using
    invoiceitem_ids
where api_invoiceitem.id = invoiceitem_ids.invoiceitem_id
;


with
    invoice_ids as (
        select api_invoice.id as invoice_id
        from api_client, api_invoice
        where
            api_client.id = api_invoice.client_id
        and (   api_client.name like 'test%'
            or  api_client.name like 'next%'
            )
    )
delete from api_invoice
using
    invoice_ids
where api_invoice.id = invoice_ids.invoice_id

with
    workpiece_ids as (
        select api_workpiece.id as workpiece_id
        from api_client, api_workpiece
        where
            api_client.id = api_workpiece.client_id
        and (   api_client.name like 'test%'
            or  api_client.name like 'next%'
            )
    )
delete from api_workpiece
using
    workpiece_ids
where api_workpiece.id = workpiece_ids.workpiece_id
;

delete from api_client
where
         (   api_client.name like 'test%'
            or  api_client.name like 'next%'
            )
;