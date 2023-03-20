declare @localeidNor int
declare @localeidEng int

select @localeidNor = id from lng.Locale where LocaleId = 'no-No'
select @localeidEng = id from lng.Locale where LocaleId = 'en-Us'

declare @alias nvarchar(max)
declare @translationEng nvarchar(max)
declare @translationNor nvarchar(max)
declare @subSystemId int

-- ===========================================
--      NEW CUSTOM TEXTS AND TRANSLATIONS
--  insert into ResourceBase AND ResourceText
-- ===========================================

declare  @id int
select @id =  max( id) from lng.ResourceBase 
if @id < 100000
begin
	set @id = 100000
end

if not exists (select * from lng.ResourceBase where Alias = 'ticket.nameLabel')
begin
	set @id = @id + 1
	insert into lng.ResourceBase (Id,SubsystemId, alias)
	values (@id,'106','ticket.nameLabel')
	insert into lng.ResourceText (ResourceId, LocaleId , Text , IsCustomTranslation )
	values (@id,@localeidEng,'Name',1)
	insert into lng.ResourceText (ResourceId, LocaleId , Text , IsCustomTranslation )
	values (@id,@localeidNor,'Navn',1)
end

if not exists (select * from lng.ResourceBase where Alias = 'ticket.telephoneLabel')
begin
	set @id = @id + 1
	insert into lng.ResourceBase (Id,SubsystemId, alias)
	values (@id,'106','ticket.telephoneLabel')
	insert into lng.ResourceText (ResourceId, LocaleId , Text , IsCustomTranslation )
	values (@id,@localeidEng,'Telephone',1)
	insert into lng.ResourceText (ResourceId, LocaleId , Text , IsCustomTranslation )
	values (@id,@localeidNor,'Telefon',1)
end

if not exists (select * from lng.ResourceBase where Alias = 'ticket.serialLabel')
begin
	set @id = @id + 1
	insert into lng.ResourceBase (Id,SubsystemId, alias)
	values (@id,'106','ticket.serialLabel')
	insert into lng.ResourceText (ResourceId, LocaleId , Text , IsCustomTranslation )
	values (@id,@localeidEng,'Serial Number',1)
	insert into lng.ResourceText (ResourceId, LocaleId , Text , IsCustomTranslation )
	values (@id,@localeidNor,'Serie nr',1)
end
if not exists (select * from lng.ResourceBase where Alias = 'ticket.itemsLabel')
begin
	set @id = @id + 1
	insert into lng.ResourceBase (Id,SubsystemId, alias)
	values (@id,'106','ticket.itemsLabel')
	insert into lng.ResourceText (ResourceId, LocaleId , Text , IsCustomTranslation )
	values (@id,@localeidEng,'Items',1)
	insert into lng.ResourceText (ResourceId, LocaleId , Text , IsCustomTranslation )
	values (@id,@localeidNor,'varer',1)
end

if not exists (select * from lng.ResourceBase where Alias = 'ticket.VATPercentLabel')
begin
	set @id = @id + 1
	insert into lng.ResourceBase (Id,SubsystemId, alias)
	values (@id,'106','ticket.VATPercentLabel')
	insert into lng.ResourceText (ResourceId, LocaleId , Text , IsCustomTranslation )
	values (@id,1,'VAT %',1)
	insert into lng.ResourceText (ResourceId, LocaleId , Text , IsCustomTranslation )
	values (@id,@localeidNor,'Mva%',1)
end

-- CARD ACTIVATION
SET @alias = 'payment.cardActivate.eftCardActivateFailedErrorMessage'
SET @subSystemId = 125
set @translationEng = 'EFT card activate failed due to internal error'
set @translationNor = 'EFT card activate failed due to internal error'

EXECUTE lng.spNGSetTranslation @alias,@subSystemId,@localeidEng,@localeIdNor,@translationEng ,@translationNor, @id output

SET @alias = 'payment.cardActivate.eftCardActivateOperationSucceededMessage'
SET @subSystemId = 125
set @translationEng = 'EFT card activate operation succeeded'
set @translationNor = 'EFT card activate operation succeeded'

EXECUTE lng.spNGSetTranslation @alias,@subSystemId,@localeidEng,@localeIdNor,@translationEng ,@translationNor, @id output

SET @alias = 'payment.cardActivate.eftCardActivateTerminalErrorResultMessage'
SET @subSystemId = 125
set @translationEng = 'EFT card activate terminal error occurred. Result:'
set @translationNor = 'EFT card activate terminal error occurred. Result:'

EXECUTE lng.spNGSetTranslation @alias,@subSystemId,@localeidEng,@localeIdNor,@translationEng ,@translationNor, @id output

SET @alias = 'payment.cardActivate.eftCardActivateNotActivate'
SET @subSystemId = 125
set @translationEng = 'Gift card was not activated'
set @translationNor = 'Gift card was not activated'

EXECUTE lng.spNGSetTranslation @alias,@subSystemId,@localeidEng,@localeIdNor,@translationEng ,@translationNor, @id output

SET @alias = 'basket.addItem.eftGiftCardAlreadyInBasket'
SET @subSystemId = 116
set @translationEng = 'Cannot add another gift card to the basket'
set @translationNor = 'Cannot add another gift card to the basket'

