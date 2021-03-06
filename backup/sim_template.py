
sim_template = '''
###########################################
#         Auto Generated                  #
###########################################
<config sw> Protocol = 29
<config sw> PIN_KRX_CANH = 6
<config sw> TYPE_KRX_CANH = 0
<config sw> VOLT_KRX_CANH = 3
<config sw> PIN_KTX_CANH = 14
<config sw> TYPE_KTX_CANH = 0
<config sw> VOLT_KTX_CANH = 3
<config sw> PIN_LRX_CANH =  6
<config sw> TYPE_LTX_CANH = 0
<config sw> VOLT_LTX_CANH = 3
<config sw> VREF = 0
<config sw> BAUDRATE = 500000
<config sw> DATABIT = 0
<config sw> PARITY = 0
<config sw> TBYTE = 5
<config sw> TFRAME = 4
<config sw> F CAN NUMBER FRAME = 1
<config sw> RANGE =   0,0;
###########################################
#         End of config                   #
###########################################
SIZE_DATABASE = 16

 //------------------------frame 1
//>>Vehicle Profile: 2011 Audi Q7
//>>VIN: WAUNF68P46A001287
 
INFO_DATABASE = Req>1			000007DF 08 02 01 00 xx xx xx xx xx 	NONE	0	0
INFO_DATABASE = Res>1			000007E8 08 06 41 00 BF BE B9 93 37 	NONE	0	0

INFO_DATABASE = Req>1			000007DF 08 02 01 01 xx xx xx xx xx 	NONE	0	0
INFO_DATABASE = Res>1			000007E8 08 06 41 01 00 07 65 65 00 	NONE	0	0

INFO_DATABASE = Req>1			000007DF 08 02 01 13 xx xx xx xx xx 	NONE	0	0
INFO_DATABASE = Res>1			000007E8 08 03 41 13 03 00 00 00 00 	NONE	0	0

INFO_DATABASE = Req>1			000007DF 08 02 01 20 xx xx xx xx xx 	NONE	0	0
INFO_DATABASE = Res>1			000007E8 08 06 41 20 A0 05 B0 11 00 	NONE	0	0

INFO_DATABASE = Req>1			000007DF 08 02 01 40 xx xx xx xx xx 	NONE	0	0
INFO_DATABASE = Res>1			000007E8 08 06 41 40 FE D0 04 00 00 	NONE	0	0

INFO_DATABASE = Req>1			000007DF 08 02 09 00 xx xx xx xx xx 	NONE	0	0
INFO_DATABASE = Res>1			000007E8 08 06 49 00 55 00 00 00 00 	NONE	0	0

INFO_DATABASE = Req>1			000007DF 08 02 09 02 xx xx xx xx xx 	NONE	0	0
INFO_DATABASE = Res>1			000007E8 08 10 14 49 02 01 57 41 31 	NONE	0	0
INFO_DATABASE = Res>1			000007E8 08 21 43 47 41 46 45 30 42 	NONE	0	0
INFO_DATABASE = Res>1			000007E8 08 22 44 30 30 31 35 37 35 	NONE	0	0


INFO_DATABASE = Req>1			000007DF 08 01 07 xx xx xx xx xx xx 	NONE	0	0
INFO_DATABASE = Res>1			000007E8 08 10 84 47 40 {} {} {} {}  	NONE	0	0
INFO_DATABASE = Res>1			000007E8 08 21 {} {} {} {} {} {} {} 	NONE	0	0
INFO_DATABASE = Res>1			000007E8 08 22 {} {} {} {} {} {} {}  	NONE	0	0
INFO_DATABASE = Res>1			000007E8 08 23 {} {} {} {} {} {} {} 	NONE	0	0
INFO_DATABASE = Res>1			000007E8 08 24 {} {} {} {} {} {} {}  	NONE	0	0
INFO_DATABASE = Res>1			000007E8 08 25 {} {} {} {} {} {} {} 	NONE	0	0
INFO_DATABASE = Res>1			000007E8 08 26 {} {} {} {} {} {} {}  	NONE	0	0
INFO_DATABASE = Res>1			000007E8 08 27 {} {} {} {} {} {} {} 	NONE	0	0
INFO_DATABASE = Res>1			000007E8 08 28 {} {} {} {} {} {} {}  	NONE	0	0
INFO_DATABASE = Res>1			000007E8 08 29 {} {} {} {} {} {} {} 	NONE	0	0
INFO_DATABASE = Res>1			000007E8 08 2A {} {} {} {} {} {} {}  	NONE	0	0
INFO_DATABASE = Res>1			000007E8 08 2B {} {} {} {} {} {} {} 	NONE	0	0
INFO_DATABASE = Res>1			000007E8 08 2C {} {} {} {} {} {} {}  	NONE	0	0
INFO_DATABASE = Res>1			000007E8 08 2D {} {} {} {} {} {} {} 	NONE	0	0
INFO_DATABASE = Res>1			000007E8 08 2E {} {} {} {} {} {} {}  	NONE	0	0
INFO_DATABASE = Res>1			000007E8 08 2F {} {} {} {} {} {} {} 	NONE	0	0
INFO_DATABASE = Res>1			000007E8 08 20 {} {} {} {} {} {} {}  	NONE	0	0
INFO_DATABASE = Res>1			000007E8 08 21 {} {} {} {} {} {} {} 	NONE	0	0
INFO_DATABASE = Res>1			000007E8 08 22 {} {} {} {} {} {} {}  	NONE	0	0


INFO_DATABASE = Req>1			000007DF 08 03 02 xx xx xx xx xx xx 	NONE	0	0
INFO_DATABASE = Res>1			000007E8 08 07 42 00 00 7E 1F 80 03 	NONE	0	0

INFO_DATABASE = Req>1			000007DF 08 01 03 xx xx xx xx xx xx 	NONE	0	0
INFO_DATABASE = Res>1			000007E8 08 02 43 01 01 00 00 00 00 	NONE	0	0


INFO_DATABASE = Req>1			000007DF 08 01 04 00 00 00 00 00 00 	NONE	0	0
INFO_DATABASE = Res>1			000007E8 08 01 44 00 00 00 00 00 00 	NONE	0	0


//Livedata
//Engine speed: 19840(0.1RPM)
INFO_DATABASE = Req>1			000007DF 08 02 01 XX xx xx xx xx xx	NONE	0	0
INFO_DATABASE = Res>1			000007E8 08 06 41 XX 1f 00 00 00 37	NONE	0	0

//>>Vehicle speed: 1305.00 centimeters/sec
INFO_DATABASE = Req>1			000007DF 08 02 01 0D xx xx xx xx xx	NONE	0	0
INFO_DATABASE = Res>1			000007E8 08 06 41 0D 2F 00 00 00 37	NONE	0	0

//>>Throttle Position 1215(0.01%)
INFO_DATABASE = Req>1			000007DF 08 02 01 11 xx xx xx xx xx	NONE	0	0
INFO_DATABASE = Res>1			000007E8 08 06 41 11 1F 00 00 00 37	NONE	0	0

//>>Engine Coolant Temperature (ECT)=-304(1/16C)
INFO_DATABASE = Req>1			000007DF 08 02 01 05 xx xx xx xx xx	NONE	0	0
INFO_DATABASE = Res>1			000007E8 08 06 41 05 15 AA 00 00 37	NONE	0	0

//>>Fuel level 0.00%
INFO_DATABASE = Req>1			000007DF 08 02 01 2F xx xx xx xx xx	NONE	0	0
INFO_DATABASE = Res>1			000007E8 08 06 41 2F 00 00 00 00 37	NONE	0	0


###########################################
#         End of DataBase                 #
###########################################
'''