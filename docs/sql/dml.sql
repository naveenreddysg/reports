    sql = """
            select
        sales0_.id as id,
        sales0_.created_date as createdOn,
        sales0_.created_by as createdBy,
        sales0_.modified_by as modifiedBy,
        sales0_.modified_date as modifiedOn,
        sales0_.active as active,
        sales0_.cumilative_cgst as cumilativeCgst,
        sales0_.cumilative_igst as cumilativeIgst,
        sales0_.cumilative_sgst as cumilativeSgst,
        sales0_.cess as cess,
        sales0_.cessValue as cessVal,
        sales0_.company_id as company,
        sales0_.customer_id as customer,
        sales0_.discount as discount,
        sales0_.discount_value as discountValue,
        sales0_.due_date as dueDate,
        sales0_.invoice_date as invoiceDate,
        sales0_.invoice_message as invoiceMessage,
        sales0_.invoice_number as invoiceNumber,
        sales0_.isBillingAddress as isBillingAddress,
        sales0_.isCgst as isCgst,
        sales0_.isIgst as isIgst,
        sales0_.isProduct as isProduct,
        sales0_.isService as isService,
        sales0_.memo as memo,
        sales0_.paid as paid,
        sales0_.payment_terms as payment,
        sales0_.sale_status as saleStatus,
        sales0_.save_type as saveType,
        sales0_.subtotal as subtotal,
        sales0_.total as total,
        sales0_.total_before_tax as totalBeforeTax,
        sales0_.cumilative_tax as cumilativeTax,
        sales0_.user_id as userId 
    from
        sales sales0_ 

        """
    query_sets = db.engine.execute(text(sql)).fetchall()
    column_names = ['id', 'createdOn', 'createdBy', 'modifiedBy', 'active', 'cumilativeCgst','cumilativeIgst',
        'cumilativeSgst', 'cess', 'cessVal', 'company', 'customer','discount', 'discountValue', 'dueDate', 'invoiceDate',
        'invoiceMessage', 'invoiceNumber', 'isBillingAddress', 'isCgst', 'isIgst', 'isProduct',
        'isService','memo', 'paid', 'payment','saleStatus', 'saveType', 'subtotal', 'total',
        'totalBeforeTax', 'cumilativeTax', 'userId']
    return excel.make_response_from_query_sets(query_sets, column_names, "xls")