EXECUTE lng.spNGSetTranslation @alias,@subSystemId,@localeidEng,@localeIdNor,@translationEng ,@translationNor, @id output
-- END OF CARD ACTIVATION
-- TOMRA MESSAGES

DECLARE @subsystem int  
SELECT @subsystem = Id FROM lng.Subsystem WHERE Name = 'BarcodeRecognition'

IF NOT EXISTS (SELECT * FROM lng.ResourceBase WHERE Alias = 'barcodeRecognition.NG.Tomra.TomraConsumeErrorMessage')
BEGIN
	SET @id = @id+1
	INSERT INTO lng.ResourceBase (Id,SubsystemId,Alias,MaximumLength)
	VALUES (@id, @subsystem, 'barcodeRecognition.NG.Tomra.TomraConsumeErrorMessage', 500)
	INSERT INTO lng.ResourceText (ResourceId, LocaleId, Text, IsCustomTranslation)
    VALUES (@id, @localeidEng, 'Tomra item has not been consumed',1)
END

IF NOT EXISTS (SELECT * FROM lng.ResourceBase WHERE Alias = 'barcodeRecognition.NG.Tomra.TomraValidationErrorMessage')
BEGIN
	SET @id = @id+1
	INSERT INTO lng.ResourceBase (Id,SubsystemId,Alias,MaximumLength)
    VALUES (@id,@subsystem,'barcodeRecognition.NG.Tomra.TomraValidationErrorMessage', 500)

	INSERT INTO lng.ResourceText (ResourceId, LocaleId, Text, IsCustomTranslation)
    VALUES (@id, @localeidEng, 'Tomra item has not been verified',1)

END
	 
IF NOT EXISTS (SELECT * FROM lng.ResourceBase WHERE Alias = 'barcodeRecognition.NG.Tomra.TomraConsumeSuccessMessage')
BEGIN	 
	SET @id = @id+1
	INSERT INTO lng.ResourceBase (Id,SubsystemId,Alias,MaximumLength)
    VALUES (@id, @subsystem, 'barcodeRecognition.NG.Tomra.TomraConsumeSuccessMessage', 500)

	INSERT INTO lng.ResourceText (ResourceId, LocaleId, Text, IsCustomTranslation)
    VALUES (@id, @localeidEng, 'Tomra items consumed',1)

END

IF NOT EXISTS (SELECT * FROM lng.ResourceBase WHERE Alias = 'barcodeRecognition.NG.Tomra.TomraAlreadyScannedMessage')
BEGIN
	SET @id = @id+1
	INSERT INTO lng.ResourceBase (Id,SubsystemId,Alias,MaximumLength)
    VALUES (@id, @subsystem, 'barcodeRecognition.NG.Tomra.TomraAlreadyScannedMessage', 500)

	INSERT INTO lng.ResourceText (ResourceId, LocaleId, Text, IsCustomTranslation)
    VALUES (@id, @localeidEng, 'Tomra item has already been scanned',1)
END
	 
IF NOT EXISTS (SELECT * FROM lng.ResourceBase WHERE Alias = 'barcodeRecognition.NG.Tomra.TomraVerifiedOffline')
BEGIN
	SET @id = @id+1
	INSERT INTO lng.ResourceBase (Id,SubsystemId,Alias,MaximumLength)
    VALUES (@id, @subsystem, 'barcodeRecognition.NG.Tomra.TomraVerifiedOffline', 500)
			
	INSERT INTO lng.ResourceText (ResourceId, LocaleId, Text, IsCustomTranslation)
    VALUES (@id, @localeidEng, 'Tomra host offline',1)
END


IF NOT EXISTS (SELECT * FROM lng.ResourceBase WHERE Alias = 'barcodeRecognition.NG.Tomra.TomraInvalidBarcode')
BEGIN
	SET @id = @id+1
	INSERT INTO lng.ResourceBase (Id,SubsystemId,Alias,MaximumLength)
    VALUES (@id, @subsystem, 'barcodeRecognition.NG.Tomra.TomraInvalidBarcode', 500)
			
	INSERT INTO lng.ResourceText (ResourceId, LocaleId, Text, IsCustomTranslation)
    VALUES (@id, @localeidEng, 'Invalid Tomra barcode',1)
	
END

IF NOT EXISTS (SELECT * FROM lng.ResourceBase WHERE Alias = 'barcodeRecognition.NG.Tomra.TomraBarcodeAlreadyUsed')
BEGIN
	SET @id = @id+1
	INSERT INTO lng.ResourceBase (Id,SubsystemId,Alias,MaximumLength)
    VALUES (@id, @subsystem, 'barcodeRecognition.NG.Tomra.TomraBarcodeAlreadyUsed', 500)
			
	INSERT INTO lng.ResourceText (ResourceId, LocaleId, Text, IsCustomTranslation)
    VALUES (@id, @localeidEng, 'Tomra barcode has been already used',1)
END

IF NOT EXISTS (SELECT * FROM lng.ResourceBase WHERE Alias = 'barcodeRecognition.NG.Tomra.TomraBarcodeNotFound')
BEGIN
	SET @id = @id+1
	INSERT INTO lng.ResourceBase (Id,SubsystemId,Alias,MaximumLength)
    VALUES (@id, @subsystem, 'barcodeRecognition.NG.Tomra.TomraBarcodeNotFound', 500)
			
	INSERT INTO lng.ResourceText (ResourceId, LocaleId, Text, IsCustomTranslation)
    VALUES (@id, @localeidEng, 'Tomra item not found. Do you want to add it to basket anyway?',1)
