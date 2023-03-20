DECLARE @orgNodeNmbr int;
DECLARE @modifiedBy int;

SET @orgNodeNmbr = 1 -- change if needed
SET @modifiedBy = 6 -- change if needed

DECLARE @json nvarchar(max);
DECLARE @translationJson nvarchar(max);

DECLARE @mopState int
DECLARE @mopGroupId int

-- Create EFT MOP GROUP
IF NOT EXISTS (SELECT 1 FROM mdd.MOPGroup WHERE [Name] = 'EFT')
BEGIN 
	PRINT 'Create EFT MOP GROUP'

	SET @mopState = 1 -- change if needed - 0 = draft, 1 = active

	SET @json = '{"EntityNo":0,"Name":"EFT","Description":"EFT Payment","Number":3,"EntityStateId":<entity_state>,"EntityStateName":null,"EntityStateDescription":null,"Translations":null}'
	SET @json = REPLACE(@json,'<entity_state>', @mopState)

	SET @translationJson = '[{"AttributeName":"Name","LCID":"en-US","TranslationText":"EFT"},{"AttributeName":"Description","LCID":"en-US","TranslationText":"EFT Payment"}]'

	EXEC mdd.spMOPGroupModify @orgNodeNmbr, @json, @translationJson
END

-- Create EFT MOP
IF NOT EXISTS (SELECT 1 FROM mdd.MethodOfPayment WHERE MOPTypeId = 4)
BEGIN
	PRINT 'Create EFT MOP'

	SELECT @mopGroupId = EntityNo FROM mdd.MOPGroup WHERE [Name] = 'EFT'
	SET @mopState = 1 -- change if needed - 0 = draft, 1 = active

	SET @json = '{"EntityNo":0,"Name":"EFT","Description":"EFT in NOK","Number":4,"MOPTypeId":4,"MopTypeDescription":null,"MOPGroupNo":<mop_group>,"MopGroupName":null,"OverpaymentRuleId":0,"RefundRuleId":1,"CurrencyNo":null,"CurrencyMajorUnitLongName":null,"OpenCashdrawerRule":0,"EntityStateId":<entity_state>,"EntityStateName":null,"FeeTypeId":1,"FeeRate":null,"FeeArticleNo":null,"HasFee":false,"PrintRuleTypeId":0,"NumberOfCopies":0,"CompanyIdentifier":"3","ExternalIdentifier":null,"IsLocked":false,"IsLockedText":null,"SplitPaymentTypeId":1,"DeductabilityTypeId":0,"UseInquiries":false,"InquiryNo":null,"IsSafeDropEnabled":false,"SafeDropWarningLimit":0.0,"IsShiftDeclarationEnabled":false,"MeasureUnitNo":null,"OwnerNodeNo":1,"RestrictionGroupNo":null,"IsRestrictionGroupBlackList":true,"MOPDenominations":[],"MOPSafeDropLimits":[],"OverpaymentCombinations":[],"PartialPaymentCombinations":[],"RefundCombinations":[],"DiscountRestrictions":[{"MOPDiscountTypeId":1,"MOPDiscountTypeName":"Loyalty points","MOPDiscountRestrictionTypeId":1,"MOPDiscountRestrictionTypeName":"Allowed","IsControlledByPos":false},{"MOPDiscountTypeId":2,"MOPDiscountTypeName":"POS discounts","MOPDiscountRestrictionTypeId":1,"MOPDiscountRestrictionTypeName":"Allowed","IsControlledByPos":false},{"MOPDiscountTypeId":3,"MOPDiscountTypeName":"Payment card","MOPDiscountRestrictionTypeId":1,"MOPDiscountRestrictionTypeName":"Allowed","IsControlledByPos":false},{"MOPDiscountTypeId":4,"MOPDiscountTypeName":"External discounts","MOPDiscountRestrictionTypeId":1,"MOPDiscountRestrictionTypeName":"Allowed","IsControlledByPos":false}],"Translations":null}'
	SET @json = REPLACE(@json,'<entity_state>', @mopState)
	SET @json = REPLACE(@json,'<mop_group>', @mopGroupId)

	SET @translationJson = '[{"AttributeName":"Name","LCID":"en-US","TranslationText":"EFT"},{"AttributeName":"Description","LCID":"en-US","TranslationText":"EFT in NOK"}]'

	EXEC mdd.spMopModify @json, @orgNodeNmbr, @modifiedBy, @translationJson
