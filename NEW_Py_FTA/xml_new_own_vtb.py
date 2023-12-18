xml_new_own_vtb = '''
<soapenv:Envelope xsi:schemaLocation="http://x-artefacts-epts-ru/ELPTSOwner/1.0.3 ELPTSOwner_v1.0.3.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:urn1="urn://x-artefacts-epts-ru/EPTS_Services/1.0.1" xmlns:trsdo="urn://x-artefacts-epts-ru/EEC_M_TR_SimpleDataObjects/1.0.8" xmlns:pas="http://passport.integration.pts.fors.ru/" xmlns:doc="urn://x-artefacts-epts-ru/ELPTSOwner/1.0.3" xmlns:csdo="urn://x-artefacts-epts-ru/EEC_M_SimpleDataObjects/0.4.7" xmlns:ccdo="urn://x-artefacts-epts-ru/EEC_M_ComplexDataObjects/0.4.16" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
	<soapenv:Header/>
	<soapenv:Body>
		<pas:ELPTSOwner>
			<MessageType>REQUEST</MessageType>
			<RequestMessage>
				<urn1:MessageID>{0}</urn1:MessageID>
				<urn1:MessageMetadata>
					<urn1:Sender>
						<urn1:Mnemonic>{2}</urn1:Mnemonic>
						<urn1:HumanReadableName>Акционерное общество "ПЕП"</urn1:HumanReadableName>
						<!--<urn1:Mnemonic>RUOWNER000017</urn1:Mnemonic><urn1:HumanReadableName>АО "ЭЛЕКТРОННЫЙ ПАСПОРТ"</urn1:HumanReadableName>-->
					</urn1:Sender>
					<urn1:SendingTimestamp>2018-12-28</urn1:SendingTimestamp>
					<urn1:Recipient>
						<urn1:Mnemonic>ELPTS</urn1:Mnemonic>
						<urn1:HumanReadableName>ИС СИСТЕМЫ ЭЛЕКТРОННЫХ ПАСПОРТОВ</urn1:HumanReadableName>
					</urn1:Recipient>
				</urn1:MessageMetadata>
				<urn1:SenderProvidedRequestData>
					<urn1:ApplicationInfoContainers>
						<urn1:ApplicationInfoContainer>
							<urn1:ApplicationID>027</urn1:ApplicationID>
							<urn1:ApplicationName>Заявление на внесение сведений о новом собственнике</urn1:ApplicationName>
						</urn1:ApplicationInfoContainer>
					</urn1:ApplicationInfoContainers>
					<urn1:MessagePrimaryContent id="contentWithPersonalSignature">
						<doc:ELPTSOwnerAppRequest>
							<ccdo:BaseForChangeDocument>
								<ccdo:DocType>OwnershipConfirm</ccdo:DocType>
								<csdo:DocName>Заявление на внесение сведений о новом собственнике (наименование)</csdo:DocName>
								<csdo:DocId>123</csdo:DocId>
								<csdo:DocCreationDate>2020-04-11</csdo:DocCreationDate>
							</ccdo:BaseForChangeDocument>
							<doc:EPassportsList>
								<doc:EPassportNumber>{1}</doc:EPassportNumber>
								<doc:VehicleMileage measurementUnitCode="KMT">10.0</doc:VehicleMileage>
								<!--<doc:VehicleCost currencyCodeListId="NSI_078" currencyCode="RUB">10000.0</doc:VehicleCost>-->
							</doc:EPassportsList>
							<doc:SignersList>
								<doc:SignerTypeCode>3</doc:SignerTypeCode>
								<ccdo:OwnerOrganizationDetails>
									<ccdo:EECCountryCode>RU</ccdo:EECCountryCode>
									<csdo:OrganizationName>ВТБ ЛИЗИНГ (АКЦИОНЕРНОЕ ОБЩЕСТВО)</csdo:OrganizationName>
									<ccdo:OrganizationId kindId="1">1037700259244</ccdo:OrganizationId>
									<ccdo:OrganizationTaxpayerId>7709378229</ccdo:OrganizationTaxpayerId>
									<csdo:TaxRegistrationReasonCode>997950001</csdo:TaxRegistrationReasonCode>
								</ccdo:OwnerOrganizationDetails>
								<doc:CommunicationDetails CommunicationChannelCode="EM">125@elpts.ru</doc:CommunicationDetails>
							</doc:SignersList>
						</doc:ELPTSOwnerAppRequest>
					</urn1:MessagePrimaryContent>
					<urn1:PersonalSignature/>
					<!--первая подпись (должностное лицо)-->
				</urn1:SenderProvidedRequestData>
				<urn1:SenderInformationSystemSignature/>
				<!--вторая подпись (системная)-->
			</RequestMessage>
		</pas:ELPTSOwner>
		<!--<pas:ELPTSOwnerAppList/>-->
	</soapenv:Body>
</soapenv:Envelope>
'''