END

IF NOT EXISTS (SELECT * FROM lng.ResourceBase WHERE Alias = 'barcodeRecognition.NG.Tomra.TomraBarcodeDifferentStore')
BEGIN
	SET @id = @id+1
	INSERT INTO lng.ResourceBase (Id,SubsystemId,Alias,MaximumLength)
    VALUES (@id, @subsystem, 'barcodeRecognition.NG.Tomra.TomraBarcodeDifferentStore', 500)
			
	INSERT INTO lng.ResourceText (ResourceId, LocaleId, Text, IsCustomTranslation)
    VALUES (@id, @localeidEng, 'Tomra item was created in a different store',1)
END

IF NOT EXISTS (SELECT * FROM lng.ResourceBase WHERE Alias = 'barcodeRecognition.NG.Tomra.TomraBarcodeIncorrectBasket')
BEGIN
	SET @id = @id+1
	INSERT INTO lng.ResourceBase (Id,SubsystemId,Alias,MaximumLength)
    VALUES (@id, @subsystem, 'barcodeRecognition.NG.Tomra.TomraBarcodeIncorrectBasket', 500)
			
	INSERT INTO lng.ResourceText (ResourceId, LocaleId, Text, IsCustomTranslation)
    VALUES (@id, @localeidEng, 'Tomra item cannot be add to return basket',1)
END

IF NOT EXISTS (SELECT * FROM lng.ResourceBase WHERE Alias = 'barcodeRecognition.NG.Tomra.TomraBarcodeZeroAmount')
BEGIN
	SET @id = @id+1
	INSERT INTO lng.ResourceBase (Id,SubsystemId,Alias,MaximumLength)
    VALUES (@id, @subsystem, 'barcodeRecognition.NG.Tomra.TomraBarcodeZeroAmount', 500)
			
	INSERT INTO lng.ResourceText (ResourceId, LocaleId, Text, IsCustomTranslation)
    VALUES (@id, @localeidEng, 'Tomra item cannot be zero value',1)
END
-- END TOMRA MESSAGES
-- Cashier
if not exists (select * from lng.ResourceBase where Alias = 'shift.getShiftForCashierDeclaration.posLabel')
begin
	set @id = @id + 1
	insert into lng.ResourceBase (Id,SubsystemId, alias)
	values (@id,'128','shift.getShiftForCashierDeclaration.posLabel')
	insert into lng.ResourceText (ResourceId, LocaleId , Text , IsCustomTranslation )
	values (@id,@localeidEng,'Pos:',1)
	insert into lng.ResourceText (ResourceId, LocaleId , Text , IsCustomTranslation )
	values (@id,@localeidNor,'Pos:',1)
end
-- End Cashier

-- EFT CASH DEPOSIT / WITHDRAWAL
SET @alias = 'payment.cashDeposit.eftCashDepositFailedErrorMessage'
SET @subSystemId = 125
set @translationEng = 'EFT cash deposit failed due to internal error'
set @translationNor = 'EFT cash deposit failed due to internal error'

EXECUTE lng.spNGSetTranslation @alias,@subSystemId,@localeidEng,@localeIdNor,@translationEng ,@translationNor, @id output

SET @alias = 'payment.cashDeposit.eftCashDepositOperationSucceededMessage'
SET @subSystemId = 125
set @translationEng = 'EFT cash deposit operation succeeded'
set @translationNor = 'EFT cash deposit operation succeeded'

EXECUTE lng.spNGSetTranslation @alias,@subSystemId,@localeidEng,@localeIdNor,@translationEng ,@translationNor, @id output

SET @alias = 'payment.cashDeposit.eftCashDepositTerminalErrorResultMessage'
SET @subSystemId = 125
set @translationEng = 'EFT cash deposit terminal error occurred. Result:'
set @translationNor = 'EFT cash deposit terminal error occurred. Result:'

EXECUTE lng.spNGSetTranslation @alias,@subSystemId,@localeidEng,@localeIdNor,@translationEng ,@translationNor, @id output

SET @alias = 'payment.cashWithdrawal.eftCashWithdrawalFailedErrorMessage'
SET @subSystemId = 125
set @translationEng = 'EFT cash withdrawal failed due to internal error'
set @translationNor = 'EFT cash withdrawal failed due to internal error'

EXECUTE lng.spNGSetTranslation @alias,@subSystemId,@localeidEng,@localeIdNor,@translationEng ,@translationNor, @id output

SET @alias = 'payment.cashWithdrawal.eftCashWithdrawalOperationSucceededMessage'
SET @subSystemId = 125
set @translationEng = 'EFT cash withdrawal operation succeeded'
set @translationNor = 'EFT cash withdrawal operation succeeded'

EXECUTE lng.spNGSetTranslation @alias,@subSystemId,@localeidEng,@localeIdNor,@translationEng ,@translationNor, @id output

SET @alias = 'payment.cashWithdrawal.eftCashWithdrawalTerminalErrorResultMessage'
SET @subSystemId = 125
set @translationEng = 'EFT cash withdrawal terminal error occurred. Result:'
set @translationNor = 'EFT cash withdrawal terminal error occurred. Result:'