END
ELSE
BEGIN
	PRINT 'Update EFT MOP'

	UPDATE [mdd].[MethodOfPayment] 
	SET [OverpaymentRuleId] = 0, [CurrencyNo] = NULL, [OpenCashdrawerRule] = 0, [EntityStateId] = 1, [FeeTypeId] = 1, [FeeRate] = NULL, [FeeArticleNo] = NULL, [HasFee] = 0, [PrintRuleTypeId] = 0, [NumberOfCopies] = 0, [CompanyIdentifier] = '3', [ExternalIdentifier] = NULL, [IsLocked] = 0, [SplitPaymentTypeId] = 1, [DeductabilityTypeId] = 0, [UseInquiries] = 0, [IsSafeDropEnabled] = 0, [SafeDropWarningLimit] = 0.00000000, [IsShiftDeclarationEnabled] = 0, [MeasureUnitNo] = NULL, [OwnerNodeNo] = 1, [RestrictionGroupNo] = NULL, [IsRestrictionGroupBlackList] = 1, [RefundRuleId] = 1
	WHERE [MOPTypeId] = 4
END

-- Create EFT MOP Type
IF NOT EXISTS (SELECT 1 FROM dict.MOPType WHERE [Name] = 'Card with cashback')
BEGIN
	INSERT INTO [dict].[MOPType] VALUES ( 7,'Card with cashback','Card with cashback', 0)
END
else
BEGIN
	UPDATE [dict].[MOPType] set Name = 'Card with cashback', Description = 'Card with cashback' where Id = 7
END
-- Create EFT CASHBACK MOP
IF NOT EXISTS (SELECT 1 FROM mdd.MethodOfPayment WHERE MOPTypeId = 7)
BEGIN
	PRINT 'Create EFT CASHBACK MOP'

	SELECT @mopGroupId = EntityNo FROM mdd.MOPGroup WHERE [Name] = 'EFT'
	SET @mopState = 1 -- change if needed - 0 = draft, 1 = active

	SET @json = '{"EntityNo":0,"Name":"EFT","Description":"Card with cashback","Number":3,"MOPTypeId":7,"MopTypeDescription":null,"MOPGroupNo":<mop_group>,"MopGroupName":null,"OverpaymentRuleId":0,"RefundRuleId":2,"CurrencyNo":null,"CurrencyMajorUnitLongName":null,"OpenCashdrawerRule":0,"EntityStateId":<entity_state>,"EntityStateName":null,"FeeTypeId":1,"FeeRate":null,"FeeArticleNo":null,"HasFee":false,"PrintRuleTypeId":0,"NumberOfCopies":0,"CompanyIdentifier":"3","ExternalIdentifier":null,"IsLocked":false,"IsLockedText":null,"SplitPaymentTypeId":1,"DeductabilityTypeId":0,"UseInquiries":false,"InquiryNo":null,"IsSafeDropEnabled":false,"SafeDropWarningLimit":0.0,"IsShiftDeclarationEnabled":false,"MeasureUnitNo":null,"OwnerNodeNo":1,"RestrictionGroupNo":null,"IsRestrictionGroupBlackList":true,"MOPDenominations":[],"MOPSafeDropLimits":[],"OverpaymentCombinations":[],"PartialPaymentCombinations":[],"RefundCombinations":[],"DiscountRestrictions":[{"MOPDiscountTypeId":1,"MOPDiscountTypeName":"Loyalty points","MOPDiscountRestrictionTypeId":1,"MOPDiscountRestrictionTypeName":"Allowed","IsControlledByPos":false},{"MOPDiscountTypeId":2,"MOPDiscountTypeName":"POS discounts","MOPDiscountRestrictionTypeId":1,"MOPDiscountRestrictionTypeName":"Allowed","IsControlledByPos":false},{"MOPDiscountTypeId":3,"MOPDiscountTypeName":"Payment card","MOPDiscountRestrictionTypeId":1,"MOPDiscountRestrictionTypeName":"Allowed","IsControlledByPos":false},{"MOPDiscountTypeId":4,"MOPDiscountTypeName":"External discounts","MOPDiscountRestrictionTypeId":1,"MOPDiscountRestrictionTypeName":"Allowed","IsControlledByPos":false}],"Translations":null}'
	SET @json = REPLACE(@json,'<entity_state>', @mopState)
	SET @json = REPLACE(@json,'<mop_group>', @mopGroupId)

	SET @translationJson = '[{"AttributeName":"Name","LCID":"en-US","TranslationText":"EFT"},{"AttributeName":"Description","LCID":"en-US","TranslationText":"Card with cashback"}]'

	EXEC mdd.spMopModify @json, @orgNodeNmbr, @modifiedBy, @translationJson
