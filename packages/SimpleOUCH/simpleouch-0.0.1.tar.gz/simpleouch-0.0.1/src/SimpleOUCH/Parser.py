class Parser:
    def __init__(self):
        self.cache = self.Cache()

    def parse(self, input, input_type='detect'):
        """"""
        byte_list = self._toBytes(input, input_type)
        while len(byte_list) > 0:
            type = chr(byte_list[0][0])
            if type == 'O':  
                message = self._enter_order(byte_list)
                self.cache.addEnterOrder(message)
            elif type == 'U': 
                message = self._replace_order_request(byte_list)
                self.cache.addReplaceOrderRequest(message)
            elif type == 'X': 
                message = self._cancel_order_request(byte_list)
                self.cache.addCancelOrderRequest(message)
            elif type == 'M': 
                message = self._modify_order_request(byte_list)
                self.cache.addModifyOrderRequest(message)
            elif type == 'Q': 
                message = self._account_query_request(byte_list)
                self.cache.addAccountQueryRequest(message)
            elif type == 'S': 
                message = self._system_event(byte_list)
                self.cache.addSystemEvent(message)
            elif type == 'A': 
                message = self._order_accepted(byte_list)
                self.cache.addOrderAccepted(message)
            elif type == 'U': 
                message = self._order_replaced(byte_list)
                self.cache.addOrderReplaced(message)
            elif type == 'C': 
                message = self._order_canceled(byte_list)
                self.cache.addOrderCanceled(message)
            elif type == 'D': 
                message = self._aiq_canceled(byte_list)
                self.cache.addAiqCanceled(message)
            elif type == 'E': 
                message = self._order_executed(byte_list)
                self.cache.addOrderExecuted(message)
            elif type == 'B': 
                message = self._broken_trade(byte_list)
                self.cache.addBrokenTrade(message)
            elif type == 'F': 
                message = self._trade_correction(byte_list)
                self.cache.addTradeCorrection(message)
            elif type == 'J': 
                message = self._rejected(byte_list)
                self.cache.addRejected(message)
            elif type == 'P': 
                message = self._cancel_pending(byte_list)
                self.cache.addCancelPending(message)
            elif type == 'I': 
                message = self._cancel_reject(byte_list)
                self.cache.addCancelReject(message)
            elif type == 'T': 
                message = self._order_priority_update(byte_list)
                self.cache.addOrderPriorityUpdate(message)
            elif type == 'M': 
                message = self._order_modified(byte_list)
                self.cache.addOrderModified(message)
            elif type == 'R': 
                message = self._order_restated(byte_list)
                self.cache.addOrderRestated(message)
            elif type == 'Q': 
                message = self._account_query_response(byte_list)
                self.cache.addAccountQueryResponse(message)
            else:
                del byte_list[0]

    def reset(self):
        """Delete all messages"""
        self.cache = self.Cache()

    def getMessages(self):
        """Return all messages in python dictionary"""
        return self.cache.toDict()

    # Cache
    class Cache:
        # Inbound Messages
        enter_orders = [['Type','UserRefNum','Side','Quantity','Symbol','Price',
        'Time In Force','Display','Capacity','InterMarket Sweep Eligibility',
        'CrossType','ClOrdID','Appendage Length','Optional Appendage']]
        replace_order_requests = [['Type','OrigUserRefNum','UserRefNum','Quantity',
        'Price','Time In Force','Display','InterMarket Sweep Eligibility',
        'ClOrdID','Appendage Length','Optional Appendage']]
        cancel_order_requests = [['Type','UserRefNum','Quantity']]
        modify_order_requests = [['Type','UserRefNum','Side','Quantity']]
        account_query_requests = [['Type']]

        # Outbound Messages
        system_events = [['Type','Timestamp','Event Code']]
        order_accepteds = [['Type','Timestamp','UesrRefNum','Side','Quantity',
        'Symbol','Price','Time In Force','Display','Order Reference Number',
        'Capacity','InterMarket Sweep Eligibility','CrossType','Order State',
        'ClOrdID','Appendage Length','Optional Appendage']]
        order_replaceds = [['Type','Timestamp','OrigUserRefNum','UserRefNum','Side',
        'Quantity','Symbol','Price','Time In Force','Display',
        'Order Reference Number','Capacity','InterMarket Sweep Eligibility',
        'CrossType','Order State','ClOrdID','Appendage Length',
        'Optional Appendage']]
        order_canceleds = [['Type','Timestamp','UserRefNum','Quantity','Reason']]
        aiq_canceleds = [['Type','Timestamp','UserRefNum','Decrement Shares',
        'Reason','Quantity prevented from trading','Execution Price',
        'Liquidity Flag']]
        order_executeds = [['Type','Timestamp','UserRefNum','Quantity','Price',
        'Liquidity Flag','Match Number','Appendage Length','Optional Appendage']]
        broken_trades = [['Type','Timestamp','UserRefNum','Match Number','Reason',
        'ClOrdID']]
        trade_corrections = [['Type','Timestamp','UserRefNum','Quantity','Price',
        'Liquidity Flag','Match Number','Reason','ClOrdID']]
        rejecteds = [['Type','Timestamp','UserRefNum','Reason','ClOrdID']]
        cancel_pendings = [['Type','Timestamp','UserRefNum']]
        cancel_rejects = [['Type','Timestamp','UserRefNum']]
        order_priority_updates = [['Type','Timestamp','UserRefNum','Price',
        'Display', 'Order Reference Number']]
        order_modifieds = [['Type','Timestamp','UserRefNum','Side','Quantity']]
        order_restateds = [['Type','Timestamp','UserRefNum','Reason', 
        'Appendage Length','Optional Appendage']]
        account_query_responses = [['Type','Timestamp','NextUserRefNum']]

        def addEnterOrder(self, message):
            self.enter_orders.append(message)
        
        def addReplaceOrderRequest(self, message):
            self.replace_order_requests.append(message)
        
        def addCancelOrderRequest(self, message):
            self.cancel_order_requests.append(message)

        def addModifyOrderRequest(self, message):
            self.modify_order_requests.append(message)

        def addAccountQueryRequest(self, message):
            self.account_query_requests.append(message)

        def addSystemEvent(self, message):
            self.system_events.append(message)

        def addOrderAccepted(self, message):
            self.order_accepteds.append(message)

        def addOrderReplaced(self, message):
            self.order_replaceds.append(message)

        def addAiqCanceled(self, message):
            self.aiq_canceleds.append(message)

        def addOrderExecuted(self, message):
            self.order_executeds.append(message)

        def addBrokenTrade(self, message):
            self.broken_trades.append(message)

        def addTradeCorrection(self, message):
            self.trade_corrections.append(message)

        def addRejected(self, message):
            self.rejecteds.append(message)

        def addCancelPending(self, message):
            self.cancel_pendings.append(message)

        def addCancelReject(self, message):
            self.cancel_rejects.append(message)

        def addOrderPriorityUpdate(self, message):
            self.order_priority_updates.append(message)

        def addOrderModified(self, message):
            self.order_modifieds.append(message)

        def addOrderRestated(self, message):
            self.order_restateds.append(message)

        def addAccountQueryResponse(self, message):
            self.account_query_responses.append(message)

        def toDict(self):
            contents = dict()
            contents["Enter Order"] = self.enter_orders
            contents["Replace Order Request"] = self.replace_order_requests
            contents["Cancel Order Request"] = self.cancel_order_requests
            contents["Modify Order Request"] = self.modify_order_requests
            contents["Account Query Request"] = self.account_query_requests
            contents["System Event"] = self.system_events
            contents["Order Accepted"] = self.order_accepteds
            contents["Order Replaced"] = self.order_replaceds
            contents["Order Canceled"] = self.order_canceleds
            contents["AIQ Canceled"] = self.aiq_canceleds
            contents["Order Executed"] = self.order_executeds
            contents["Broken Trade"] = self.broken_trades
            contents["Trade Correction"] = self.trade_corrections
            contents["Rejected"] = self.rejecteds
            contents["Cancel Pending"] = self.cancel_pendings
            contents["Cancel Reject"] = self.cancel_rejects
            contents["Order Priority Update"] = self.order_priority_updates
            contents["Order Modified"] = self.order_modifieds
            contents["Order Restated"] = self.order_restateds
            contents["Account Query Response"] = self.account_query_responses
            
            return contents
        
        # Message Formatting
        # Inbound Messages
        def _enter_order(self, bytes: list):
            msg_end = 47 + self._toShort(bytes[45:47])
            msg = [self._toAlpha(bytes[:1]),
                    self._toUserRefNum(bytes[1:5]),
                    self._toAlpha(bytes[5:6]),
                    self._toInt(bytes[6:10]),
                    self._toAlpha(bytes[10:18]),
                    self._toPrice(bytes[18:26]),
                    self._toAlpha(bytes[26:27]),
                    self._toAlpha(bytes[27:28]),
                    self._toAlpha(bytes[28:29]),
                    self._toAlpha(bytes[29:30]),
                    self._toAlpha(bytes[30:31]),
                    self._toAlpha(bytes[31:45]),
                    self._toShort(bytes[45:47]),
                    self._getOptionalAppendage(bytes[45:msg_end])]
            del bytes[:msg_end]
            return msg

        def _replace_order_request(self, bytes: list):
            msg_end = 40 + self._toShort(bytes[38:40])
            msg = [self._toAlpha(bytes[:1]),
                    self._toUserRefNum(bytes[1:5]),
                    self._toUserRefNum(bytes[5:9]),
                    self._toInt(bytes[9:13]),
                    self._toPrice(bytes[13:21]),
                    self._toAlpha(bytes[21:22]),
                    self._toAlpha(bytes[22:23]),
                    self._toAlpha(bytes[23:24]),
                    self._toAlpha(bytes[24:38]),
                    self._toShort(bytes[38:40]),
                    self._getOptionalAppendage(bytes[38:msg_end])]
            del bytes[:msg_end]
            return msg

        def _cancel_order_request(self, bytes: list):
            msg = [self._toAlpha(bytes[:1]),
                    self._toUserRefNum(bytes[1:5]),
                    self._toInt(bytes[5:9])]
            del bytes[:9]
            return msg
            
        def _modify_order_request(self, bytes: list):
            msg = [self._toAlpha(bytes[:1]),
                    self._toUserRefNum(bytes[1:5]),
                    self._toAlpha(bytes[5:6]),
                    self._toInt(bytes[6:10])]
            del bytes[:10]
            return msg

        def _account_query_request(self, bytes: list):
            msg = [self._toAlpha(bytes[:1])]
            del bytes[:1]
            return msg

        # Outbound messages
        def _system_event(self, bytes: list):
            msg = [self._toAlpha(bytes[:1]),
                    self._toTimestamp(bytes[1:9]),
                    self._toAlpha(bytes[9:10])]
            del bytes[:10]
            return msg

        def _order_accepted(self, bytes: list):
            msg_end = 64 + self._toShort(bytes[62:64])
            msg = [self._toAlpha(bytes[:1]),
                    self._toTimestamp(bytes[1:9]),
                    self._toUserRefNum(bytes[9:13]),
                    self._toAlpha(bytes[13:14]),
                    self._toInt(bytes[14:18]),
                    self._toAlpha(bytes[18:26]),
                    self._toPrice(bytes[26:34]),
                    self._toAlpha(bytes[34:35]),
                    self._toAlpha(bytes[35:36]),
                    self._toLong(bytes[36:44]),
                    self._toAlpha(bytes[44:45]),
                    self._toAlpha(bytes[45:46]),
                    self._toAlpha(bytes[46:47]),
                    self._toAlpha(bytes[47:48]),
                    self._toAlpha(bytes[48:62]),
                    self._toShort(bytes[62:64]),
                    self._toOptionalAppendage(bytes[62:msg_end])]
            del bytes[:msg_end]
            return msg

        def _order_replaced(self, bytes: list):
            msg_end = 68 + self._toShort(bytes[66:68])
            msg = [self._toAlpha(bytes[:1]),
                    self._toTimestamp(bytes[1:9]),
                    self._toUserRefNum(bytes[9:13]),
                    self._toUserRefNum(bytes[13:17]),
                    self._toAlpha(bytes[17:18]),
                    self._toInt(bytes[18:22]),
                    self._toAlpha(bytes[22:30]),
                    self._toPrice(bytes[30:38]),
                    self._toAlpha(bytes[38:39]),
                    self._toAlpha(bytes[39:40]),
                    self._toLong(bytes[40:48]),
                    self._toAlpha(bytes[49:49]),
                    self._toAlpha(bytes[49:50]),
                    self._toAlpha(bytes[50:51]),
                    self._toAlpha(bytes[51:52]),
                    self._toAlpha(bytes[52:66]),
                    self._toShort(bytes[66:68]),
                    self._toOptionalAppendage(bytes[66:msg_end])]
            del bytes[:msg_end]
            return msg

        def _order_canceled(self, bytes: list):
            msg = [self._toAlpha(bytes[:1]),
                    self._toTimestamp(bytes[1:9]),
                    self._toUserRefNum(bytes[9:13]),
                    self._toInt(bytes[13:17]),
                    self._toByte(bytes[17:18])]
            del bytes[:18]
            return msg

        def _aiq_canceled(self, bytes: list):
            msg = [self._toAlpha(bytes[:1]),
                    self._toTimestamp(bytes[1:9]),
                    self._toUserRefNum(bytes[9:13]),
                    self._toInt(bytes[13:17]),
                    self._toByte(bytes[17:18]),
                    self._toInt(bytes[18:22]),
                    self._toPrice(bytes[22:30]),
                    self._toAlpha(bytes[30:31])] 
            del bytes[:31]
            return msg

        def _order_executed(self, bytes: list):
            msg_end = 36 + self._toShort(bytes[34:36])
            msg = [self._toAlpha(bytes[:1]),
                    self._toTimestamp(bytes[1:9]),
                    self._toUserRefNum(bytes[9:13]),
                    self._toInt(bytes[13:17]),
                    self._toPrice(bytes[17:25]),
                    self._toAlpha(bytes[25:26]),
                    self._toLong(bytes[26:34]),
                    self._toShort(bytes[34:36]),
                    self._toOptionalAppendage(bytes[34:msg_end])]
            del bytes[:msg_end]
            return msg

        def _broken_trade(self, bytes: list):
            msg = [self._toAlpha(bytes[:1]),
                    self._toTimestamp(bytes[1:9]),
                    self._toUserRefNum(bytes[9:13]),
                    self._toLong(bytes[13:21]),
                    self._toAlpha(bytes[21:22]),
                    self._toAlpha(bytes[22:36])]
            del bytes[:36]
            return msg

        def _trade_correction(self, bytes: list):
            msg = [self._toAlpha(bytes[:1]),
                    self._toTimestamp(bytes[1:9]),
                    self._toUserRefNum(bytes[9:13]),
                    self._toInt(bytes[13:17]),
                    self._toPrice(bytes[17:25]),
                    self._toAlpha(bytes[25:26]),
                    self._toLong(bytes[26:34]),
                    self._toAlpha(bytes[34:35]),
                    self._toAlpha(bytes[35:49])]
            del bytes[:49]
            return msg

        def _rejected(self, bytes: list):
            msg = [self._toAlpha(bytes[:1]),
                    self._toTimestamp(bytes[1:9]),
                    self._toUserRefNum(bytes[9:13]),
                    self._toShort(bytes[13:15]),
                    self._toAlpha(bytes[15:29])]
            del bytes[:29]
            return msg

        def _cancel_pending(self, bytes: list):
            msg = [self._toAlpha(bytes[:1]),
                    self._toTimestamp(bytes[1:9]),
                    self._toUserRefNum(bytes[9:13])]
            del bytes[:13]
            return msg

        def _cancel_reject(self, bytes: list):
            msg = [self._toAlpha(bytes[:1]),
                    self._toTimestamp(bytes[1:9]),
                    self._toUserRefNum(bytes[9:13])]
            del bytes[:13]
            return msg

        def _order_priority_update(self, bytes: list):
            msg = [self._toAlpha(bytes[:1]),
                    self._toTimestamp(bytes[1:9]),
                    self._toUserRefNum(bytes[9:13]),
                    self._toAlpha(bytes[13:21]),
                    self._toAlpha(bytes[21:22]),
                    self._toLong(bytes[22:30])]
            del bytes[:30]
            return msg

        def _order_modified(self, bytes: list):
            msg = [self._toAlpha(bytes[:1]),
                    self._toTimestamp(bytes[1:9]),
                    self._toUserRefNum(bytes[9:13]),
                    self._toAlpha(bytes[13:12]),
                    self._toInt(bytes[14:18])]
            del bytes[:18]
            return msg

        def _order_restated(self, bytes: list):
            msg_end =  16 + self._toShort(bytes[14:16])
            msg = [self._toAlpha(bytes[:1]),
                    self._toTimestamp(bytes[1:9]),
                    self._toUserRefNum(bytes[9:13]),
                    self._toAlpha(bytes[13:14]),
                    self._toShort(bytes[14:16]),
                    self._toOptionalAppendage(bytes[14:msg_end])]
            del bytes[:msg_end]
            return msg
                    

        def _account_query_response(self, bytes: list):
            msg = [self._toAlpha(bytes[:1]),
                    self._toTimestamp(bytes[1:9]),
                    self._toUserRefNum(bytes[9:13])]
            del bytes[:13]
            return msg
        
        # Field Formatting
        def _stripNulls(self, data):
            # Several data types are padded to the right with \x00
            while data[-1] == b'\x00':
                data = data[:-1]
            return data

        def _joinBytes(self, data):
            joined_data = b''
            for val in data:
                joined_data += val 
            return joined_data

        def _toLong(self, data) -> int:
            assert type(data[0]) == bytes
            assert len(data) == 8
            return int.from_bytes(self._joinBytes(data), byteorder='big')

        def _toInt(self, data) -> int:
            assert(type(data[0]) == bytes)
            assert(len(data) == 4)
            return int.from_bytes(self._joinBytes(data), byteorder='big')

        def _toShort(self, data) -> int:
            assert type(data[0]) == bytes
            assert len(data) == 2
            return int.from_bytes(self._joinBytes(data), byteorder='big')

        def _toByte(self, data) -> int:
            assert type(data[0]) == bytes
            assert len(data) == 1
            return int.from_bytes(self._joinBytes(data), byteorder='big')

        def _toPrice(self, data) -> float:
            assert type(data[0]) == bytes
            return float(int.from_bytes(self._joinBytes(data), byteorder='big'))/1000

        def _toSignedPrice(self, data) -> float:
            assert type(data[0]) == bytes
            assert len(data) == 4
            return float(int.from_bytes(self._joinBytes(data), byteorder='big'))/1000

        def _toTimestamp(self, data) -> int:
            # Nanoseconds since midnight
            assert type(data[0]) == bytes
            assert len(data) == 8
            return self._toLong(data)

        def _toAlpha(self, data) -> str:
            assert type(data[0]) == bytes
            data = self._stripNulls(data)
            return ''.join([chr(byte[0]) for byte in data])

        def _toUserRefNum(self, data):
            assert type(data[0]) == bytes
            assert(len(data) == 4)
            return self._toAlpha(data)

        # Optional Appendage Formatting
        def _toOptionalAppendage(self, message):
            assert type(message[0]) == bytes
            msg_len = self._toShort(message[:2])
            i = 2
            fields = []
            while msg_len > 0:
                assert i < len(message), "Invalid input in optional appendage"
                field_type = self._toByte(message[i:i+1])
                field_len = self._getFieldLength(field_type)
                field = self._getField(message, i, field_type, field_len)
                fields.append(field)
                i += field_len
                msg_len -= field_len
            return fields

        def _getField(self, message, i: int, field_type: int, field_len: int):
                if field_type == 1:
                    return ("SecondaryOrdRefNum", self._toLong(message[i:i+field_len]))
                elif field_type == 2:
                    return ("Firm",self._toAlpha(message[i:i+field_len]))
                elif field_type == 3:
                    return ("MinQty",self._toInt(message[i:i+field_len]))
                elif field_type == 4:
                    return ("CustomerType", self._toAlpha(message[i:i+field_len]))
                elif field_type == 5:
                    return ("MaxFloor",self._toInt(message[i:i+field_len]))
                elif field_type == 6:
                    return ("PriceType",self._toAlpha(message[i:i+field_len]))
                elif field_type == 7:
                    return ("PegOffset",self._toSignedPrice(message[i:i+field_len]))
                elif field_type == 9:
                    return ("DiscretionPrice",self._toPrice(message[i:i+field_len]))
                elif field_type == 10:
                    return ("DiscretionPriceType",self._toAlpha(message[i:i+field_len]))
                elif field_type == 11:
                    return ("DiscretionPegOffset",self._toSignedPrice(message[i:i+field_len]))
                elif field_type == 12:
                    return ("PostOnly",self._toAlpha(message[i:i+field_len]))
                elif field_type == 13:
                    return ("RandomReserves",self._toInt(message[i:i+field_len]))
                elif field_type == 14:
                    return ("Route",self._toAlpha(message[i:i+field_len]))
                elif field_type == 15:
                    return ("ExpireTime",self._toInt(message[i:i+field_len]))
                elif field_type == 16:
                    return ("TradeNow",self._toAlpha(message[i:i+field_len]))
                elif field_type == 17:
                    return ("HandleInst",self._toAlpha(message[i:i+field_len]))
                elif field_type == 18:
                    return ("BBO Weight Indicator",self._toAlpha(message[i:i+field_len]))
                elif field_type == 19:
                    return ("Reference Price",self._toPrice(message[i:i+field_len]))
                elif field_type == 20:
                    return ("Reference Price Type",self._toAlpha(message[i:i+field_len]))
                elif field_type == 22:
                    return ("Display Quantity",self._toInt(message[i:i+field_len]))
                elif field_type == 23:
                    return ("Display Price",self._toPrice(message[i:i+field_len]))
                elif field_type == 24:
                    return ("Group ID",self._toShort(message[i:i+field_len]))
                elif field_type == 25:
                    return ("Shares Located",self._toAlpha(message[i:i+field_len]))
                else:
                    raise ValueError("Optional field contains invalid field type") 

        def _getFieldLength(self, field_type: int):
                if field_type == 1:
                    return 16
                elif field_type == 2:
                    return 8
                elif field_type == 3:
                    return 8
                elif field_type == 4:
                    return 2
                elif field_type == 5:
                    return 8
                elif field_type == 6:
                    return 2
                elif field_type == 7:
                    return 8
                elif field_type == 9:
                    return 16
                elif field_type == 10:
                    return 2
                elif field_type == 11:
                    return 8
                elif field_type == 12:
                    return 2
                elif field_type == 13:
                    return 8
                elif field_type == 14:
                    return 8
                elif field_type == 15:
                    return 8
                elif field_type == 16:
                    return 2
                elif field_type == 17:
                    return 2
                elif field_type == 18:
                    return 2
                elif field_type == 19:
                    return 16
                elif field_type == 20:
                    return 2
                elif field_type == 22:
                    return 8
                elif field_type == 23:
                    return 16
                elif field_type == 24:
                    return 4
                elif field_type == 25:
                    return 2
                else:
                    raise ValueError("Optional field contains invalid field type")
                

        # Input formatting
        def _toBytes(self, input, input_type):
            valid_input_types = {'detect','bytes','hex_str','binary_str','decimal_str',
                                'byte_list','hex_str_list','binary_str_list',
                                'decimal_str_list','int_list'}
            assert input_type in valid_input_types
            if input_type == 'detect':
                input_type = self._detectInputType(input)
            
            if input_type == 'bytes': return self._bytesToByteList(input)
            elif input_type == 'hex_str': return self._hexStrToByteList(input)
            elif input_type == 'binary_str': return self._binaryStrToByteList(input)
            elif input_type == 'byte_list': return self._formatByteList(input)
            elif input_type == 'hex_str_list': return self._hexStrListToByteList(input)
            elif input_type == 'binary_str_list': return self._binaryStrListToByteList(input)
            elif input_type == 'int_list': return self._intListToByteList(input)
            else: raise TypeError("Invalid input. Must be of type bytes, str,"
                                "List[bytes], List[str], or List[int]")
            

        def _detectInputType(self, input):
            # Check input type
            input_type = type(input)
            if input_type == bytes:
                return 'bytes'

            if input_type != str and input_type != list:
                return "error"

            type_first_value = type(input[0])
            if type_first_value == bytes:
                return 'byte_list'
            elif type_first_value == int:
                return 'int_list'

            if type_first_value != str:
                return "error"

            # Check v
            sample = input[:1000].replace('\n','').replace(' ','').replace('\t','')

            values = set()
            for val in sample:
                values.add(val)
            
            if values.issubset({'0', '1'}):
                if input_type != list:
                    return 'binary_str'
                else:
                    return 'binary_str_list'
            
            elif values.issubset({'0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f'}):
                if input_type != list:
                    return 'hex_str'
                else:
                    return 'hex_str_list'

            else:
                return 'error'

        def _bytesToByteList(self, input):
            return [byte.to_bytes(1,byteorder='big') for byte in input]

        def _hexStrToByteList(self, input):
            byte_list = []
            input = input.replace(' ','').replace('\n','').replace('\t','')
            for i in range(0,len(input),2):
                byte_list.append(int(input[i:i+2],base=16).to_bytes(1,byteorder='big'))
            return byte_list

        def _binaryStrToByteList(self, input):
            byte_list = []
            for i in range(0,len(input),8):
                byte_list.append(int(input[i:i+8],base=2).to_bytes(1,byteorder='big'))
            return byte_list

        def _formatByteList(self, input):
            for byte in input:
                assert len(byte == 1), "Byte list must contain bytes of len 1"
            return input

        def _hexStrListToByteList(self, input):
            assert len(input[0]) == 2
            return [int(val,base=16).to_bytes(1,byteorder='big') for val in input]

        def _binaryStrListToByteList(self, input):
            return [int(val,base=2).to_bytes(1,byteorder='big') for val in input]

        def _intListToByteList(self, input):
            return [val.to_bytes(1,byteorder='big') for val in input]