EXECUTE lng.spNGSetTranslation @alias,@subSystemId,@localeidEng,@localeIdNor,@translationEng ,@translationNor, @id output

SET @alias = 'adminPanelContent.NG.paymentTerminalManagement.cashDeposit.buttonText'
SET @subSystemId = 102
set @translationEng = 'Cash deposit'
set @translationNor = 'Cash deposit'

EXECUTE lng.spNGSetTranslation @alias,@subSystemId,@localeidEng,@localeIdNor,@translationEng ,@translationNor, @id output

SET @alias = 'adminPanelContent.NG.paymentTerminalManagement.cashWithdrawal.buttonText'
SET @subSystemId = 102
set @translationEng = 'Cash withdrawal'
set @translationNor = 'Cash withdrawal'

EXECUTE lng.spNGSetTranslation @alias,@subSystemId,@localeidEng,@localeIdNor,@translationEng ,@translationNor, @id output

SET @alias = 'payment.NG.cashDeposit.setIFlag'
SET @subSystemId = 102
set @translationEng = 'Set iFlag?'
set @translationNor = 'Set iFlag?'

EXECUTE lng.spNGSetTranslation @alias,@subSystemId,@localeidEng,@localeIdNor,@translationEng ,@translationNor, @id output

SET @alias = 'payment.NG.cashDeposit.terminalWait'
SET @subSystemId = 102
set @translationEng = 'Follow instructions displayed on terminal'
set @translationNor = 'Follow instructions displayed on terminal'

EXECUTE lng.spNGSetTranslation @alias,@subSystemId,@localeidEng,@localeIdNor,@translationEng ,@translationNor, @id output

-- END OF EFT CASH DEPOSIT / WITHDRAWAL


-- EFT CASHBACK
SET @alias = 'mopTypes.cardWithCashback.text'
SET @subSystemId = 102
set @translationEng = 'Card with cashback'
set @translationNor = 'Card with cashback'

EXECUTE lng.spNGSetTranslation @alias,@subSystemId,@localeidEng,@localeIdNor,@translationEng ,@translationNor, @id output

SET @alias = 'checkoutPanel.numpad.cashback.title'
SET @subSystemId = 102
set @translationEng = 'CASHBACK AMOUNT'
set @translationNor = 'CASHBACK AMOUNT'

EXECUTE lng.spNGSetTranslation @alias,@subSystemId,@localeidEng,@localeIdNor,@translationEng ,@translationNor, @id output

-- END OF EFTCASHBACK

-- EFT GlobalReconciliation
SET @alias = 'payment.globalReconciliation.eftGlobalReconciliationFailedErrorMessage'
SET @subSystemId = 125
set @translationEng = 'EFT Global Reconciliation failed due to internal error'
set @translationNor = 'EFT Global Reconciliation failed due to internal error'
EXECUTE lng.spNGSetTranslation @alias,@subSystemId,@localeidEng,@localeIdNor,@translationEng ,@translationNor, @id output

SET @alias = 'payment.globalReconciliation.eftGlobalReconciliationOperationSucceededMessage'
SET @subSystemId = 125
set @translationEng = 'EFT Global Reconciliation operation succeeded'
set @translationNor = 'EFT Global Reconciliation operation succeeded'
EXECUTE lng.spNGSetTranslation @alias,@subSystemId,@localeidEng,@localeIdNor,@translationEng ,@translationNor, @id output

SET @alias = 'payment.globalReconciliation.eftGlobalReconciliationTerminalErrorResultMessage'
SET @subSystemId = 125
set @translationEng = 'EFT Global Reconciliation terminal error occurred. Result:'
set @translationNor = 'EFT Global Reconciliation terminal error occurred. Result:'
EXECUTE lng.spNGSetTranslation @alias,@subSystemId,@localeidEng,@localeIdNor,@translationEng ,@translationNor, @id output

SET @alias = 'payment.globalReconciliation.RptGlobalReconciliationError'
SET @subSystemId = 125
set @translationEng = 'Error while formatting the Global Reconciliation report'
set @translationNor = 'Error while formatting the Global Reconciliation report'
EXECUTE lng.spNGSetTranslation @alias,@subSystemId,@localeidEng,@localeIdNor,@translationEng ,@translationNor, @id output

SET @alias = 'ticket.RptGlobalReconciliationId'
SET @subSystemId = 106
set @translationEng = 'Global Reconciliation'
set @translationNor = 'Global Reconciliation'
EXECUTE lng.spNGSetTranslation @alias,@subSystemId,@localeidEng,@localeIdNor,@translationEng ,@translationNor, @id output

SET @alias = 'ticket.RptGlobalReconciliationCurrency'
SET @subSystemId = 106
set @translationEng = 'Currency'
set @translationNor = 'Currency'
EXECUTE lng.spNGSetTranslation @alias,@subSystemId,@localeidEng,@localeIdNor,@translationEng ,@translationNor, @id output

SET @alias = 'ticket.RptGlobalReconciliationTotalCount'
SET @subSystemId = 106
set @translationEng = 'Total Count'
set @translationNor = 'Total Count'
EXECUTE lng.spNGSetTranslation @alias,@subSystemId,@localeidEng,@localeIdNor,@translationEng ,@translationNor, @id output