END
ELSE
BEGIN
	PRINT 'Update EFT CASHBACK MOP'

	UPDATE [mdd].[MethodOfPayment] 
	SET [OverpaymentRuleId] = 0, [CurrencyNo] = NULL, [OpenCashdrawerRule] = 0, [EntityStateId] = 1, [FeeTypeId] = 1, [FeeRate] = NULL, [FeeArticleNo] = NULL, [HasFee] = 0, [PrintRuleTypeId] = 0, [NumberOfCopies] = 0, [CompanyIdentifier] = '3', [ExternalIdentifier] = NULL, [IsLocked] = 0, [SplitPaymentTypeId] = 1, [DeductabilityTypeId] = 0, [UseInquiries] = 0, [IsSafeDropEnabled] = 0, [SafeDropWarningLimit] = 0.00000000, [IsShiftDeclarationEnabled] = 0, [MeasureUnitNo] = NULL, [OwnerNodeNo] = 1, [RestrictionGroupNo] = NULL, [IsRestrictionGroupBlackList] = 1, [RefundRuleId] = 2
	WHERE [MOPTypeId] = 7
END

-- Create EFT Fallback MOP
IF NOT EXISTS (SELECT 1 FROM mdd.MethodOfPayment WHERE MOPTypeId = 6)
BEGIN
	PRINT 'Create EFT Fallback MOP'

	SELECT @mopGroupId = EntityNo FROM mdd.MOPGroup WHERE [Name] = 'EFT'
	SET @mopState = 1 -- change if needed - 0 = draft, 1 = active

	SET @json = '{"EntityNo":0,"Name":"EFT","Description":"Eft Fallback","Number":7,"MOPTypeId":6,"MopTypeDescription":null,"MOPGroupNo":<mop_group>,"MopGroupName":null,"OverpaymentRuleId":0,"RefundRuleId":1,"CurrencyNo":null,"CurrencyMajorUnitLongName":null,"OpenCashdrawerRule":0,"EntityStateId":<entity_state>,"EntityStateName":null,"FeeTypeId":1,"FeeRate":null,"FeeArticleNo":null,"HasFee":false,"PrintRuleTypeId":0,"NumberOfCopies":0,"CompanyIdentifier":"3","ExternalIdentifier":null,"IsLocked":false,"IsLockedText":null,"SplitPaymentTypeId":1,"DeductabilityTypeId":0,"UseInquiries":false,"InquiryNo":null,"IsSafeDropEnabled":false,"SafeDropWarningLimit":0.0,"IsShiftDeclarationEnabled":false,"MeasureUnitNo":null,"OwnerNodeNo":1,"RestrictionGroupNo":null,"IsRestrictionGroupBlackList":true,"MOPDenominations":[],"MOPSafeDropLimits":[],"OverpaymentCombinations":[],"PartialPaymentCombinations":[],"RefundCombinations":[],"DiscountRestrictions":[{"MOPDiscountTypeId":1,"MOPDiscountTypeName":"Loyalty points","MOPDiscountRestrictionTypeId":1,"MOPDiscountRestrictionTypeName":"Allowed","IsControlledByPos":false},{"MOPDiscountTypeId":2,"MOPDiscountTypeName":"POS discounts","MOPDiscountRestrictionTypeId":1,"MOPDiscountRestrictionTypeName":"Allowed","IsControlledByPos":false},{"MOPDiscountTypeId":3,"MOPDiscountTypeName":"Payment card","MOPDiscountRestrictionTypeId":1,"MOPDiscountRestrictionTypeName":"Allowed","IsControlledByPos":false},{"MOPDiscountTypeId":4,"MOPDiscountTypeName":"External discounts","MOPDiscountRestrictionTypeId":1,"MOPDiscountRestrictionTypeName":"Allowed","IsControlledByPos":false}],"Translations":null}'
	SET @json = REPLACE(@json,'<entity_state>', @mopState)
	SET @json = REPLACE(@json,'<mop_group>', @mopGroupId)

	SET @translationJson = '[{"AttributeName":"Name","LCID":"en-US","TranslationText":"EFT Fallback"},{"AttributeName":"Description","LCID":"en-US","TranslationText":"EFT Fallback"}]'

	EXEC mdd.spMopModify @json, @orgNodeNmbr, @modifiedBy, @translationJson