SET @alias = 'ticket.RptGlobalReconciliationTotalAmount'
SET @subSystemId = 106
set @translationEng = 'Total Amount'
set @translationNor = 'Total Amount'
EXECUTE lng.spNGSetTranslation @alias,@subSystemId,@localeidEng,@localeIdNor,@translationEng ,@translationNor, @id output

SET @alias = 'ticket.RptGlobalReconciliationCard'
SET @subSystemId = 106
set @translationEng = 'Card'
set @translationNor = 'Card'
EXECUTE lng.spNGSetTranslation @alias,@subSystemId,@localeidEng,@localeIdNor,@translationEng ,@translationNor, @id output

SET @alias = 'ticket.RptGlobalReconciliationAcquirer'
SET @subSystemId = 106
set @translationEng = 'Acquirer'
set @translationNor = 'Acquirer'
EXECUTE lng.spNGSetTranslation @alias,@subSystemId,@localeidEng,@localeIdNor,@translationEng ,@translationNor, @id output

SET @alias = 'ticket.RptGlobalReconciliationDebitCount'
SET @subSystemId = 106
set @translationEng = 'Debit Count'
set @translationNor = 'Debit Count'
EXECUTE lng.spNGSetTranslation @alias,@subSystemId,@localeidEng,@localeIdNor,@translationEng ,@translationNor, @id output

SET @alias = 'ticket.RptGlobalReconciliationDebitAmount'
SET @subSystemId = 106
set @translationEng = 'Debit Amount'
set @translationNor = 'Debit Amount'
EXECUTE lng.spNGSetTranslation @alias,@subSystemId,@localeidEng,@localeIdNor,@translationEng ,@translationNor, @id output

SET @alias = 'ticket.RptGlobalReconciliationCashbackCount'
SET @subSystemId = 106
set @translationEng = 'Cashback Count'
set @translationNor = 'Cashback Count'
EXECUTE lng.spNGSetTranslation @alias,@subSystemId,@localeidEng,@localeIdNor,@translationEng ,@translationNor, @id output

SET @alias = 'ticket.RptGlobalReconciliationCashbackAmount'
SET @subSystemId = 106
set @translationEng = 'Cashback Amount'
set @translationNor = 'Cashback Amount'
EXECUTE lng.spNGSetTranslation @alias,@subSystemId,@localeidEng,@localeIdNor,@translationEng ,@translationNor, @id output

SET @alias = 'ticket.RptGlobalReconciliationDebitReverseCount'
SET @subSystemId = 106
set @translationEng = 'Debit Reverse Count'
set @translationNor = 'Debit Reverse Count'
EXECUTE lng.spNGSetTranslation @alias,@subSystemId,@localeidEng,@localeIdNor,@translationEng ,@translationNor, @id output

SET @alias = 'ticket.RptGlobalReconciliationDebitReverseAmount'
SET @subSystemId = 106
set @translationEng = 'Debit Reverse Amount'
set @translationNor = 'Debit Reverse Amount'
EXECUTE lng.spNGSetTranslation @alias,@subSystemId,@localeidEng,@localeIdNor,@translationEng ,@translationNor, @id output

SET @alias = 'ticket.RptGlobalReconciliationCreditCount'
SET @subSystemId = 106
set @translationEng = 'Credit Count'
set @translationNor = 'Credit Count'
EXECUTE lng.spNGSetTranslation @alias,@subSystemId,@localeidEng,@localeIdNor,@translationEng ,@translationNor, @id output

SET @alias = 'ticket.RptGlobalReconciliationCreditAmount'
SET @subSystemId = 106
set @translationEng = 'Credit Amount'
set @translationNor = 'Credit Amount'
EXECUTE lng.spNGSetTranslation @alias,@subSystemId,@localeidEng,@localeIdNor,@translationEng ,@translationNor, @id output

SET @alias = 'paymentTerminalManagement.panel.globalReconciliation.buttonText'
SET @subSystemId = 102
set @translationEng = 'Global reconciliation'
set @translationNor = 'Global reconciliation'
EXECUTE lng.spNGSetTranslation @alias,@subSystemId,@localeidEng,@localeIdNor,@translationEng ,@translationNor, @id output

SET @alias = 'payment.globalReconciliation.print.buttonText'
SET @subSystemId = 102
set @translationEng = 'Print document'
set @translationNor = 'Print document'
EXECUTE lng.spNGSetTranslation @alias,@subSystemId,@localeidEng,@localeIdNor,@translationEng ,@translationNor, @id output

-- End of EFT GlobalReconciliation

-- EFT GetLastTransaction

SET @alias = 'payment.getLastTransaction.eftGetLastTransactionTransactionDetails'
SET @subSystemId = 125
set @translationEng = 'Transaction details'
set @translationNor = 'transaction details'

EXECUTE lng.spNGSetTranslation @alias,@subSystemId,@localeidEng,@localeIdNor,@translationEng ,@translationNor, @id output

SET @alias = 'payment.getLastTransaction.eftGetLastTransactionRequestType'
SET @subSystemId = 125
set @translationEng = 'Request type'
set @translationNor = 'Request type'

EXECUTE lng.spNGSetTranslation @alias,@subSystemId,@localeidEng,@localeIdNor,@translationEng ,@translationNor, @id output

SET @alias = 'payment.getLastTransaction.eftGetLastTransactionRequestID'
SET @subSystemId = 125
set @translationEng = 'Request ID'
set @translationNor = 'Request ID'

EXECUTE lng.spNGSetTranslation @alias,@subSystemId,@localeidEng,@localeIdNor,@translationEng ,@translationNor, @id output

SET @alias = 'payment.getLastTransaction.eftGetLastTransactionOverallResult'
SET @subSystemId = 125
set @translationEng = 'Overall result'
set @translationNor = 'Overall result'

EXECUTE lng.spNGSetTranslation @alias,@subSystemId,@localeidEng,@localeIdNor,@translationEng ,@translationNor, @id output

SET @alias = 'payment.getLastTransaction.eftGetLastTransactionTotalAmount'
SET @subSystemId = 125
set @translationEng = 'Payment amount'
set @translationNor = 'Payment amount'

EXECUTE lng.spNGSetTranslation @alias,@subSystemId,@localeidEng,@localeIdNor,@translationEng ,@translationNor, @id output

SET @alias = 'payment.getLastTransaction.eftGetLastTransactionAuthorisationTimeStamp'
SET @subSystemId = 125
set @translationEng = 'Authorisation timestamp'
set @translationNor = 'Authorisation timestamp'

EXECUTE lng.spNGSetTranslation @alias,@subSystemId,@localeidEng,@localeIdNor,@translationEng ,@translationNor, @id output

SET @alias = 'payment.getLastTransaction.eftGetLastTransactionErrorWithResultMessage'
SET @subSystemId = 125
set @translationEng = 'Eft get last transaction terminal error occurred. Result'
set @translationNor = 'Eft get last transaction terminal error occurred. Result'

EXECUTE lng.spNGSetTranslation @alias,@subSystemId,@localeidEng,@localeIdNor,@translationEng ,@translationNor, @id output

SET @alias = 'payment.getLastTransaction.eftGetLastTransactionFailedErrorMessage'
SET @subSystemId = 125
set @translationEng = 'EFT get last transaction failed due to internal error'
set @translationNor = 'EFT get last transaction failed due to internal error'

EXECUTE lng.spNGSetTranslation @alias,@subSystemId,@localeidEng,@localeIdNor,@translationEng ,@translationNor, @id output

SET @alias = 'paymentTerminalManagement.panel.getLastTransaction.buttonText'
SET @subSystemId = 102
set @translationEng = 'Get last transaction'
set @translationNor = 'Get last transaction'

EXECUTE lng.spNGSetTranslation @alias,@subSystemId,@localeidEng,@localeIdNor,@translationEng ,@translationNor, @id output

-- End of EFT GetlastTransaction


-- =========================================
--        ADD ONLY NO-NO TRANSLATIONS
--   insert into ResourceText in norwegian
-- =========================================


if not exists (select * from lng.ResourceText where ResourceId = 22786 and LocaleId = @localeidNor )
begin
	insert into lng.ResourceText (ResourceId, LocaleId , Text , IsCustomTranslation )
	values (22786,@localeidNor,'RETUR GJENPART',1 )
end
else
begin
	update lng.ResourceText set Text = 'RETUR GJENPART' where ResourceId = 22786
end

if not exists (select * from lng.ResourceText where ResourceId = 22535 and LocaleId = @localeidNor )
begin
	insert into lng.ResourceText (ResourceId, LocaleId , Text , IsCustomTranslation )
	values (22535,@localeidNor,'Sjefskortinnehaver',1 )
end

if not exists (select * from lng.ResourceText where ResourceId = 22534 and LocaleId = @localeidNor )
begin
	insert into lng.ResourceText (ResourceId, LocaleId , Text , IsCustomTranslation )
	values (22534,@localeidNor,'Kasserer',1 )
end

if not exists (select * from lng.ResourceText where ResourceId = 22765 and LocaleId = @localeidNor )
begin
	insert into lng.ResourceText (ResourceId, LocaleId , Text , IsCustomTranslation )
	values (22765,@localeidNor,'OperNr',1 )
end

if not exists (select * from lng.ResourceText where ResourceId = 47156 and LocaleId = @localeidNor )
begin
	insert into lng.ResourceText (ResourceId, LocaleId , Text , IsCustomTranslation )
	values (47156,@localeidNor,'Kvitt',1 )
end

if not exists (select * from lng.ResourceText where ResourceId = 40247 and LocaleId = @localeidNor )
begin
	insert into lng.ResourceText (ResourceId, LocaleId , Text , IsCustomTranslation )
	values (40247,@localeidNor,N'?reavrunding',1 )
end
if not exists (select * from lng.ResourceText where ResourceId = 22740 and LocaleId = @localeidNor )
begin
	insert into lng.ResourceText (ResourceId, LocaleId , Text , IsCustomTranslation )
	values (22740,@localeidNor,'Total',1 )
end

if not exists (select * from lng.ResourceText where ResourceId = 45753 and LocaleId = @localeidNor )
begin
	insert into lng.ResourceText (ResourceId, LocaleId , Text , IsCustomTranslation )
	values (45753,@localeidNor,'Mva',1 )
end