END
ELSE
BEGIN
	PRINT 'Update EFT Fallback MOP'

	UPDATE [mdd].[MethodOfPayment]
	SET [OverpaymentRuleId] = 0, [CurrencyNo] = NULL, [OpenCashdrawerRule] = 0, [EntityStateId] = 1, [FeeTypeId] = 1, [FeeRate] = NULL, [FeeArticleNo] = NULL, [HasFee] = 0, [PrintRuleTypeId] = 0, [NumberOfCopies] = 0, [CompanyIdentifier] = '3', [ExternalIdentifier] = NULL, [IsLocked] = 0, [SplitPaymentTypeId] = 1, [DeductabilityTypeId] = 0, [UseInquiries] = 0, [IsSafeDropEnabled] = 0, [SafeDropWarningLimit] = 0.00000000, [IsShiftDeclarationEnabled] = 0, [MeasureUnitNo] = NULL, [OwnerNodeNo] = 1, [RestrictionGroupNo] = NULL, [IsRestrictionGroupBlackList] = 1, [RefundRuleId] = 1
	WHERE [MOPTypeId] = 6
END

-- MOPCombination for partial payments (2) and refund (3)
PRINT 'Create MOPCombination'

DECLARE @eftEntityNo int
DECLARE @fallbackEntityNo int
DECLARE @nokEntityNo int

SELECT @eftEntityNo = EntityNo FROM mdd.MethodOfPayment WHERE MOPTypeId = 4 -- 4 means Card
SELECT @fallbackEntityNo = EntityNo FROM mdd.MethodOfPayment WHERE MOPTypeId = 6 -- 6 means Eft Fallback
SELECT @nokEntityNo = MAX(EntityNo) FROM mdd.MethodOfPayment WHERE MOPTypeId = 0 -- 0 means Cash (Max to get Cash in NOK)

DELETE FROM mdd.MOPCombination WHERE MethodOfPaymentNo = @eftEntityNo
DELETE FROM mdd.MOPCombination WHERE MethodOfPaymentNo = @fallbackEntityNo
DELETE FROM mdd.MOPCombination WHERE MethodOfPaymentNo = @nokEntityNo

INSERT INTO [mdd].[MOPCombination]([MethodOfPaymentNo], [MOPCombinationTypeId], [CombinedWithMopNo])
VALUES	(@eftEntityNo, 2, @eftEntityNo),
		(@eftEntityNo, 2, @fallbackEntityNo),
		(@eftEntityNo, 2, @nokEntityNo),
		(@eftEntityNo, 3, @eftEntityNo),
		(@eftEntityNo, 3, @fallbackEntityNo),
		(@eftEntityNo, 3, @nokEntityNo),
		(@fallbackEntityNo, 2, @eftEntityNo),
		(@fallbackEntityNo, 2, @fallbackEntityNo),
		(@fallbackEntityNo, 2, @nokEntityNo),
		(@fallbackEntityNo, 3, @eftEntityNo),
		(@fallbackEntityNo, 3, @fallbackEntityNo),
		(@fallbackEntityNo, 3, @nokEntityNo),
		(@nokEntityNo, 2, @eftEntityNo),
		(@nokEntityNo, 2, @fallbackEntityNo),
		(@nokEntityNo, 2, @nokEntityNo),
		(@nokEntityNo, 3, @eftEntityNo),
		(@nokEntityNo, 3, @fallbackEntityNo),
		(@nokEntityNo, 3, @nokEntityNo)


-- Configure MOP allow for returns
PRINT 'Configure MOP allow for returns'

UPDATE config.ConfigurationValue
SET Value = '["0","1","2","3","4","6"]'
WHERE SettingId = 141