if not exists (select * from lng.ResourceText where ResourceId = 22748 and LocaleId = @localeidNor )
begin
	insert into lng.ResourceText (ResourceId, LocaleId , Text , IsCustomTranslation )
	values (22748,@localeidNor,'Grunnlag',1 )
end
if not exists (select * from lng.ResourceText where ResourceId = 22771 and LocaleId = @localeidNor )
begin
	insert into lng.ResourceText (ResourceId, LocaleId , Text , IsCustomTranslation )
	values (22771,@localeidNor,'Kasse',1 )
end

if not exists (select * from lng.ResourceText where ResourceId = 47155 and LocaleId = @localeidNor )
begin
	insert into lng.ResourceText (ResourceId, LocaleId , Text , IsCustomTranslation )
	values (47155,@localeidNor,'Salgskvittering',1 )
end

if not exists (select * from lng.ResourceText where ResourceId = 22775 and LocaleId = @localeidNor )
begin
	insert into lng.ResourceText (ResourceId, LocaleId , Text , IsCustomTranslation )
	values (22775,@localeidNor,'Returkvittering',1 )
end

if not exists (select * from lng.ResourceText where ResourceId = 22749 and LocaleId = @localeidNor )
begin
	insert into lng.ResourceText (ResourceId, LocaleId , Text , IsCustomTranslation )
	values (22749,@localeidNor,'Rabatt',1 )
end

if not exists (select * from lng.ResourceText where ResourceId = 22861 and LocaleId = @localeidNor )
begin
	insert into lng.ResourceText (ResourceId, LocaleId , Text , IsCustomTranslation )
	values (22861,@localeidNor,'Rabatt',1 )
end

if not exists (select * from lng.ResourceText where ResourceId = 22738 and LocaleId = @localeidNor )
begin
	insert into lng.ResourceText (ResourceId, LocaleId , Text , IsCustomTranslation )
	values (22738,@localeidNor,'Prisoverstyring',1 )
end

if not exists (select * from lng.ResourceText where ResourceId = 41454 and LocaleId = @localeidNor )
begin
	insert into lng.ResourceText (ResourceId, LocaleId , Text , IsCustomTranslation )
	values (41454,@localeidNor,'Autorisert av',1 )
end

if not exists (select * from lng.ResourceText where ResourceId = 22772 and LocaleId = @localeidNor )
begin
	insert into lng.ResourceText (ResourceId, LocaleId , Text , IsCustomTranslation )
	values (22772,@localeidNor,'----------        KOPI       ---------',1 )
end

select @id =  id from lng.ResourceBase where Alias = 'ticket.AbortTitleLineLabel'
if not exists (select * from lng.ResourceText where ResourceId = @id and LocaleId = @localeidNor )
begin
	insert into lng.ResourceText (ResourceId, LocaleId , Text , IsCustomTranslation )
	values (@id,@localeidNor,'***       KORREKSJONS GJENPART      ***',1 )
end

-- Panto MESSAGES
SELECT @subsystem = Id FROM lng.Subsystem WHERE Name = 'BarcodeRecognition'
select @id =  max( id) from lng.ResourceBase 
if @id < 100000
begin
	set @id = 100000
end
IF NOT EXISTS (SELECT * FROM lng.ResourceBase WHERE Alias = 'barcodeRecognition.NG.Panto.PantoConsumeErrorMessage')
BEGIN
	SET @id = @id+1
	INSERT INTO lng.ResourceBase (Id,SubsystemId,Alias,MaximumLength)
	VALUES (@id, @subsystem, 'barcodeRecognition.NG.Panto.PantoConsumeErrorMessage', 500)
	INSERT INTO lng.ResourceText (ResourceId, LocaleId, Text, IsCustomTranslation)
    VALUES (@id, @localeidEng, 'Panto item has not been consumed',1)
END

IF NOT EXISTS (SELECT * FROM lng.ResourceBase WHERE Alias = 'barcodeRecognition.NG.Panto.PantoValidationErrorMessage')
BEGIN
	SET @id = @id+1
	INSERT INTO lng.ResourceBase (Id,SubsystemId,Alias,MaximumLength)
    VALUES (@id,@subsystem,'barcodeRecognition.NG.Panto.PantoValidationErrorMessage', 500)

	INSERT INTO lng.ResourceText (ResourceId, LocaleId, Text, IsCustomTranslation)
    VALUES (@id, @localeidEng, 'Panto item has not been verified',1)

END
	 
IF NOT EXISTS (SELECT * FROM lng.ResourceBase WHERE Alias = 'barcodeRecognition.NG.Panto.PantoConsumeSuccessMessage')
BEGIN	 
	SET @id = @id+1
	INSERT INTO lng.ResourceBase (Id,SubsystemId,Alias,MaximumLength)
    VALUES (@id, @subsystem, 'barcodeRecognition.NG.Panto.PantoConsumeSuccessMessage', 500)

	INSERT INTO lng.ResourceText (ResourceId, LocaleId, Text, IsCustomTranslation)
    VALUES (@id, @localeidEng, 'Panto items consumed',1)

END

IF NOT EXISTS (SELECT * FROM lng.ResourceBase WHERE Alias = 'barcodeRecognition.NG.Panto.PantoAlreadyScannedMessage')
BEGIN
	SET @id = @id+1
	INSERT INTO lng.ResourceBase (Id,SubsystemId,Alias,MaximumLength)
    VALUES (@id, @subsystem, 'barcodeRecognition.NG.Panto.PantoAlreadyScannedMessage', 500)

	INSERT INTO lng.ResourceText (ResourceId, LocaleId, Text, IsCustomTranslation)
    VALUES (@id, @localeidEng, 'Panto item has already been scanned',1)
END
	 
IF NOT EXISTS (SELECT * FROM lng.ResourceBase WHERE Alias = 'barcodeRecognition.NG.Panto.PantoVerifiedOffline')
BEGIN
	SET @id = @id+1
	INSERT INTO lng.ResourceBase (Id,SubsystemId,Alias,MaximumLength)
    VALUES (@id, @subsystem, 'barcodeRecognition.NG.Panto.PantoVerifiedOffline', 500)
			
	INSERT INTO lng.ResourceText (ResourceId, LocaleId, Text, IsCustomTranslation)
    VALUES (@id, @localeidEng, 'Panto host offline',1)
END


IF NOT EXISTS (SELECT * FROM lng.ResourceBase WHERE Alias = 'barcodeRecognition.NG.Panto.PantoInvalidBarcode')
BEGIN
	SET @id = @id+1
	INSERT INTO lng.ResourceBase (Id,SubsystemId,Alias,MaximumLength)
    VALUES (@id, @subsystem, 'barcodeRecognition.NG.Panto.PantoInvalidBarcode', 500)
			
	INSERT INTO lng.ResourceText (ResourceId, LocaleId, Text, IsCustomTranslation)
    VALUES (@id, @localeidEng, 'Invalid Panto barcode',1)
	
END

IF NOT EXISTS (SELECT * FROM lng.ResourceBase WHERE Alias = 'barcodeRecognition.NG.Panto.PantoBarcodeAlreadyUsed')
BEGIN
	SET @id = @id+1
	INSERT INTO lng.ResourceBase (Id,SubsystemId,Alias,MaximumLength)
    VALUES (@id, @subsystem, 'barcodeRecognition.NG.Panto.PantoBarcodeAlreadyUsed', 500)
			
	INSERT INTO lng.ResourceText (ResourceId, LocaleId, Text, IsCustomTranslation)
    VALUES (@id, @localeidEng, 'Panto barcode has been already used',1)
END

IF NOT EXISTS (SELECT * FROM lng.ResourceBase WHERE Alias = 'barcodeRecognition.NG.Panto.PantoBarcodeNotFound')
BEGIN
	SET @id = @id+1
	INSERT INTO lng.ResourceBase (Id,SubsystemId,Alias,MaximumLength)
    VALUES (@id, @subsystem, 'barcodeRecognition.NG.Panto.PantoBarcodeNotFound', 500)
			
	INSERT INTO lng.ResourceText (ResourceId, LocaleId, Text, IsCustomTranslation)
    VALUES (@id, @localeidEng, 'Panto item not found. Do you want to add it to basket anyway?',1)
END

IF NOT EXISTS (SELECT * FROM lng.ResourceBase WHERE Alias = 'barcodeRecognition.NG.Panto.PantoBarcodeDifferentStore')
BEGIN
	SET @id = @id+1
	INSERT INTO lng.ResourceBase (Id,SubsystemId,Alias,MaximumLength)
    VALUES (@id, @subsystem, 'barcodeRecognition.NG.Panto.PantoBarcodeDifferentStore', 500)
			
	INSERT INTO lng.ResourceText (ResourceId, LocaleId, Text, IsCustomTranslation)
    VALUES (@id, @localeidEng, 'Panto item was created in a different store',1)
END

IF NOT EXISTS (SELECT * FROM lng.ResourceBase WHERE Alias = 'barcodeRecognition.NG.Panto.PantoBarcodeIncorrectBasket')
BEGIN
	SET @id = @id+1
	INSERT INTO lng.ResourceBase (Id,SubsystemId,Alias,MaximumLength)
    VALUES (@id, @subsystem, 'barcodeRecognition.NG.Panto.PantoBarcodeIncorrectBasket', 500)
			
	INSERT INTO lng.ResourceText (ResourceId, LocaleId, Text, IsCustomTranslation)
    VALUES (@id, @localeidEng, 'Panto item cannot be add to return basket',1)
END
IF NOT EXISTS (SELECT * FROM lng.ResourceBase WHERE Alias = 'barcodeRecognition.NG.Panto.PantoBarcodePayoutBlocked')
BEGIN
	SET @id = @id+1
	INSERT INTO lng.ResourceBase (Id,SubsystemId,Alias,MaximumLength)
    VALUES (@id, @subsystem, 'barcodeRecognition.NG.Panto.PantoBarcodePayoutBlocked', 500)
			
	INSERT INTO lng.ResourceText (ResourceId, LocaleId, Text, IsCustomTranslation)
    VALUES (@id, @localeidEng, 'Winnings cannot be paid out in store, contact Pantelotteriet',1)
	INSERT INTO lng.ResourceText (ResourceId, LocaleId, Text, IsCustomTranslation)
    VALUES (@id, @localeidNor, 'Gevinst kan ikke utbetales i butikk, kontakt Pantelotteriet',1)
END
-- END Panto MESSAGES
